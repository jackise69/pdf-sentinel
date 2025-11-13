"""PyMuPDF4LLM converter - Fast, LLM-optimized PDF to Markdown conversion."""

import time
import logging
import traceback
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional

from pdf_sentinel.converters.base import BaseConverter

logger = logging.getLogger(__name__)


class PyMuPDFConverter(BaseConverter):
    """
    PyMuPDF4LLM converter for fast, LLM-optimized PDF to Markdown conversion.

    Performance: 60x faster than pdfplumber (0.042s vs 2.5s per page)
    Best for: General use, LLM/RAG workflows, speed
    """

    @property
    def name(self) -> str:
        return "PyMuPDF4LLM"

    def convert(self, pdf_path: Path, output_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Convert PDF to Markdown using PyMuPDF4LLM.

        Args:
            pdf_path: Path to input PDF file
            output_path: Path to output markdown file

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        try:
            import pymupdf4llm

            logger.info(f"Converting with PyMuPDF4LLM: {pdf_path.name}")
            start_time = time.time()

            # Convert PDF to markdown
            md_text = pymupdf4llm.to_markdown(str(pdf_path))

            # Add metadata header
            header = f"""# {pdf_path.stem}

**Converted:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Conversion Engine:** PyMuPDF4LLM (LLM-optimized)
**Source:** {pdf_path.name}

---

"""

            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(header)
                f.write(md_text)

            elapsed = time.time() - start_time

            # Count pages (approximate from content)
            page_count = md_text.count('-----')  # PyMuPDF4LLM uses ----- as page separators

            logger.info(f"PyMuPDF4LLM conversion complete: {output_path.name} "
                       f"({page_count} pages in {elapsed:.2f}s)")

            return True, None

        except ImportError as e:
            error_msg = f"PyMuPDF4LLM not installed: {str(e)}\nInstall with: pip install pymupdf4llm"
            logger.error(error_msg)
            return False, error_msg

        except Exception as e:
            error_msg = f"PyMuPDF4LLM conversion failed: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            return False, error_msg
