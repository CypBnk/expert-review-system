#!/bin/bash
# Run Both Backend and Frontend Servers

echo "========================================"
echo "Expert Review Analysis System V2"
echo "Starting Full Stack"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found"
    echo "Please run setup.sh first"
    exit 1
fi

echo "[INFO] Starting backend server..."
source venv/bin/activate
python3 api_server.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

echo "[INFO] Starting frontend server..."
python3 -m http.server 8000 &
FRONTEND_PID=$!

# Wait for frontend to start
sleep 2

echo "[INFO] Opening browser..."
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8000 2>/dev/null &
elif command -v open &> /dev/null; then
    open http://localhost:8000 2>/dev/null &
fi

echo ""
echo "========================================"
echo "Both servers are running!"
echo "========================================"
echo ""
echo "Backend API:  http://localhost:5000"
echo "Frontend:     http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "Servers stopped"
    exit 0
}

# Set trap to catch Ctrl+C
trap cleanup INT TERM

# Wait indefinitely
wait
