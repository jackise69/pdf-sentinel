"""Event handlers for PDF file system events."""

import time
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from watchdog.events import FileSystemEventHandler

if TYPE_CHECKING:
    from pdf_sentinel.watcher import PDFSentinel

logger = logging.getLogger(__name__)


class PDFEventHandler(FileSystemEventHandler):
    """Event handler for PDF file creation events."""

    def __init__(self, sentinel: "PDFSentinel"):
        """
        Initialize PDF event handler.

        Args:
            sentinel: PDFSentinel instance to process files
        """
        super().__init__()
        self.sentinel = sentinel

    def on_created(self, event):
        """
        Called when a file is created in the watched directory.

        Args:
            event: File system event
        """
        # Ignore directories
        if event.is_directory:
            return

        # Only process PDF files
        if not event.src_path.lower().endswith('.pdf'):
            return

        pdf_path = Path(event.src_path)

        # Wait a moment for file to be fully written
        time.sleep(0.5)

        # Check if file still exists and is accessible
        if not pdf_path.exists():
            logger.warning(f"File disappeared before processing: {pdf_path.name}")
            return

        logger.info(f"New PDF detected: {pdf_path.name}")

        # Process the PDF
        self.sentinel.process_pdf(pdf_path)

        # Log stats every 10 files
        if (self.sentinel.stats.total_processed + self.sentinel.stats.total_failed) % 10 == 0:
            self.sentinel.stats.log_stats()
