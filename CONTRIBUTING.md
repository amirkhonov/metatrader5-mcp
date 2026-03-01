# Contributing to MetaTrader5-MCP

Thank you for your interest in contributing to MetaTrader5-MCP! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## Getting Started

### Prerequisites

- Python 3.10 or higher
- MetaTrader 5 terminal (for testing)
- Git

### Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/metatrader5-mcp.git
   cd metatrader5-mcp
   ```

2. **Install dependencies:**

   Using Poetry (recommended):
   ```bash
   poetry install
   ```

   Or using pip:
   ```bash
   pip install -r requirements-dev.txt
   pip install -e .
   ```

3. **Set up pre-commit hooks:**
   ```bash
   pre-commit install
   ```

4. **Copy environment template:**
   ```bash
   cp .env.example .env
   # Edit .env with your MT5 credentials
   ```

## Development Workflow

### Creating a Branch

Create a new branch for your work:
```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### Making Changes

1. **Write clean, documented code:**
   - Follow PEP 8 style guidelines
   - Add docstrings to all functions and classes
   - Use type hints
   - Keep functions focused and small

2. **Test your changes:**
   ```bash
   pytest
   ```

3. **Format your code:**
   ```bash
   black .
   ruff check --fix .
   ```

4. **Run pre-commit checks:**
   ```bash
   pre-commit run --all-files
   ```

### Commit Messages

Write clear, descriptive commit messages:
- Use present tense ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Add detailed description if needed

Example:
```
Add support for custom timeframes

- Implement timeframe conversion function
- Update documentation with examples
- Add tests for edge cases
```

### Pull Requests

1. **Update your fork:**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push your changes:**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request:**
   - Provide a clear description of the changes
   - Reference any related issues
   - Include screenshots for UI changes
   - Ensure all CI checks pass

## Code Style

### Python Style

- Follow PEP 8
- Use Black for formatting (line length: 88)
- Use Ruff for linting
- Use type hints for all function parameters and returns
- Add docstrings using Google style

Example:
```python
def mt5_get_symbol_info(symbol: str) -> dict[str, Any]:
    """
    Get information about a trading symbol.

    Args:
        symbol: The trading symbol (e.g., "EURUSD").

    Returns:
        Dictionary containing symbol information including spread,
        digits, tick size, etc.

    Raises:
        ValueError: If symbol is empty or invalid.
        RuntimeError: If MT5 is not initialized.
    """
    if not symbol:
        raise ValueError("Symbol cannot be empty")
    # Implementation
```

### Documentation

- Keep README.md up to date
- Update CHANGELOG.md for notable changes
- Add examples for new features
- Document breaking changes clearly

## Testing

### Writing Tests

- Place tests in a `tests/` directory
- Name test files as `test_*.py`
- Use descriptive test names
- Test edge cases and error conditions
- Mock MT5 connections for unit tests

Example:
```python
def test_mt5_get_symbol_info_success(mock_mt5):
    """Test successful retrieval of symbol information."""
    mock_mt5.symbol_info.return_value = {"spread": 2, "digits": 5}
    result = mt5_get_symbol_info("EURUSD")
    assert result["spread"] == 2
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=metatrader5_mcp --cov-report=html

# Run specific test file
pytest tests/test_connection.py

# Run specific test
pytest tests/test_connection.py::test_mt5_get_symbol_info_success
```

## Reporting Bugs

### Before Reporting

- Check if the bug has already been reported
- Verify it's reproducible on the latest version
- Collect relevant information (logs, error messages, etc.)

### Bug Report Template

```markdown
**Describe the bug**
A clear description of the bug.

**To Reproduce**
Steps to reproduce:
1. Initialize with...
2. Call tool...
3. See error...

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment:**
- OS: [e.g., Windows 10]
- Python version: [e.g., 3.11]
- MT5 version: [e.g., 5.0.4]
- Package version: [e.g., 0.1.0]

**Logs**
```
Paste relevant logs here
```

**Additional context**
Any other relevant information.
```

## Suggesting Features

### Feature Request Template

```markdown
**Is your feature request related to a problem?**
A clear description of the problem.

**Describe the solution you'd like**
What you want to happen.

**Describe alternatives you've considered**
Other approaches you've thought about.

**Additional context**
Any other relevant information.
```

## Security

If you discover a security vulnerability:
1. **DO NOT** open a public issue
2. Email the maintainers privately
3. Include details about the vulnerability
4. Wait for a response before disclosure

## Recognition

Contributors will be recognized in:
- CHANGELOG.md for their contributions
- GitHub contributors page

## Questions?

Feel free to:
- Open a GitHub Discussion
- Ask in existing issues
- Reach out to maintainers

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to MetaTrader5-MCP! 🎉
