"""Microsoft MarkItDown converter - LLM-optimized PDF to Markdown conversion."""

import time
import logging
import traceback
from pathlib import Path
from datetime import datetime
from typing import Tuple, Optional

from pdf_sentinel.converters.base import BaseConverter

logger = logging.getLogger(__name__)


class MarkItDownConverter(BaseConverter):
    """
    Microsoft MarkItDown converter for LLM-optimized PDF to Markdown conversion.

    Performance: ~0.35s per 6-page document
    Best for: Microsoft ecosystem, LLM workflows
    """

    @property
    def name(self) -> str:
        return "Microsoft MarkItDown"

    def convert(self, pdf_path: Path, output_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Convert PDF to Markdown using Microsoft MarkItDown.

        Args:
            pdf_path: Path to input PDF file
            output_path: Path to output markdown file

        Returns:
            Tuple of (success: bool, error_message: Optional[str])
        """
        try:
            from markitdown import MarkItDown

            logger.info(f"Converting with MarkItDown: {pdf_path.name}")
            start_time = time.time()

            # Initialize converter
            md = MarkItDown()

            # Convert PDF
            result = md.convert(str(pdf_path))

            # Add metadata header
            header = f"""# {pdf_path.stem}

**Converted:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Conversion Engine:** Microsoft MarkItDown (LLM-optimized)
**Source:** {pdf_path.name}

---

"""

            # Write to file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(header)
                f.write(result.text_content)

            elapsed = time.time() - start_time

            logger.info(f"MarkItDown conversion complete: {output_path.name} ({elapsed:.2f}s)")

            return True, None

        except ImportError as e:
            error_msg = f"MarkItDown not installed: {str(e)}\nInstall with: pip install markitdown"
            logger.error(error_msg)
            return False, error_msg

        except Exception as e:
            error_msg = f"MarkItDown conversion failed: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            return False, error_msg
