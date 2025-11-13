"""Tests for PDF Sentinel configuration."""

import pytest
import tempfile
from pathlib import Path

from pdf_sentinel.config import Config, ConversionEngine


def test_config_basic():
    """Test basic configuration creation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(
            input_dir=Path(tmpdir) / "input",
            output_dir=Path(tmpdir) / "output"
        )

        assert config.input_dir.exists()
        assert config.output_dir.exists()
        assert config.processed_dir.exists()
        assert config.failed_dir.exists()
        assert config.engine == ConversionEngine.PYMUPDF4LLM


def test_config_custom_engine():
    """Test configuration with custom engine."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = Config(
            input_dir=Path(tmpdir) / "input",
            output_dir=Path(tmpdir) / "output",
            engine="markitdown"
        )

        assert config.engine == ConversionEngine.MARKITDOWN


def test_config_from_env(monkeypatch):
    """Test configuration from environment variables."""
    with tempfile.TemporaryDirectory() as tmpdir:
        monkeypatch.setenv("PDF_SENTINEL_DIR", tmpdir)
        monkeypatch.setenv("PDF_CONVERTER", "pdfplumber")
        monkeypatch.setenv("PDF_MAX_RETRIES", "3")

        config = Config.from_env()

        assert config.engine == ConversionEngine.PDFPLUMBER
        assert config.max_retries == 3
        assert str(tmpdir) in str(config.input_dir)


def test_config_directories_created():
    """Test that all directories are created."""
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)

        config = Config(
            input_dir=base / "input",
            output_dir=base / "output"
        )

        # Check all directories exist
        assert (base / "input").exists()
        assert (base / "output").exists()
        assert (base / "input" / "processed").exists()
        assert (base / "input" / "failed").exists()


def test_config_invalid_engine():
    """Test configuration with invalid engine."""
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(ValueError):
            Config(
                input_dir=Path(tmpdir) / "input",
                output_dir=Path(tmpdir) / "output",
                engine="invalid_engine"
            )
