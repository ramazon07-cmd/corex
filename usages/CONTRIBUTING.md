# Contributing to CoreX

Thank you for your interest in contributing to CoreX. This document explains how to get started, coding standards, testing, and the process for submitting pull requests.

- Clone the repository and install dependencies:

```bash
git clone https://github.com/ramazon07-cmd/corex.git
cd corex
python -m pip install --upgrade pip
pip install -e .
```

- Run tests:

```bash
pytest
```

- Code style:
  - Use Black for formatting
  - Run flake8 for linting

- Writing templates:
  - Use Jinja2 syntax
  - Ensure no unresolved placeholders remain in generated files
  - Add tests when changing generators

- Submit a pull request with a clear description of changes and link to any related issues.
