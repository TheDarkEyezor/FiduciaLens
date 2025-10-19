#!/bin/bash

echo "🚀 FiduciaLens Setup Script"
echo "=========================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+"
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+"
    exit 1
fi
echo "✅ Node.js found: $(node --version)"

echo ""
echo "📦 Installing dependencies..."
echo ""

# Setup contracts
echo "1️⃣ Setting up smart contracts..."
cd contracts
python3 -m pip install -r requirements.txt
echo "✅ Contract dependencies installed"
echo ""

# Setup backend
echo "2️⃣ Setting up backend..."
cd ../backend
python3 -m pip install -r requirements.txt
if [ ! -f .env ]; then
    cp .env.example .env
    echo "📝 Created .env file - please configure it!"
fi
echo "✅ Backend dependencies installed"
echo ""

# Setup frontend
echo "3️⃣ Setting up frontend..."
cd ../frontend
if command -v npm &> /dev/null; then
    npm install
    if [ ! -f .env ]; then
        cp .env.example .env
        echo "📝 Created .env file - please configure it!"
    fi
    echo "✅ Frontend dependencies installed"
else
    echo "⚠️  npm not found, skipping frontend setup"
fi
echo ""

cd ..
echo "✨ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Compile & deploy the smart contract:"
echo "   cd contracts && python3 loan_pool.py && python3 deploy.py"
echo ""
echo "2. Configure backend/.env with your settings"
echo ""
echo "3. Start the backend:"
echo "   cd backend && python3 main.py"
echo ""
echo "4. Start the frontend (in a new terminal):"
echo "   cd frontend && npm run dev"
echo ""
echo "🎉 Happy hacking!"
