# Configuration

PDF Sentinel can be configured via command-line arguments, environment variables, or programmatically via the Python API.

## Configuration Options

### Input/Output Directories

**Required:** Specify where to watch for PDFs and where to save markdown output.

```bash
# CLI
pdf-sentinel start --input ./input --output ./output

# Environment variables
export PDF_SENTINEL_INPUT_DIR=/path/to/input
export PDF_SENTINEL_OUTPUT_DIR=/path/to/output
pdf-sentinel start

# Python API
from pdf_sentinel import Config
config = Config(input_dir="/path/to/input", output_dir="/path/to/output")
```

### Conversion Engine

**Default:** `pymupdf4llm`

Choose which PDF parsing library to use:

```bash
# CLI
pdf-sentinel start --input ./input --output ./output --engine markitdown

# Environment variable
export PDF_SENTINEL_ENGINE=markitdown

# Python API
config = Config(input_dir="./input", output_dir="./output", engine="markitdown")
```

**Available engines:**
- `pymupdf4llm` - Fastest (60x faster), LLM-optimized (default)
- `markitdown` - Microsoft 2024, LLM-optimized
- `pdfplumber` - Best for complex tables

### Retry Logic

**Default:** 2 retries with 2-second delay

Configure automatic retry behavior for failed conversions:

```bash
# Environment variables
export PDF_SENTINEL_MAX_RETRIES=3
export PDF_SENTINEL_RETRY_DELAY=5.0  # seconds

# Python API
config = Config(
    input_dir="./input",
    output_dir="./output",
    max_retries=3,
    retry_delay=5.0
)
```

### Logging

**Default:** INFO level, console + file output

Configure logging behavior:

```bash
# Environment variables
export PDF_SENTINEL_LOG_LEVEL=DEBUG
export PDF_SENTINEL_LOG_FILE=/var/log/pdf-sentinel/watcher.log

# Python API
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Log levels:**
- `DEBUG` - Detailed diagnostic information
- `INFO` - General informational messages (default)
- `WARNING` - Warning messages
- `ERROR` - Error messages only

## Environment Variables Reference

| Variable | Type | Default | Description |
|----------|------|---------|-------------|
| `PDF_SENTINEL_INPUT_DIR` | string | Required | Directory to watch for PDFs |
| `PDF_SENTINEL_OUTPUT_DIR` | string | Required | Directory for markdown output |
| `PDF_SENTINEL_ENGINE` | string | `pymupdf4llm` | Conversion engine to use |
| `PDF_SENTINEL_MAX_RETRIES` | int | `2` | Number of retry attempts |
| `PDF_SENTINEL_RETRY_DELAY` | float | `2.0` | Seconds between retries |
| `PDF_SENTINEL_LOG_LEVEL` | string | `INFO` | Logging verbosity |
| `PDF_SENTINEL_LOG_FILE` | string | `./pdf_watcher.log` | Log file path |

## Configuration Examples

### Basic Setup

```bash
pdf-sentinel start --input ~/Documents/pdfs --output ~/Documents/markdown
```

### High Reliability

For mission-critical document processing:

```bash
export PDF_SENTINEL_MAX_RETRIES=5
export PDF_SENTINEL_RETRY_DELAY=10.0
export PDF_SENTINEL_LOG_LEVEL=DEBUG
export PDF_SENTINEL_LOG_FILE=/var/log/pdf-sentinel/watcher.log

pdf-sentinel start --input /data/input --output /data/output
```

### Complex Tables

When dealing with PDFs that have complex table layouts:

```bash
pdf-sentinel start --input ./input --output ./output --engine pdfplumber
```

### Python Configuration

```python
from pdf_sentinel import PDFSentinel, Config
from pathlib import Path

config = Config(
    input_dir=Path("/data/input"),
    output_dir=Path("/data/output"),
    engine="pymupdf4llm",
    max_retries=3,
    retry_delay=5.0
)

sentinel = PDFSentinel(config)
sentinel.start()
```

## Next Steps

- **[CLI Usage](../user-guide/cli-usage.md)** - Full command reference
- **[Python API](../user-guide/python-api.md)** - Programmatic usage
- **[Conversion Engines](../user-guide/conversion-engines.md)** - Engine comparison and selection
