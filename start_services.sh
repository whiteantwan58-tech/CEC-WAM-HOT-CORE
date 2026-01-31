#!/bin/bash
# start_services.sh
# -----------------
# Starts all CEC-WAM services including chart automation and API server

set -e

echo "============================================"
echo "Starting CEC-WAM Services"
echo "============================================"

# Set working directory
cd "$(dirname "$0")"

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Error: Python is not installed"
    exit 1
fi

# Install dependencies if needed
echo "Checking dependencies..."
pip install -r requirements.txt -q --user || echo "Note: Some packages may already be installed"

# Run initial chart automation
echo ""
echo "Running initial chart automation..."
python chart_automation.py

# Start API server in background
echo ""
echo "Starting API server on port 5000..."
python api_server.py &
API_PID=$!
echo "API server started (PID: $API_PID)"

# Start simple HTTP server for frontend in background
echo ""
echo "Starting frontend server on port 8000..."
python -m http.server 8000 &
FRONTEND_PID=$!
echo "Frontend server started (PID: $FRONTEND_PID)"

echo ""
echo "============================================"
echo "Services started successfully!"
echo "============================================"
echo "Frontend: http://localhost:8000"
echo "API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"
echo "============================================"

# Function to handle cleanup
cleanup() {
    echo ""
    echo "Stopping services..."
    kill $API_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    echo "Services stopped."
    exit 0
}

# Set up trap to catch Ctrl+C
trap cleanup SIGINT SIGTERM

# Wait for background processes
wait
