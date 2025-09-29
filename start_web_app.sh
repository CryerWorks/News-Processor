#!/bin/bash

echo "========================================================="
echo "   Mundus News Digest Generator - Web Application"
echo "========================================================="
echo ""
echo "Starting the web-based news processing application..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found!"
    echo ""
    echo "Please create a .env file with your OpenAI API key:"
    echo "OPENAI_API_KEY=your_api_key_here"
    echo ""
    read -p "Press Enter to continue..."
fi

# Check if key dependencies are installed
echo "Checking dependencies..."
if ! python3 -c "import flask, flask_socketio, pandas, openai" >/dev/null 2>&1; then
    echo "Missing dependencies detected. Installing..."
    pip3 install -r requirements.txt
    echo ""
    echo "Dependencies installed successfully!"
    echo ""
else
    echo "All dependencies are installed. Ready to start!"
    echo ""
fi

# Start the application
echo "Starting web server..."
echo "Your browser will open automatically to http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "========================================================="
python3 run_web_app.py
