#!/bin/bash
# Start Frontend HTTP Server

echo "========================================"
echo "Expert Review Analysis System V2"
echo "Starting Frontend Server"
echo "========================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    exit 1
fi

echo "[INFO] Starting HTTP server on http://localhost:8000"
echo "[INFO] Press Ctrl+C to stop the server"
echo ""
echo "========================================"
echo ""

# Open browser (works on most systems)
if command -v xdg-open &> /dev/null; then
    xdg-open http://localhost:8000 2>/dev/null &
elif command -v open &> /dev/null; then
    open http://localhost:8000 2>/dev/null &
fi

# Start Python HTTP server
python3 -m http.server 8000
