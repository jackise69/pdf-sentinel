"""pdfplumber converter - Best for complex table extraction."""

import time
import logging
import traceback
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional

from pdf_sentinel.converters.base import BaseConverter

logger = logging.getLogger(__name__)


class PDFPlumberConverter(BaseConverter):
    """
    pdfplumber converter for detailed table extraction.

    Performance: ~0.35s per page (slower than PyMuPDF)
    Best for: Complex tables, detailed layout preservation
    """

    @property
    def name(self) -> str:
        return "pdfplumber"

    def convert(self, pdf_path: Path, output_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Convert PDF to Markdown using pdfplumber.

        Args:
            pdf_path: Path to input PDF file
            output_path: Path to output markdown file

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        try:
            import pdfplumber

            logger.info(f"Converting with pdfplumber: {pdf_path.name}")
            start_time = time.time()

            with open(output_path, 'w', encoding='utf-8') as md_file:
                with pdfplumber.open(pdf_path) as pdf:
                    total_pages = len(pdf.pages)

                    # Write document header
                    md_file.write(f"# {pdf_path.stem}\n\n")
                    md_file.write(f"**Converted:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    md_file.write(f"**Conversion Engine:** pdfplumber (table-optimized)\n")
                    md_file.write(f"**Total Pages:** {total_pages}\n\n")
                    md_file.write("---\n\n")

                    for page_num, page in enumerate(pdf.pages, 1):
                        # Progress logging
                        if page_num % 10 == 0:
                            logger.debug(f"Processing page {page_num}/{total_pages}")

                        # Add page header
                        md_file.write(f"\n\n---\n## Page {page_num}\n\n")

                        # Extract tables first
                        tables = page.extract_tables()

                        # Extract text
                        text = page.extract_text()

                        if tables:
                            for table_num, table in enumerate(tables, 1):
                                if table:
                                    md_file.write(f"\n### Table {table_num}\n\n")
                                    for row_num, row in enumerate(table):
                                        if row:
                                            cleaned_row = [str(cell).strip() if cell else '' for cell in row]
                                            md_file.write("| " + " | ".join(cleaned_row) + " |\n")
                                            if row_num == 0:
                                                md_file.write("| " + " | ".join(['---'] * len(cleaned_row)) + " |\n")
                                    md_file.write("\n")

                        # Write text content
                        if text:
                            md_file.write(text)
                            md_file.write("\n")

            elapsed = time.time() - start_time
            logger.info(f"pdfplumber conversion complete: {output_path.name} "
                       f"({total_pages} pages in {elapsed:.2f}s)")

            return True, None

        except ImportError as e:
            error_msg = f"pdfplumber not installed: {str(e)}\nInstall with: pip install pdfplumber"
            logger.error(error_msg)
            return False, error_msg

        except Exception as e:
            error_msg = f"pdfplumber conversion failed: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            return False, error_msg
