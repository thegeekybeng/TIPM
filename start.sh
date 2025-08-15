#!/bin/bash

# TIPM FastAPI Startup Script
echo "🚀 Starting TIPM FastAPI Backend..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Change to API directory
echo "📁 Changing to API directory..."
cd api

# Start FastAPI server
echo "🌐 Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port $PORT
