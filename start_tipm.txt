#!/bin/bash

# TIPM v2.0 Startup Script
# Starts both FastAPI backend and React frontend

echo "🚀 Starting TIPM v2.0 - Clean Architecture"
echo "=========================================="

# Check if virtual environment exists
if [ ! -d "tipm_env" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv tipm_env
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source tipm_env/bin/activate

# Install/update dependencies
echo "📦 Installing/updating Python dependencies..."
pip install -r requirements.txt

# Check if FastAPI is installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📥 Installing FastAPI..."
    pip install fastapi uvicorn
fi

# Start FastAPI backend in background
echo "🔌 Starting FastAPI backend on port 8000..."
python api/main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Backend started successfully"
else
    echo "❌ Backend failed to start"
    exit 1
fi

# Check if Node.js dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node.js dependencies..."
    npm install
fi

# Start React frontend
echo "🌐 Starting React frontend on port 3000..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🎉 TIPM v2.0 is starting up!"
echo "=========================================="
echo "📊 Backend API: http://localhost:8000"
echo "🌐 Frontend: http://localhost:3000"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Shutting down TIPM..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ TIPM stopped"
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Wait for both processes
wait
