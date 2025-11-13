# Testing

Testing guide for PDF Sentinel contributors.

## Running Tests

### All Tests

```bash
pytest
```

### With Coverage

```bash
pytest --cov=pdf_sentinel --cov-report=html
```

View coverage report:
```bash
open htmlcov/index.html
```

### Specific Tests

```bash
# Test configuration
pytest tests/test_config.py

# Test converters
pytest tests/test_converters.py

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

## Test Structure

```
tests/
├── __init__.py
├── test_config.py           # Configuration tests
├── test_converters.py        # Converter tests
├── test_watcher.py           # Watcher tests (future)
└── fixtures/
    └── sample.pdf            # Test PDFs
```

## Writing Tests

### Unit Tests

```python
import pytest
from pdf_sentinel import Config

def test_config_creation():
    config = Config(
        input_dir="/tmp/input",
        output_dir="/tmp/output"
    )
    assert config.engine == "markitdown"  # default

def test_config_validation():
    with pytest.raises(ValueError):
        Config(input_dir="", output_dir="/tmp/output")
```

### Integration Tests

```python
import pytest
from pathlib import Path
from pdf_sentinel import PDFSentinel, Config

def test_end_to_end_conversion(tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    output_dir.mkdir()

    # Copy test PDF
    test_pdf = Path("tests/fixtures/sample.pdf")
    (input_dir / "test.pdf").write_bytes(test_pdf.read_bytes())

    # Run conversion
    config = Config(input_dir=input_dir, output_dir=output_dir)
    sentinel = PDFSentinel(config)
    sentinel.process_existing_pdfs()

    # Verify output
    assert (output_dir / "test.md").exists()
```

## Code Quality

### Format Code

```bash
black src/ tests/
```

### Lint

```bash
ruff check src/ tests/
```

### Type Check

```bash
mypy src/
```

## Continuous Integration

GitHub Actions runs tests automatically:

- **On push:** All tests
- **On PR:** All tests + code quality checks
- **Python versions:** 3.10, 3.11, 3.12

See [.github/workflows/test.yml](.github/workflows/test.yml)

## Next Steps

- **[Contributing](../contributing.md)** - Contribution guidelines
- **[Release Process](release-process.md)** - How releases are made
