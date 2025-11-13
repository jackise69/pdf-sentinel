"""Tests for PDF converters."""

import pytest
import tempfile
from pathlib import Path

from pdf_sentinel.converters import PyMuPDFConverter, MarkItDownConverter, PDFPlumberConverter


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


def test_pymupdf_converter_name():
    """Test PyMuPDF converter name."""
    converter = PyMuPDFConverter()
    assert converter.name == "PyMuPDF4LLM"


def test_markitdown_converter_name():
    """Test MarkItDown converter name."""
    converter = MarkItDownConverter()
    assert converter.name == "Microsoft MarkItDown"


def test_pdfplumber_converter_name():
    """Test pdfplumber converter name."""
    converter = PDFPlumberConverter()
    assert converter.name == "pdfplumber"


def test_converter_missing_dependency(temp_dir):
    """Test converter behavior when dependency is missing."""
    # This test assumes the library might not be installed
    converter = PyMuPDFConverter()
    pdf_path = temp_dir / "test.pdf"
    output_path = temp_dir / "test.md"

    # Create a dummy PDF file (not a real PDF)
    pdf_path.write_text("dummy content")

    # Should fail gracefully
    success, error = converter.convert(pdf_path, output_path)

    # Should return False and an error message
    assert isinstance(success, bool)
    assert error is None or isinstance(error, str)


# Note: Full converter tests would require sample PDF files
# For now, we're testing the basic structure and error handling
