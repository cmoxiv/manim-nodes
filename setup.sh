#!/bin/bash
set -e

echo "=========================================="
echo "Manim Nodes - Setup Script"
echo "=========================================="
echo

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

# Check Node version
echo "Checking Node.js version..."
node_version=$(node --version 2>&1)
echo "Node.js version: $node_version"

echo
echo "=========================================="
echo "Backend Setup"
echo "=========================================="
echo

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv ~/.venvs/pg

# Activate virtual environment
echo "Activating virtual environment..."
source ~/.venvs/pg/bin/activate

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

echo
echo "=========================================="
echo "Frontend Setup"
echo "=========================================="
echo

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo
echo "To start the development servers:"
echo
echo "Terminal 1 (Backend):"
echo "  source ~/.venvs/pg/bin/activate"
echo "  uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
echo
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo
echo "Then open http://localhost:5173 in your browser"
echo
echo "Alternatively, use Docker:"
echo "  docker-compose up -d"
echo "  Open http://localhost:8000"
echo
