# Contributing to deproto

Thank you for your interest in contributing to deproto! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. Fork and clone the repository:
```bash
git clone https://github.com/mrdebugger/deproto.git
cd deproto
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Include docstrings for classes and public methods
- Keep lines under 80 characters when possible

## Testing

All new features and bug fixes should include tests. The project uses pytest for testing:

```bash
# Run all tests
pytest tests/

# Run with coverage
coverage run -m pytest tests/
coverage report
```

## Development Workflow

1. Create a new branch for your feature/fix:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and commit them:
```bash
git add .
git commit -m "Description of your changes"
```

3. Ensure all tests pass and add new tests if needed
4. Update documentation if necessary
5. Push your changes and create a pull request

## Pull Request Guidelines

When submitting a pull request:

1. Describe the changes and why they're needed
2. Include any relevant issue numbers
3. Ensure all tests pass
4. Update CHANGELOG.md following the existing format
5. Add yourself to CONTRIBUTORS.md if you're not already listed

## Project Structure

- `deproto/` - Main package source code
- `tests/` - Test suite
- `examples/` - Example usage scripts
- `assets/` - Project assets (icons, images)

## Version Control

The project follows [Semantic Versioning](https://semver.org/). Version numbers are in the format MAJOR.MINOR.PATCH:

- MAJOR: Incompatible API changes
- MINOR: Backwards-compatible new features
- PATCH: Backwards-compatible bug fixes

## Documentation

- Update README.md for user-facing changes
- Add docstrings for new classes and methods
- Include example usage in docstrings
- Update type hints where applicable

## Release Process

1. Update version number in `setup.py`
2. Update CHANGELOG.md
3. Create a new release on GitHub
4. Build and upload to PyPI:
```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Getting Help

- Open an issue for bugs or feature requests
- Join discussions in existing issues
- Contact the maintainer: [Ijaz Ur Rahim](https://ijazurrahim.com)

## License

By contributing to deproto, you agree that your contributions will be licensed under the MIT License. See [LICENSE](LICENSE) for details.