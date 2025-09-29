#!/bin/bash

echo "========================================================="
echo "   Mundus News Digest Generator - Dependency Setup"
echo "========================================================="
echo ""
echo "This script will install all required Python dependencies."
echo "Run this once before using the application."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Installing Python dependencies..."
echo ""
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "========================================================="
    echo "SUCCESS: All dependencies installed successfully!"
    echo ""
    echo "You can now run the application using:"
    echo "- ./start_web_app.sh (macOS/Linux)"
    echo "- python3 run_web_app.py (Direct)"
    echo "========================================================="
else
    echo ""
    echo "ERROR: Failed to install dependencies"
    echo "Please check your internet connection and try again"
fi

read -p "Press Enter to continue..."
