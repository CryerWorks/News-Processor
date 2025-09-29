@echo off
echo =========================================================
echo    Mundus News Digest Generator - Dependency Setup
echo =========================================================
echo.
echo This script will install all required Python dependencies.
echo Run this once before using the application.
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from python.org
    pause
    exit /b 1
)

echo Installing Python dependencies...
echo.
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo =========================================================
    echo SUCCESS: All dependencies installed successfully!
    echo.
    echo You can now run the application using:
    echo - start_web_app.bat (Windows)
    echo - python run_web_app.py (Direct)
    echo =========================================================
) else (
    echo.
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
)

pause
