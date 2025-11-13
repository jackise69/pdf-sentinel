"""Configuration management for PDF Sentinel."""

import os
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class ConversionEngine(Enum):
    """Supported PDF conversion engines."""
    MARKITDOWN = "markitdown"
    PDFPLUMBER = "pdfplumber"


@dataclass
class Config:
    """PDF Sentinel configuration."""

    # Directories
    input_dir: Path
    output_dir: Path
    processed_dir: Optional[Path] = None
    failed_dir: Optional[Path] = None

    # Conversion settings
    engine: ConversionEngine = ConversionEngine.MARKITDOWN
    max_retries: int = 2
    retry_delay: float = 2.0

    # Logging
    log_file: Optional[Path] = None
    log_level: str = "INFO"

    def __post_init__(self):
        """Initialize derived paths and create directories."""
        # Convert strings to Path objects
        self.input_dir = Path(self.input_dir)
        self.output_dir = Path(self.output_dir)

        # Set default subdirectories
        if self.processed_dir is None:
            self.processed_dir = self.input_dir / "processed"
        else:
            self.processed_dir = Path(self.processed_dir)

        if self.failed_dir is None:
            self.failed_dir = self.input_dir / "failed"
        else:
            self.failed_dir = Path(self.failed_dir)

        # Create all directories
        for directory in [self.input_dir, self.output_dir,
                         self.processed_dir, self.failed_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        # Convert engine string to enum if needed
        if isinstance(self.engine, str):
            self.engine = ConversionEngine(self.engine.lower())

    @classmethod
    def from_env(cls, base_dir: Optional[Path] = None) -> "Config":
        """Create configuration from environment variables."""
        if base_dir is None:
            base_dir = Path(os.getenv("PDF_SENTINEL_DIR", Path.home() / "pdf-conversions"))
        else:
            base_dir = Path(base_dir)

        return cls(
            input_dir=Path(os.getenv("PDF_INPUT_DIR", base_dir / "input")),
            output_dir=Path(os.getenv("PDF_OUTPUT_DIR", base_dir / "output")),
            engine=os.getenv("PDF_CONVERTER", "markitdown"),
            max_retries=int(os.getenv("PDF_MAX_RETRIES", "2")),
            log_file=base_dir / "pdf_watcher.log",
            log_level=os.getenv("PDF_LOG_LEVEL", "INFO"),
        )
