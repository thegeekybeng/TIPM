#!/bin/bash

# TIPM FastAPI Startup Script
echo "🚀 Starting TIPM FastAPI Backend..."

# Change to API directory
echo "📁 Changing to API directory..."
cd api

# Start FastAPI server
echo "🌐 Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port $PORT
