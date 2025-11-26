#!/bin/bash
# Start the Expert Review Analysis System V2 Backend Server

echo "========================================"
echo "Expert Review Analysis System V2"
echo "Starting Backend Server"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found"
    echo "Please run setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

echo "[INFO] Starting Flask API server on http://localhost:5000"
echo "[INFO] Press Ctrl+C to stop the server"
echo ""
echo "========================================"
echo ""

# Start the Flask server from backend directory
python3 ./backend/api_server.py
