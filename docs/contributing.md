# Contributing to PDF Sentinel

Thank you for your interest in contributing to PDF Sentinel! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project follows a simple code of conduct: be respectful, be constructive, and help make PDF Sentinel better for everyone.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in [Issues](https://github.com/ai4genxers/pdf-sentinel/issues)
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Your environment (OS, Python version, PDF Sentinel version)
   - Sample PDF if relevant (ensure no sensitive data)

### Suggesting Features

1. Check [existing feature requests](https://github.com/ai4genxers/pdf-sentinel/issues?q=is%3Aissue+label%3Aenhancement)
2. Create a new issue with:
   - Clear use case
   - Proposed solution
   - Alternatives considered
   - Willingness to implement

### Pull Requests

1. **Fork the repository**

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set up development environment**
   ```bash
   cd pdf-sentinel
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -e ".[dev]"
   ```

4. **Make your changes**
   - Write clear, documented code
   - Follow existing code style
   - Add tests for new features
   - Update documentation as needed

5. **Run tests and checks**
   ```bash
   # Format code
   black src/ tests/

   # Lint
   ruff check src/ tests/

   # Type check
   mypy src/

   # Run tests
   pytest
   ```

6. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

   Follow [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat:` new feature
   - `fix:` bug fix
   - `docs:` documentation
   - `test:` testing
   - `refactor:` code refactoring
   - `chore:` maintenance

7. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a Pull Request on GitHub

## Development Guidelines

### Code Style

- Follow PEP 8
- Use type hints
- Write docstrings for public APIs
- Keep functions focused and small
- Use meaningful variable names

### Testing

- Write tests for new features
- Maintain or improve test coverage
- Test edge cases
- Use fixtures for common setup

### Documentation

- Update README for user-facing changes
- Add docstrings to new code
- Update CHANGELOG.md
- Add examples if helpful

### Converter Implementation

When adding a new PDF converter:

1. Create a new file in `src/pdf_sentinel/converters/`
2. Implement the `BaseConverter` interface
3. Add tests in `tests/test_converters.py`
4. Update README and documentation
5. Add to `ConversionEngine` enum in `config.py`

Example:
```python
from pdf_sentinel.converters.base import BaseConverter

class MyConverter(BaseConverter):
    @property
    def name(self) -> str:
        return "MyConverter"

    def convert(self, pdf_path: Path, output_path: Path) -> Tuple[bool, Optional[str]]:
        # Implementation
        pass
```

## Project Structure

```
pdf-sentinel/
├── src/pdf_sentinel/       # Source code
│   ├── converters/          # PDF conversion engines
│   ├── config.py            # Configuration
│   ├── watcher.py           # Main watcher class
│   ├── handlers.py          # Event handlers
│   └── cli.py               # CLI interface
├── tests/                   # Tests
├── docs/                    # Documentation
├── .github/                 # GitHub Actions
└── pyproject.toml           # Project configuration
```

## Getting Help

- Open an [issue](https://github.com/ai4genxers/pdf-sentinel/issues)
- Check existing [documentation](https://github.com/ai4genxers/pdf-sentinel/tree/main/docs)
- Read the [architecture documentation](https://github.com/ai4genxers/pdf-sentinel/blob/main/docs/architecture.md)

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes
- README (for significant contributions)

Thank you for contributing to PDF Sentinel! 🎉
