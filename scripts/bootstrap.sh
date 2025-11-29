#!/bin/bash

# CoreX Bootstrap Script for Unix-like systems (macOS/Linux)

set -e

echo "🚀 CoreX Bootstrap Script"
echo "========================"

# Check if running on supported OS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Running on macOS"
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "🐧 Running on Linux"
    OS="linux"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

# Check for required tools
echo "🔍 Checking for required tools..."

REQUIRED_TOOLS=("python3" "pip3" "git" "node" "npm")
MISSING_TOOLS=()

for tool in "${REQUIRED_TOOLS[@]}"; do
    if ! command -v "$tool" &> /dev/null; then
        MISSING_TOOLS+=("$tool")
    else
        echo "✅ $tool found"
    fi
done

if [ ${#MISSING_TOOLS[@]} -ne 0 ]; then
    echo "❌ Missing tools: ${MISSING_TOOLS[*]}"
    
    if [[ "$OS" == "macos" ]]; then
        echo "💡 Install missing tools with Homebrew:"
        echo "   brew install ${MISSING_TOOLS[*]}"
    elif [[ "$OS" == "linux" ]]; then
        echo "💡 Install missing tools with your package manager:"
        if command -v apt &> /dev/null; then
            echo "   sudo apt update && sudo apt install ${MISSING_TOOLS[*]}"
        elif command -v yum &> /dev/null; then
            echo "   sudo yum install ${MISSING_TOOLS[*]}"
        elif command -v dnf &> /dev/null; then
            echo "   sudo dnf install ${MISSING_TOOLS[*]}"
        fi
    fi
    
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check Python version
echo "🐍 Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d'.' -f2)

if [[ $PYTHON_MAJOR -lt 3 ]] || [[ $PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 8 ]]; then
    echo "❌ Python 3.8 or higher is required. Found: $PYTHON_VERSION"
    exit 1
else
    echo "✅ Python $PYTHON_VERSION found"
fi

# Install CoreX
echo "📦 Installing CoreX..."
pip3 install -e .

# Install GUI dependencies
echo "🖥️  Installing GUI dependencies..."
cd gui/corex-gui
npm install

# Create virtual environment for template testing
echo "🧪 Creating virtual environment for template testing..."
cd ../..
python3 -m venv corex-test-env
source corex-test-env/bin/activate
pip install -r requirements.txt

echo "✅ CoreX bootstrap completed successfully!"
echo ""
echo "To get started:"
echo "1. Activate the test environment: source corex-test-env/bin/activate"
echo "2. Run the GUI: cd gui/corex-gui && npm run dev"
echo "3. Run the CoreX agent: python -m corex.agent.server"
echo "4. Create a new project: corex new myproject --template ecommerce"