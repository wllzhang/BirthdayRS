# Contributing

Thank you for your interest in contributing to BirthdayRS!

## How to Contribute

### Reporting Bugs

1. Check existing issues on GitHub
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment information (Python version, OS, etc.)

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

```bash
# Clone the repository
git clone https://github.com/wllzhang/BirthdayRS.git
cd BirthdayRS

# Install dependencies
uv sync

# Or using pip
pip install -r requirements.txt
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run with HTML coverage report
pytest --cov=src --cov-report=html
```

## Code Style

This project uses [flake8](https://flake8.pycqa.org/) for code style checking.

```bash
# Run flake8
flake8 .

# Configuration is in .flake8
# - Max line length: 100
# - Ignores: E501, W503
```

## Documentation

Documentation is built with [Sphinx](https://www.sphinx-doc.org/) and automatically deployed to GitHub Pages.

```bash
# Build documentation locally
cd docs
sphinx-build -b html . _build

# Or using make (if available)
make html
```

## Project Structure

```
BirthdayRS/
├── src/
│   ├── core/                   # Core business logic
│   ├── notification/           # Notification senders
│   └── main.py                # Application entry point
├── tests/                     # Test suite
├── templates/                 # Jinja2 email templates
├── docs/                      # Documentation
├── .github/workflows/         # GitHub Actions workflows
└── config.example.yml         # Configuration example
```

## Coding Guidelines

1. Follow PEP 8 style guide
2. Write tests for new features
3. Update documentation for API changes
4. Use meaningful commit messages
5. Keep pull requests focused and concise

## License

By contributing to BirthdayRS, you agree that your contributions will be licensed under the MIT License.
