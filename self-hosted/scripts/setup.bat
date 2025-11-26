@echo off
REM Expert Review Analysis System V2 - Windows Setup Script

echo ========================================
echo Expert Review Analysis System V2
echo Local Test Environment Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Python found
python --version

REM Check if pip is available
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] pip is not installed
    pause
    exit /b 1
)

echo [2/4] pip found
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [3/4] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created
) else (
    echo [3/4] Virtual environment already exists
)

echo.
echo [4/4] Installing dependencies...
echo This may take a few minutes...
echo.

REM Activate virtual environment and install dependencies
call venv\Scripts\activate.bat

REM Install basic dependencies first (lighter)
pip install flask flask-cors pandas numpy --quiet

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo OPTIONAL: To install full ML dependencies (torch, transformers)
echo Run: pip install -r requirements.txt
echo Note: This will download ~2GB of packages
echo.
echo To start the server, run: start_server.bat
echo.
pause
