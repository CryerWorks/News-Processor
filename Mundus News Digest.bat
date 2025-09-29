@echo off
title Mundus News Digest Generator
color 0B

REM Mundus News Digest Generator - Double-Click Launcher for Windows
REM This file can be double-clicked to start the application

echo.
echo 🚀 Starting Mundus News Digest Generator...
echo =========================================================
echo    Welcome to Mundus News Digest Generator
echo =========================================================
echo.

REM Get current directory
echo 📍 Location: %~dp0
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: Python is not installed
    echo.
    echo Please install Python 3.8 or higher:
    echo 1. Visit https://www.python.org/downloads/
    echo 2. Download Python for Windows
    echo 3. Run the installer ^(IMPORTANT: Check "Add Python to PATH"^)
    echo.
    echo Press any key to open Python download page...
    pause >nul
    start https://www.python.org/downloads/
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python found: %PYTHON_VERSION%

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo ⚠️  SETUP REQUIRED: OpenAI API Key Missing
    echo.
    echo To use this application, you need an OpenAI API key.
    echo.
    echo Steps to get your API key:
    echo 1. Visit https://platform.openai.com/api-keys
    echo 2. Sign in or create an account
    echo 3. Click 'Create new secret key'
    echo 4. Copy the key that starts with 'sk-'
    echo.
    set /p "setup_choice=Would you like to open the API key page now? (y/n): "
    
    if /i "%setup_choice%"=="y" (
        echo.
        echo Opening OpenAI API key page...
        start https://platform.openai.com/api-keys
        echo.
        set /p "api_key=Please paste your OpenAI API key here: "
        echo OPENAI_API_KEY=!api_key! > .env
        echo.
        echo ✅ API key saved successfully!
        echo.
    ) else (
        echo.
        echo You can create a .env file manually with:
        echo OPENAI_API_KEY=your_api_key_here
        echo.
        echo Press any key to continue anyway...
        pause >nul
    )
)

REM Check if key dependencies are installed
echo 🔍 Checking dependencies...
python -c "import flask, flask_socketio, pandas, openai" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo 📦 Installing required components ^(this may take a few minutes^)...
    echo Please wait while we set up the application...
    echo.
    
    pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo.
        echo ✅ Setup completed successfully!
        echo.
    ) else (
        echo.
        echo ❌ Installation failed. Please check your internet connection.
        echo Press any key to exit...
        pause >nul
        exit /b 1
    )
) else (
    echo ✅ All components ready!
)

echo.
echo 🌐 Starting web server...
echo.
echo Your web browser will open automatically in a few seconds.
echo If it doesn't open, manually visit: http://localhost:5000
echo.
echo 💡 TIP: Keep this window open while using the application.
echo 💡 To stop the server, close this window or press Ctrl+C.
echo.
echo =========================================================

REM Start the Python application
python run_web_app.py

REM If we get here, the app has stopped
echo.
echo 👋 Mundus News Digest Generator has stopped.
echo Press any key to close this window...
pause >nul
