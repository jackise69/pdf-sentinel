"""Base converter interface."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Tuple, Optional


class BaseConverter(ABC):
    """Abstract base class for PDF converters."""

    @abstractmethod
    def convert(self, pdf_path: Path, output_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Convert PDF to Markdown.

        Args:
            pdf_path: Path to input PDF file
            output_path: Path to output markdown file

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Engine name."""
        pass
