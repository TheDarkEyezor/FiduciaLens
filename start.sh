#!/bin/bash

# FiduciaLens Development Startup Script
# This script handles PATH issues and starts all services

echo "🚀 FiduciaLens Development Environment"
echo "======================================"
echo ""

# Setup Node.js path
export PATH="$HOME/.nvm/versions/node/v22.17.0/bin:$PATH"

# Check if backend is configured
if [ ! -f backend/.env ]; then
    echo "⚠️  Backend not configured!"
    echo "   Run: cp backend/.env.example backend/.env"
    echo "   Then edit backend/.env with your APP_ID"
    exit 1
fi

# Check if frontend is configured  
if [ ! -f frontend/.env ]; then
    echo "⚠️  Frontend not configured!"
    echo "   Run: cp frontend/.env.example frontend/.env"
    echo "   Then edit frontend/.env with your APP_ID"
    exit 1
fi

echo "✅ Configuration files found"
echo ""

# Ask what to start
echo "What would you like to start?"
echo "1) Backend only"
echo "2) Frontend only"
echo "3) Both (recommended)"
read -p "Choice (1-3): " choice

case $choice in
    1)
        echo ""
        echo "🖥️  Starting backend..."
        cd backend && python3 main.py
        ;;
    2)
        echo ""
        echo "🎨 Starting frontend..."
        cd frontend && npm run dev
        ;;
    3)
        echo ""
        echo "🎯 Starting both services..."
        echo ""
        echo "Backend will start in this terminal."
        echo "Frontend will open in a new terminal window."
        echo ""
        
        # Start frontend in new terminal
        osascript -e 'tell app "Terminal" to do script "cd '$(pwd)'/frontend && export PATH=\"$HOME/.nvm/versions/node/v22.17.0/bin:$PATH\" && npm run dev"'
        
        # Start backend in current terminal
        echo "🖥️  Backend starting..."
        sleep 2
        cd backend && python3 main.py
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
