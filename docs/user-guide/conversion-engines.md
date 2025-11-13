# Conversion Engines

PDF Sentinel supports two conversion engines, each optimized for different use cases. All engines are MIT licensed for maximum compatibility.

## Engine Comparison

| Feature | MarkItDown (Default) | pdfplumber |
|---------|----------------------|------------|
| **Speed** | ⚡⚡ Fast (~0.35s) | ⚡ Slower (2.1s) |
| **LLM-Optimized** | ✅ Yes | ❌ No |
| **Table Handling** | ⚡⚡ Good | ⚡⚡⚡ Excellent |
| **Text Extraction** | ⚡⚡ Good | ⚡⚡ Good |
| **Formatting Preservation** | ⚡⚡ Good | ⚡ Basic |
| **Memory Usage** | Low | Medium |
| **License** | MIT | MIT |
| **Best For** | LLM workflows, general use | Complex tables, data extraction |

## Microsoft MarkItDown (Default)

**Recommended for:** Most use cases, LLM/RAG workflows, production deployments

### Strengths

- **LLM-optimized** - Designed for LLM context by Microsoft
- **Modern architecture** - Released 2024 with latest best practices
- **Good all-around performance** - Balanced speed and accuracy
- **Microsoft Office support** - Handles .docx, .pptx alongside PDFs
- **MIT licensed** - Full commercial and open source compatibility

### Weaknesses

- Newer library (2024 release)
- Not as fast as some AGPL-licensed alternatives

### Usage

```bash
# CLI
pdf-sentinel convert document.pdf -o output.md --engine markitdown

# Python API
from pdf_sentinel import Config
config = Config(input_dir="./input", output_dir="./output", engine="markitdown")
```

### When to Use

- General PDF to markdown conversion (default)
- LLM/RAG pipeline integration
- Converting Microsoft Office documents
- Modern PDF files from digital sources
- Production deployments

## pdfplumber

**Recommended for:** Complex table layouts, data extraction, legacy PDFs

### Strengths

- **Excellent table handling** - Best-in-class for complex tables
- **Precise text positioning** - Accurate character-level extraction
- **Mature library** - Well-tested and reliable

### Weaknesses

- Slower than MarkItDown (~6x)
- Not LLM-optimized
- Higher memory usage
- Basic markdown formatting

### Usage

```bash
# CLI
pdf-sentinel convert document.pdf -o output.md --engine pdfplumber

# Python API
from pdf_sentinel import Config
config = Config(input_dir="./input", output_dir="./output", engine="pdfplumber")
```

### When to Use

- PDFs with complex table layouts
- Financial reports, spreadsheets
- Data extraction from structured documents
- When table accuracy is critical

## Choosing the Right Engine

### Decision Flow

1. **Default choice:** Start with `markitdown`
   - LLM-optimized, modern, works for 90% of use cases
   - MIT licensed for full compatibility

2. **Tables important?** Try `pdfplumber`
   - Best table extraction
   - Worth the performance trade-off for complex tables

3. **Still not satisfied?** Test both engines
   - Compare outputs side-by-side
   - Choose based on your specific documents

### Performance Benchmarks

Tested on 6-page business PDF:

| Engine | Time | RAM | Output Quality | License |
|--------|------|-----|----------------|---------|
| MarkItDown | ~0.35s | 52MB | Good (LLM-optimized) | MIT |
| pdfplumber | 2.1s | 68MB | Good (best tables) | MIT |

## Switching Engines

Easy to test different engines on the same document:

```bash
# Convert with both engines
pdf-sentinel convert doc.pdf -o doc-markitdown.md --engine markitdown
pdf-sentinel convert doc.pdf -o doc-pdfplumber.md --engine pdfplumber

# Compare outputs
diff doc-markitdown.md doc-pdfplumber.md
```

## Engine-Specific Configuration

### MarkItDown

```python
from pdf_sentinel.converters import MarkItDownConverter

converter = MarkItDownConverter()
success, error = converter.convert(pdf_path, output_path)
```

### pdfplumber

```python
from pdf_sentinel.converters import PDFPlumberConverter

converter = PDFPlumberConverter()
success, error = converter.convert(pdf_path, output_path)
```

## License Compatibility

Both conversion engines are MIT licensed, ensuring:
- ✅ Full commercial use allowed
- ✅ No copyleft restrictions
- ✅ Compatible with any open source license
- ✅ No vendor lock-in or licensing fees

## Next Steps

- **[Architecture](../architecture.md)** - Research and design decisions
- **[Performance](../architecture/performance.md)** - Detailed benchmarks
- **[Troubleshooting](../troubleshooting.md)** - Common conversion issues
