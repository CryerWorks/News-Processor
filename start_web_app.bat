@echo off
echo =========================================================
echo    Mundus News Digest Generator - Web Application
echo =========================================================
echo.
echo Starting the web-based news processing application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo WARNING: .env file not found!
    echo.
    echo Please create a .env file with your OpenAI API key:
    echo OPENAI_API_KEY=your_api_key_here
    echo.
    pause
)

REM Check if key dependencies are installed
echo Checking dependencies...
python -c "import flask, flask_socketio, pandas, openai" >nul 2>&1
if %errorlevel% neq 0 (
    echo Missing dependencies detected. Installing...
    pip install -r requirements.txt
    echo.
    echo Dependencies installed successfully!
    echo.
) else (
    echo All dependencies are installed. Ready to start!
    echo.
)

REM Start the application
echo Starting web server...
echo Your browser will open automatically to http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo =========================================================
python run_web_app.py

pause
