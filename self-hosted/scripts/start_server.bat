@echo off
REM Start the Expert Review Analysis System V2 Backend Server

echo ========================================
echo Expert Review Analysis System V2
echo Starting Backend Server
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo [INFO] Starting Flask API server on http://localhost:5000
echo [INFO] Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

REM Start the Flask server
python .\\backend\\api_server.py

pause
