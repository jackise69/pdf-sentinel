"""
PDF Sentinel - Event-driven PDF to Markdown conversion.

A production-grade system for automatically converting PDF files to Markdown format,
optimized for LLM and RAG workflows.
"""

__version__ = "2.0.0"
__author__ = "AI4GenXers"
__description__ = "Event-driven PDF to Markdown conversion for LLM workflows"

from pdf_sentinel.watcher import PDFSentinel
from pdf_sentinel.config import Config

__all__ = ["PDFSentinel", "Config", "__version__"]
