"""Main PDF Sentinel watcher implementation."""

import time
import logging
import traceback
from pathlib import Path
from datetime import datetime
from typing import Optional

from watchdog.observers import Observer

from pdf_sentinel.config import Config, ConversionEngine
from pdf_sentinel.handlers import PDFEventHandler
from pdf_sentinel.converters import MarkItDownConverter, PDFPlumberConverter

logger = logging.getLogger(__name__)


class PDFSentinel:
    """
    Main PDF Sentinel class for event-driven PDF to Markdown conversion.

    Features:
    - Event-driven monitoring (zero idle resources)
    - Multiple conversion engines
    - Automatic retry logic
    - Comprehensive error handling
    - Statistics tracking
    """

    def __init__(self, config: Config):
        """
        Initialize PDF Sentinel.

        Args:
            config: Configuration object
        """
        self.config = config
        self.observer: Optional[Observer] = None
        self.stats = Statistics()

        # Set up logging
        self._setup_logging()

        # Initialize converter
        self.converter = self._get_converter()

    def _setup_logging(self) -> None:
        """Configure logging based on config."""
        log_handlers = [logging.StreamHandler()]

        if self.config.log_file:
            log_handlers.append(logging.FileHandler(self.config.log_file))

        logging.basicConfig(
            level=self.config.log_level,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=log_handlers,
            force=True  # Override any existing configuration
        )

    def _get_converter(self):
        """Get the appropriate converter based on configuration."""
        if self.config.engine == ConversionEngine.MARKITDOWN:
            return MarkItDownConverter()
        elif self.config.engine == ConversionEngine.PDFPLUMBER:
            return PDFPlumberConverter()
        else:
            raise ValueError(f"Unknown conversion engine: {self.config.engine}")

    def process_pdf(self, pdf_path: Path, retry_count: int = 0) -> bool:
        """
        Process a single PDF file with retry logic.

        Args:
            pdf_path: Path to PDF file
            retry_count: Current retry attempt

        Returns:
            True if successful, False otherwise
        """
        try:
            # Generate output path
            output_path = self.config.output_dir / f"{pdf_path.stem}.md"

            # Convert PDF to markdown
            success, error_msg = self.converter.convert(pdf_path, output_path)

            if success:
                # Update statistics
                self.stats.total_processed += 1

                # Move to processed folder
                self._move_to_processed(pdf_path)
                return True
            else:
                # Retry logic
                if retry_count < self.config.max_retries:
                    logger.warning(
                        f"Retrying conversion ({retry_count + 1}/{self.config.max_retries}): "
                        f"{pdf_path.name}"
                    )
                    time.sleep(self.config.retry_delay)
                    return self.process_pdf(pdf_path, retry_count + 1)
                else:
                    # Max retries exceeded
                    self.stats.total_failed += 1
                    self._move_to_failed(pdf_path, error_msg or "Unknown error")
                    return False

        except Exception as e:
            error_msg = f"Unexpected error processing {pdf_path.name}: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            self.stats.total_failed += 1
            self._move_to_failed(pdf_path, error_msg)
            return False

    def _move_to_processed(self, pdf_path: Path) -> bool:
        """Move successfully processed PDF to processed directory."""
        try:
            processed_path = self.config.processed_dir / pdf_path.name

            # If file already exists, add timestamp
            if processed_path.exists():
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                processed_path = self.config.processed_dir / f"{pdf_path.stem}_{timestamp}{pdf_path.suffix}"

            pdf_path.rename(processed_path)
            logger.info(f"Moved to processed: {pdf_path.name}")
            return True

        except Exception as e:
            logger.error(f"Error moving {pdf_path.name} to processed: {str(e)}")
            return False

    def _move_to_failed(self, pdf_path: Path, error_msg: str) -> bool:
        """Move failed PDF to failed directory with error log."""
        try:
            failed_path = self.config.failed_dir / pdf_path.name

            # If file already exists, add timestamp
            if failed_path.exists():
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                failed_path = self.config.failed_dir / f"{pdf_path.stem}_{timestamp}{pdf_path.suffix}"

            pdf_path.rename(failed_path)

            # Write error log
            error_log_path = failed_path.with_suffix('.error.txt')
            with open(error_log_path, 'w', encoding='utf-8') as f:
                f.write(f"Failed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(error_msg)

            logger.warning(f"Moved to failed: {pdf_path.name}")
            return True

        except Exception as e:
            logger.error(f"Error moving {pdf_path.name} to failed: {str(e)}")
            return False

    def scan_existing_files(self) -> None:
        """Scan input directory for existing PDFs (startup scan)."""
        pdf_files = list(self.config.input_dir.glob("*.pdf"))

        if pdf_files:
            logger.info(f"Startup scan: Found {len(pdf_files)} existing PDF(s)")
            for pdf_path in pdf_files:
                logger.info(f"Processing existing file: {pdf_path.name}")
                self.process_pdf(pdf_path)
        else:
            logger.info("Startup scan: No existing PDFs found")

    def start(self, scan_existing: bool = True) -> None:
        """
        Start the PDF watcher service.

        Args:
            scan_existing: Whether to process existing PDFs on startup
        """
        logger.info("=" * 70)
        logger.info("PDF Sentinel v2.0 (Event-Driven)")
        logger.info(f"Input: {self.config.input_dir}")
        logger.info(f"Output: {self.config.output_dir}")
        logger.info(f"Conversion Engine: {self.converter.name}")
        logger.info("Event-driven monitoring with Watchdog (zero idle resources)")
        logger.info("=" * 70)

        # Process any existing files first
        if scan_existing:
            self.scan_existing_files()

        # Set up event handler and observer
        event_handler = PDFEventHandler(self)
        self.observer = Observer()
        self.observer.schedule(event_handler, str(self.config.input_dir), recursive=False)

        # Start watching
        self.observer.start()
        logger.info("File watcher started. Monitoring for new PDFs...")

        try:
            # Keep the script running
            while True:
                time.sleep(60)  # Wake up every minute for housekeeping

                # Log stats every hour
                if int(time.time()) % 3600 < 60:
                    self.stats.log_stats()

        except KeyboardInterrupt:
            logger.info("Shutting down file watcher...")
            self.stop()

    def stop(self) -> None:
        """Stop the PDF watcher service."""
        if self.observer:
            self.observer.stop()
            self.observer.join()
            self.stats.log_stats()
            logger.info("PDF Sentinel stopped")


class Statistics:
    """Track conversion statistics."""

    def __init__(self):
        self.total_processed = 0
        self.total_failed = 0
        self.total_pages = 0
        self.start_time = datetime.now()

    def log_stats(self) -> None:
        """Log current statistics."""
        uptime = datetime.now() - self.start_time
        logger.info(
            f"Stats: {self.total_processed} successful, {self.total_failed} failed, "
            f"{self.total_pages} pages, uptime: {uptime}"
        )
