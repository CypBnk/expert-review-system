@echo off
REM Start Frontend HTTP Server

echo ========================================
echo Expert Review Analysis System V2
echo Starting Frontend Server
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed
    pause
    exit /b 1
)

echo [INFO] Starting HTTP server on http://localhost:8000
echo [INFO] Opening browser...
echo [INFO] Press Ctrl+C to stop the server
echo.
echo ========================================
echo.

REM Start Python HTTP server and open browser
start http://localhost:8000
cd frontend && python -m http.server 8000

pause
