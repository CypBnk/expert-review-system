#!/bin/bash
# Expert Review Analysis System V2 - Unix/Mac Setup Script

echo "========================================"
echo "Expert Review Analysis System V2"
echo "Local Test Environment Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[1/4] Python found"
python3 --version

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "[ERROR] pip is not installed"
    exit 1
fi

echo "[2/4] pip found"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "[3/4] Creating virtual environment..."
    python3 -m venv venv
    echo "Virtual environment created"
else
    echo "[3/4] Virtual environment already exists"
fi

echo ""
echo "[4/4] Installing dependencies..."
echo "This may take a few minutes..."
echo ""

# Activate virtual environment and install dependencies
source venv/bin/activate

# Install basic dependencies first (lighter)
pip install flask flask-cors pandas numpy --quiet

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "OPTIONAL: To install full ML dependencies (torch, transformers)"
echo "Run: pip install -r requirements.txt"
echo "Note: This will download ~2GB of packages"
echo ""
echo "To start the server, run: ./start_server.sh"
echo ""
