#!/bin/bash

# Mundus News Digest Generator - Double-Click Launcher for macOS
# This file can be double-clicked to start the application

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Clear the terminal for a clean look
clear

echo "🚀 Starting Mundus News Digest Generator..."
echo "========================================================="
echo "   Welcome to Mundus News Digest Generator"
echo "========================================================="
echo ""
echo "📍 Location: $SCRIPT_DIR"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed"
    echo ""
    echo "Please install Python 3.8 or higher:"
    echo "1. Visit https://www.python.org/downloads/"
    echo "2. Download Python for macOS"
    echo "3. Run the installer"
    echo ""
    echo "Press any key to exit..."
    read -n 1
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  SETUP REQUIRED: OpenAI API Key Missing"
    echo ""
    echo "To use this application, you need an OpenAI API key."
    echo ""
    echo "Steps to get your API key:"
    echo "1. Visit https://platform.openai.com/api-keys"
    echo "2. Sign in or create an account"
    echo "3. Click 'Create new secret key'"
    echo "4. Copy the key that starts with 'sk-'"
    echo ""
    echo "Would you like to enter your API key now? (y/n)"
    read -n 1 response
    echo ""
    
    if [[ $response =~ ^[Yy]$ ]]; then
        echo ""
        echo "Please paste your OpenAI API key:"
        read -s api_key
        echo "OPENAI_API_KEY=$api_key" > .env
        echo ""
        echo "✅ API key saved successfully!"
        echo ""
    else
        echo ""
        echo "You can create a .env file manually with:"
        echo "OPENAI_API_KEY=your_api_key_here"
        echo ""
        echo "Press any key to continue anyway..."
        read -n 1
    fi
fi

# Check if key dependencies are installed
echo "🔍 Checking dependencies..."
if ! python3 -c "import flask, flask_socketio, pandas, openai" >/dev/null 2>&1; then
    echo ""
    echo "📦 Installing required components (this may take a few minutes)..."
    echo "Please wait while we set up the application..."
    echo ""
    
    # Install dependencies with user feedback
    if pip3 install -r requirements.txt; then
        echo ""
        echo "✅ Setup completed successfully!"
        echo ""
    else
        echo ""
        echo "❌ Installation failed. Please check your internet connection."
        echo "Press any key to exit..."
        read -n 1
        exit 1
    fi
else
    echo "✅ All components ready!"
fi

echo ""
echo "🌐 Starting web server..."
echo ""
echo "Your web browser will open automatically in a few seconds."
echo "If it doesn't open, manually visit: http://localhost:5000"
echo ""
echo "💡 TIP: Keep this window open while using the application."
echo "💡 To stop the server, press Ctrl+C in this window."
echo ""
echo "========================================================="

# Start the Python application
python3 run_web_app.py

# If we get here, the app has stopped
echo ""
echo "👋 Mundus News Digest Generator has stopped."
echo "Press any key to close this window..."
read -n 1
