# Installation

PDF Sentinel requires Python 3.10 or higher and can be installed in several ways.

## Requirements

- **Python:** 3.10, 3.11, or 3.12
- **Operating System:** Linux (recommended), macOS, Windows
- **Dependencies:** Automatically installed via pip

## Installation Methods

### Method 1: From GitHub Release (Recommended)

Install the latest stable release directly from GitHub:

```bash
pip install https://github.com/Ai4GenXers/pdf-sentinel/releases/download/v2.0.0/pdf_sentinel-2.0.0-py3-none-any.whl
```

### Method 2: From Source

Clone the repository and install in editable mode:

```bash
git clone https://github.com/Ai4GenXers/pdf-sentinel.git
cd pdf-sentinel
pip install -e .
```

### Method 3: Development Install

For contributors and developers:

```bash
git clone https://github.com/Ai4GenXers/pdf-sentinel.git
cd pdf-sentinel
pip install -e ".[dev]"
```

This installs additional development dependencies:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatter
- `ruff` - Linter
- `mypy` - Type checker

## Verify Installation

Check that PDF Sentinel is installed correctly:

```bash
pdf-sentinel --version
```

You should see output like:

```
pdf-sentinel version 2.0.0
```

## Next Steps

- **[Quick Start](quick-start.md)** - Get up and running in minutes
- **[Configuration](configuration.md)** - Customize PDF Sentinel for your needs
- **[CLI Usage](../user-guide/cli-usage.md)** - Learn the command-line interface
