# CLI Usage

PDF Sentinel provides three main commands: `start`, `convert`, and `install`.

## Commands Overview

```bash
pdf-sentinel --help
```

### `start` - Watch Folder

Start monitoring a folder for automatic PDF conversion.

```bash
pdf-sentinel start --input INPUT_DIR --output OUTPUT_DIR [OPTIONS]
```

**Options:**

- `--input`, `-i` - Input directory to watch for PDFs (required)
- `--output`, `-o` - Output directory for markdown files (required)
- `--engine`, `-e` - Conversion engine: `pymupdf4llm`, `markitdown`, or `pdfplumber` (default: `pymupdf4llm`)
- `--scan` / `--no-scan` - Process existing PDFs on startup (default: `--scan`)

**Example:**

```bash
pdf-sentinel start --input ~/pdfs/input --output ~/pdfs/output --engine pymupdf4llm
```

**Behavior:**

1. Scans input directory for existing PDFs (if `--scan`)
2. Converts all found PDFs to markdown
3. Starts watching for new PDFs
4. Automatically converts new PDFs as they appear
5. Moves processed PDFs to `input/processed/`
6. Moves failed PDFs to `input/failed/` with error reports

**Stop watching:** Press `Ctrl+C`

### `convert` - Single File

Convert a single PDF to markdown.

```bash
pdf-sentinel convert PDF_FILE --output OUTPUT_FILE [OPTIONS]
```

**Options:**

- `PDF_FILE` - Path to PDF file to convert (required)
- `--output`, `-o` - Output markdown file path (required)
- `--engine`, `-e` - Conversion engine (default: `pymupdf4llm`)

**Example:**

```bash
pdf-sentinel convert document.pdf -o output.md --engine markitdown
```

### `install` - systemd Service

Install PDF Sentinel as a systemd user service (Linux only).

```bash
pdf-sentinel install --input INPUT_DIR --output OUTPUT_DIR [OPTIONS]
```

**Options:**

- `--input`, `-i` - Input directory to watch (required)
- `--output`, `-o` - Output directory for markdown (required)
- `--engine`, `-e` - Conversion engine (default: `pymupdf4llm`)

**Example:**

```bash
pdf-sentinel install --input /home/user/pdfs/input --output /home/user/pdfs/output
```

**This will:**

1. Create systemd user service file at `~/.config/systemd/user/pdf-sentinel.service`
2. Enable the service to start on boot
3. Start the service immediately

**Service management:**

```bash
# Check status
systemctl --user status pdf-sentinel

# Stop service
systemctl --user stop pdf-sentinel

# Start service
systemctl --user start pdf-sentinel

# Restart service
systemctl --user restart pdf-sentinel

# Disable service
systemctl --user disable pdf-sentinel

# View logs
journalctl --user -u pdf-sentinel -f
```

## Common Usage Patterns

### Development Testing

```bash
# Terminal 1: Watch with verbose output
pdf-sentinel start -i ./test-input -o ./test-output --engine pymupdf4llm

# Terminal 2: Drop test files
cp test.pdf test-input/
```

### Production Service

```bash
# Install and forget
pdf-sentinel install -i /data/pdfs/input -o /data/pdfs/output

# Check it's running
systemctl --user status pdf-sentinel
```

### Batch Conversion

```bash
# Convert all PDFs in a directory
for pdf in pdfs/*.pdf; do
    pdf-sentinel convert "$pdf" -o "markdown/$(basename "$pdf" .pdf).md"
done
```

### Engine Comparison

```bash
# Test different engines on the same file
pdf-sentinel convert doc.pdf -o doc-pymupdf.md --engine pymupdf4llm
pdf-sentinel convert doc.pdf -o doc-markitdown.md --engine markitdown
pdf-sentinel convert doc.pdf -o doc-pdfplumber.md --engine pdfplumber

# Compare results
diff doc-pymupdf.md doc-markitdown.md
```

## Environment Variables

All CLI options can be set via environment variables:

```bash
export PDF_SENTINEL_INPUT_DIR=/path/to/input
export PDF_SENTINEL_OUTPUT_DIR=/path/to/output
export PDF_SENTINEL_ENGINE=markitdown

# Now you can run without flags
pdf-sentinel start
```

See [Configuration](../getting-started/configuration.md) for full environment variable reference.

## Exit Codes

- `0` - Success
- `1` - Error (configuration, conversion, or runtime error)
- `2` - Interrupted by user (Ctrl+C)

## Next Steps

- **[Python API](python-api.md)** - Programmatic usage
- **[systemd Service](systemd-service.md)** - Advanced service management
- **[Conversion Engines](conversion-engines.md)** - Choose the right engine
