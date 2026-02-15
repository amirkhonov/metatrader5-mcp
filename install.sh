#!/bin/bash
# Quick installation script for MetaTrader5-MCP
# This script sets up the environment and installs the package

set -e

echo "================================================"
echo "MetaTrader5-MCP Installation Script"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.10"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "Error: Python $REQUIRED_VERSION or higher is required. Found: $PYTHON_VERSION"
    exit 1
fi

echo "✓ Python $PYTHON_VERSION detected"
echo ""

# Check if Poetry is installed
echo "Checking for Poetry..."
if command -v poetry &> /dev/null; then
    echo "✓ Poetry detected"
    USE_POETRY=true
else
    echo "Poetry not found. Will use pip instead."
    USE_POETRY=false
fi
echo ""

# Create virtual environment if needed
if [ "$USE_POETRY" = false ]; then
    echo "Creating virtual environment..."
    if [ ! -d "venv" ]; then
        python3 -m venv venv
        echo "✓ Virtual environment created"
    else
        echo "✓ Virtual environment already exists"
    fi

    # Activate virtual environment
    source venv/bin/activate
    echo "✓ Virtual environment activated"
    echo ""
fi

# Install dependencies
echo "Installing dependencies..."
if [ "$USE_POETRY" = true ]; then
    poetry install
    echo "✓ Dependencies installed via Poetry"
else
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install -e .
    echo "✓ Dependencies installed via pip"
fi
echo ""

# Copy example environment file if .env doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created"
    echo "⚠️  Please edit .env with your MT5 credentials"
else
    echo "✓ .env file already exists"
fi
echo ""

# Install pre-commit hooks (optional)
read -p "Install pre-commit hooks for development? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    pip install pre-commit
    pre-commit install
    echo "✓ Pre-commit hooks installed"
fi
echo ""

echo "================================================"
echo "Installation Complete! 🎉"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your MT5 credentials:"
echo "   nano .env"
echo ""
echo "2. Run the server:"
if [ "$USE_POETRY" = true ]; then
    echo "   poetry run metatrader5-mcp"
else
    echo "   source venv/bin/activate  # if not already activated"
    echo "   metatrader5-mcp"
fi
echo ""
echo "3. Or with command line arguments:"
if [ "$USE_POETRY" = true ]; then
    echo "   poetry run metatrader5-mcp --login 12345 --password secret --server MetaQuotes-Demo"
else
    echo "   metatrader5-mcp --login 12345 --password secret --server MetaQuotes-Demo"
fi
echo ""
echo "For help, see README.md or run:"
echo "   metatrader5-mcp --help"
echo ""
