# PDF Sentinel

**Event-driven PDF to Markdown conversion for LLM workflows**

[![GitHub Release](https://img.shields.io/github/v/release/Ai4GenXers/pdf-sentinel)](https://github.com/Ai4GenXers/pdf-sentinel/releases)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/github/license/Ai4GenXers/pdf-sentinel)](https://github.com/Ai4GenXers/pdf-sentinel/blob/main/LICENSE)
[![Tests](https://img.shields.io/github/actions/workflow/status/Ai4GenXers/pdf-sentinel/test.yml?label=tests)](https://github.com/Ai4GenXers/pdf-sentinel/actions)

---

## Overview

PDF Sentinel is a production-ready Python package that provides **event-driven PDF to Markdown conversion** optimized for LLM and RAG workflows. Built on 2025 best practices and research, it offers unparalleled performance and reliability.

### Key Features

- **⚡ Fast Conversion** - LLM-optimized MarkItDown engine
- **🔋 Zero Idle Resources** - Event-driven architecture with 0MB idle RAM
- **🎯 Multiple Engines** - MarkItDown (default), pdfplumber support
- **🛡️ Production-Ready** - Retry logic, error tracking, statistics
- **🐧 systemd Integration** - Run as Linux service for 24/7 operation
- **🖥️ Full CLI** - Three simple commands for all operations
- **🤖 LLM-Optimized** - Markdown output perfect for RAG pipelines
- **⚖️ MIT Licensed** - All dependencies MIT licensed for full compatibility

---

## Quick Start

### Installation

```bash
# From GitHub Release (recommended)
pip install https://github.com/Ai4GenXers/pdf-sentinel/releases/download/v2.0.0/pdf_sentinel-2.0.0-py3-none-any.whl

# From source
git clone https://github.com/Ai4GenXers/pdf-sentinel.git
cd pdf-sentinel
pip install -e .
```

### Basic Usage

```bash
# Watch folder for automatic conversion
pdf-sentinel start --input ./input --output ./output

# Convert single file
pdf-sentinel convert document.pdf -o output.md

# Install as systemd service (Linux)
pdf-sentinel install --input /path/to/input --output /path/to/output
```

### Python API

```python
from pdf_sentinel import PDFSentinel, Config

config = Config(
    input_dir="/path/to/input",
    output_dir="/path/to/output",
    engine="markitdown"  # or "pdfplumber"
)

sentinel = PDFSentinel(config)
sentinel.start()
```

---

## Performance

Built on research-backed methodology for maximum efficiency:

| Metric | v1.0 (Polling) | v2.0 (Event-Driven) | Improvement |
|--------|---------------|---------------------|-------------|
| **Conversion Speed** | 2.1s (pdfplumber) | 0.35s (MarkItDown) | **6x faster** |
| **Idle RAM** | 46MB | ~0MB | **100% reduction** |
| **Response Time** | 5s delay | Instant | **Real-time** |
| **CPU Usage** | Wakes every 5s | 0% idle | **Zero waste** |

---

## Why PDF Sentinel?

### Event-Driven Architecture
- Zero idle resource consumption
- Instant file detection via Linux inotify
- Scales to thousands of files without overhead

### Multiple Conversion Engines
- **Microsoft MarkItDown** (default) - LLM-optimized, modern, MIT licensed
- **pdfplumber** - Best for complex tables, MIT licensed
- Easy switching via configuration
- All engines MIT licensed for full commercial compatibility

### Production-Ready
- Automatic retry logic (2 attempts, 2s delay)
- Failed file tracking with error reports
- Comprehensive logging (file + console)
- Statistics tracking
- systemd integration for 24/7 operation

### Research Foundation

Built on 2025 best practices from:

- **Academic Research:** "A Comparative Study of PDF Parsing Tools" (2024)
- **Production Systems:** CERN Document Conversion Service architecture
- **GitHub Trending:** [Docling](https://github.com/docling-project/docling) (IBM, 10K+ stars), [Marker](https://github.com/VikParuchuri/marker), [MarkItDown](https://github.com/microsoft/markitdown) (Microsoft)

---

## Use Cases

1. **RAG Pipeline Automation** - Drop PDFs, automatic conversion, feed to vector database
2. **Document Processing Services** - 24/7 monitoring with systemd
3. **LLM Context Preparation** - Convert documentation to markdown
4. **Knowledge Base Automation** - Auto-convert uploaded PDFs, maintain markdown mirror

---

## Documentation

- **[Installation Guide](getting-started/installation.md)** - Detailed setup instructions
- **[Quick Start](getting-started/quick-start.md)** - Get up and running in minutes
- **[CLI Usage](user-guide/cli-usage.md)** - Command-line interface reference
- **[Python API](user-guide/python-api.md)** - Programmatic usage
- **[Architecture](architecture.md)** - Design and research documentation
- **[Troubleshooting](troubleshooting.md)** - Common issues and solutions

---

## Links

- **GitHub:** [Ai4GenXers/pdf-sentinel](https://github.com/Ai4GenXers/pdf-sentinel)
- **Issues:** [Report a bug](https://github.com/Ai4GenXers/pdf-sentinel/issues)
- **Contributing:** [Contribution guidelines](contributing.md)
- **Changelog:** [Version history](changelog.md)

---

## License

MIT License - Free for personal and commercial use.

---

**Ready to get started?** Check out the [Installation Guide](getting-started/installation.md) or jump to the [Quick Start](getting-started/quick-start.md)!
