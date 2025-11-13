# Python API

Use PDF Sentinel programmatically in your Python applications.

## Basic Usage

```python
from pdf_sentinel import PDFSentinel, Config

# Create configuration
config = Config(
    input_dir="/path/to/input",
    output_dir="/path/to/output",
    engine="pymupdf4llm"
)

# Create sentinel instance
sentinel = PDFSentinel(config)

# Start watching
sentinel.start()  # Blocks until Ctrl+C
```

## Configuration

### Config Class

```python
from pdf_sentinel import Config
from pathlib import Path

config = Config(
    input_dir=Path("/path/to/input"),      # Required
    output_dir=Path("/path/to/output"),    # Required
    engine="pymupdf4llm",                  # Optional, default: "pymupdf4llm"
    max_retries=2,                         # Optional, default: 2
    retry_delay=2.0                        # Optional, default: 2.0 seconds
)
```

**Parameters:**

- `input_dir` (Path | str) - Directory to watch for PDFs
- `output_dir` (Path | str) - Directory to save markdown files
- `engine` (str) - Conversion engine: `"pymupdf4llm"`, `"markitdown"`, or `"pdfplumber"`
- `max_retries` (int) - Number of retry attempts for failed conversions
- `retry_delay` (float) - Seconds to wait between retry attempts

### From Environment Variables

```python
from pdf_sentinel import Config

# Reads from PDF_SENTINEL_* environment variables
config = Config.from_env()
```

## PDFSentinel Class

### Constructor

```python
from pdf_sentinel import PDFSentinel, Config

sentinel = PDFSentinel(config)
```

### Methods

#### `start(scan_existing: bool = True) -> None`

Start watching the input directory.

```python
sentinel.start()              # Scan and process existing PDFs
sentinel.start(scan_existing=False)  # Only watch for new files
```

**Blocks until interrupted (Ctrl+C).**

#### `stop() -> None`

Stop watching (called automatically on Ctrl+C).

```python
sentinel.stop()
```

## Single File Conversion

```python
from pdf_sentinel.converters import PyMuPDFConverter, MarkItDownConverter, PDFPlumberConverter
from pathlib import Path

# Choose converter
converter = PyMuPDFConverter()
# converter = MarkItDownConverter()
# converter = PDFPlumberConverter()

# Convert
success, error = converter.convert(
    pdf_path=Path("document.pdf"),
    output_path=Path("output.md")
)

if success:
    print("Conversion successful!")
else:
    print(f"Conversion failed: {error}")
```

## Advanced Usage

### Custom Event Handler

```python
from pdf_sentinel import PDFSentinel, Config
from pdf_sentinel.handlers import PDFEventHandler
from watchdog.events import FileSystemEvent

class CustomHandler(PDFEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        print(f"New file detected: {event.src_path}")
        super().on_created(event)  # Call original handler

# Use custom handler
config = Config(input_dir="./input", output_dir="./output")
sentinel = PDFSentinel(config)
sentinel.start()
```

### Context Manager

```python
from pdf_sentinel import PDFSentinel, Config

config = Config(input_dir="./input", output_dir="./output")

with PDFSentinel(config) as sentinel:
    sentinel.start()
# Automatically stops on exit
```

### Async Integration

```python
import asyncio
from pdf_sentinel import PDFSentinel, Config

async def monitor_pdfs():
    config = Config(input_dir="./input", output_dir="./output")
    sentinel = PDFSentinel(config)

    # Run in executor to avoid blocking
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, sentinel.start)

asyncio.run(monitor_pdfs())
```

## Exception Handling

```python
from pdf_sentinel import PDFSentinel, Config
from pdf_sentinel.exceptions import ConfigError, ConversionError

try:
    config = Config(input_dir="./input", output_dir="./output")
    sentinel = PDFSentinel(config)
    sentinel.start()
except ConfigError as e:
    print(f"Configuration error: {e}")
except ConversionError as e:
    print(f"Conversion error: {e}")
except KeyboardInterrupt:
    print("Stopped by user")
```

## Logging

```python
import logging
from pdf_sentinel import PDFSentinel, Config

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pdf-sentinel.log'),
        logging.StreamHandler()
    ]
)

# PDF Sentinel will use this configuration
config = Config(input_dir="./input", output_dir="./output")
sentinel = PDFSentinel(config)
sentinel.start()
```

## Complete Example

```python
#!/usr/bin/env python3
"""
PDF Sentinel monitoring script with custom logging and error handling.
"""
import logging
from pathlib import Path
from pdf_sentinel import PDFSentinel, Config

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('/var/log/pdf-sentinel.log'),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)

    try:
        # Create configuration
        config = Config(
            input_dir=Path("/data/pdfs/input"),
            output_dir=Path("/data/pdfs/output"),
            engine="pymupdf4llm",
            max_retries=3,
            retry_delay=5.0
        )

        logger.info("Starting PDF Sentinel...")
        logger.info(f"Input: {config.input_dir}")
        logger.info(f"Output: {config.output_dir}")
        logger.info(f"Engine: {config.engine}")

        # Start monitoring
        sentinel = PDFSentinel(config)
        sentinel.start()

    except KeyboardInterrupt:
        logger.info("Stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
```

## Next Steps

- **[CLI Usage](cli-usage.md)** - Command-line interface
- **[systemd Service](systemd-service.md)** - Run as system service
- **[Conversion Engines](conversion-engines.md)** - Engine comparison
