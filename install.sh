#!/bin/bash

# CoreX Installation Script

echo "🚀 Installing CoreX - Django Scaffolding Framework"

# Check if Python 3.9+ is installed
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Error: Python 3.9 or higher is required. Found: $python_version"
    exit 1
fi

echo "✅ Python $python_version found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed"
    exit 1
fi

echo "✅ pip3 found"

# Install CoreX
echo "📦 Installing CoreX..."

# Install in development mode
pip3 install -e .

# Or install directly
# pip3 install .

echo "✅ CoreX installed successfully!"

# Test installation
echo "🧪 Testing installation..."
if command -v corex &> /dev/null; then
    echo "✅ CoreX command is available"
    corex --version
else
    echo "⚠️  CoreX command not found in PATH"
    echo "Try running: python3 -m corex --version"
fi

echo ""
echo "🎉 CoreX installation complete!"
echo ""
echo "📖 Usage examples:"
echo "  corex new myproject --auth=jwt --ui=tailwind"
echo "  corex app blog --type=blog --auth=jwt --ui=tailwind"
echo "  corex runserver"
echo ""
echo "📚 For more information, visit: https://github.com/ramazon07-cmd/corex"
