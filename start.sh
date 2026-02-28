#!/bin/bash

echo "================================"
echo "Industrial Monitoring Dashboard"
echo "================================"
echo ""

echo "[1/4] Starting PostgreSQL..."
docker-compose up -d
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to start PostgreSQL"
    echo "Please make sure Docker is running"
    exit 1
fi
echo "PostgreSQL started successfully!"
echo ""

echo "[2/4] Setting up Backend..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate
pip install -r requirements.txt --quiet
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi
echo "Backend setup complete!"
echo ""

echo "[3/4] Setting up Frontend..."
cd ../frontend
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi
echo "Frontend setup complete!"
echo ""

echo "[4/4] Starting services..."
echo ""
echo "===================================="
echo " Dashboard will be ready at:"
echo " http://localhost:3000"
echo ""
echo " API Documentation at:"
echo " http://localhost:8000/docs"
echo "===================================="
echo ""

# Start backend in background
echo "Starting Backend..."
cd ../backend
source venv/bin/activate
python main.py &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 3

# Start frontend in background
echo "Starting Frontend..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "All services started!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for interrupt
trap "echo ''; echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; docker-compose down; echo 'Services stopped.'; exit 0" INT

# Keep script running
wait
