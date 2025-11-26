@echo off
REM Run Both Backend and Frontend Servers

echo ========================================
echo Expert Review Analysis System V2
echo Starting Full Stack
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found
    echo Please run setup.bat first
    pause
    exit /b 1
)

echo [INFO] Starting backend server in new window...
start "API Server - Port 5000" cmd /k "call venv\Scripts\activate.bat && python .\\backend\\api_server.py"

REM Wait a moment for backend to start
timeout /t 3 /nobreak >nul

echo [INFO] Starting frontend server in new window...
start "Frontend Server - Port 8000" cmd /k "cd frontend && python -m http.server 8000"

REM Wait a moment for frontend to start
timeout /t 2 /nobreak >nul

echo [INFO] Opening browser...
start http://localhost:8000

echo.
echo ========================================
echo Both servers are running!
echo ========================================
echo.
echo Backend API:  http://localhost:5000
echo Frontend:     http://localhost:8000
echo.
echo Close this window or the server windows to stop
echo.
pause
