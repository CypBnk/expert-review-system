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

REM Install dependencies from requirements.txt
echo Installing Python dependencies from backend\requirements.txt...
echo This may take several minutes and download ~2GB...
echo.
pip install -r backend\requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

REM Copy .env.example if .env doesn't exist
if not exist ".env" (
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo.
        echo [INFO] Created .env from .env.example
        echo You can edit .env to customize configuration
    )
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start all services: .\scripts\start_all.bat
echo To start backend only: .\scripts\start_server.bat
echo To start frontend only: .\scripts\start_frontend.bat
echo.
pause
