# Quick Start

Get up and running with PDF Sentinel in under 5 minutes.

## Installation

```bash
pip install https://github.com/Ai4GenXers/pdf-sentinel/releases/download/v2.0.0/pdf_sentinel-2.0.0-py3-none-any.whl
```

## Basic Usage

### 1. Convert a Single PDF

The simplest way to convert a PDF:

```bash
pdf-sentinel convert document.pdf -o output.md
```

This converts `document.pdf` to `output.md` using the default PyMuPDF4LLM engine.

### 2. Watch a Folder

For automatic conversion of multiple PDFs:

```bash
# Create input and output directories
mkdir input output

# Start watching
pdf-sentinel start --input ./input --output ./output
```

Now drop PDF files into the `input/` folder and they'll automatically convert to markdown in `output/`.

**Try it:**

```bash
# Copy a PDF to the input folder
cp ~/Documents/sample.pdf input/

# Check the output folder
ls output/
# You should see: sample.md
```

### 3. Run as a Service (Linux)

For 24/7 operation, install as a systemd service:

```bash
pdf-sentinel install --input /home/user/pdfs/input --output /home/user/pdfs/output
```

This creates and enables a systemd user service that starts automatically.

## Choose a Conversion Engine

PDF Sentinel supports three conversion engines:

```bash
# PyMuPDF4LLM (default, fastest, LLM-optimized)
pdf-sentinel convert document.pdf -o output.md --engine pymupdf4llm

# Microsoft MarkItDown (LLM-optimized, modern)
pdf-sentinel convert document.pdf -o output.md --engine markitdown

# pdfplumber (best for complex tables)
pdf-sentinel convert document.pdf -o output.md --engine pdfplumber
```

## Python API

For programmatic use:

```python
from pdf_sentinel import PDFSentinel, Config

# Create configuration
config = Config(
    input_dir="/path/to/input",
    output_dir="/path/to/output",
    engine="pymupdf4llm"
)

# Start watching
sentinel = PDFSentinel(config)
sentinel.start()
```

## What's Next?

- **[Configuration](configuration.md)** - Customize behavior, retry logic, logging
- **[CLI Usage](../user-guide/cli-usage.md)** - Full command reference
- **[Python API](../user-guide/python-api.md)** - Detailed API documentation
- **[systemd Service](../user-guide/systemd-service.md)** - Advanced service management
