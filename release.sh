#!/bin/bash
# CoreX Release Script v1.0.0
# 
# This script handles the release process for CoreX
# Usage: ./release.sh [version]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Get version
VERSION=${1:-"1.0.0"}

log_info "Starting CoreX release process for version $VERSION"

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ] || [ ! -d "corex" ]; then
    log_error "This script must be run from the CoreX root directory"
    exit 1
fi

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    log_error "Git working directory is not clean. Please commit or stash your changes."
    exit 1
fi

# Update version in pyproject.toml
log_info "Updating version in pyproject.toml..."
sed -i.bak "s/version = \".*\"/version = \"$VERSION\"/" pyproject.toml
rm pyproject.toml.bak

# Update version in CLI
log_info "Updating version in CLI..."
sed -i.bak "s/version=\".*\"/version=\"$VERSION\"/" corex/cli.py
rm corex/cli.py.bak

# Run tests
log_info "Running tests..."
if command -v poetry &> /dev/null; then
    poetry run pytest -v
else
    python -m pytest -v
fi

# Run linting
log_info "Running code quality checks..."
if command -v poetry &> /dev/null; then
    poetry run black --check .
    poetry run isort --check-only .
    poetry run flake8 .
else
    black --check .
    isort --check-only .
    flake8 .
fi

log_success "All tests and quality checks passed!"

# Build package
log_info "Building package..."
if command -v poetry &> /dev/null; then
    poetry build
else
    python -m build
fi

log_success "Package built successfully!"

# Create git tag
log_info "Creating git tag v$VERSION..."
git add pyproject.toml corex/cli.py
git commit -m "Bump version to $VERSION"
git tag -a "v$VERSION" -m "Release version $VERSION"

log_info "Package is ready for release!"
echo
echo "Next steps:"
echo "1. Push to repository: git push origin main --tags"
echo "2. Upload to PyPI: poetry publish (or twine upload dist/*)"
echo "3. Create GitHub release with changelog"
echo
echo "To upload to PyPI:"
echo "  poetry publish"
echo
echo "To upload to Test PyPI first:"
echo "  poetry config repositories.testpypi https://test.pypi.org/legacy/"
echo "  poetry publish -r testpypi"

log_success "Release script completed successfully!"