@echo off
echo ================================
echo Industrial Monitoring Dashboard
echo ================================
echo.

echo [1/4] Starting PostgreSQL...
docker-compose up -d
if %errorlevel% neq 0 (
    echo ERROR: Failed to start PostgreSQL
    echo Please make sure Docker Desktop is running
    pause
    exit /b 1
)
echo PostgreSQL started successfully!
echo.

echo [2/4] Setting up Backend...
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt --quiet
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
)
echo Backend setup complete!
echo.

echo [3/4] Setting up Frontend...
cd ..\frontend
if not exist node_modules (
    echo Installing dependencies...
    call npm install
)
echo Frontend setup complete!
echo.

echo [4/4] Starting services...
echo.
echo ====================================
echo  Dashboard will be ready at:
echo  http://localhost:3000
echo.
echo  API Documentation at:
echo  http://localhost:8000/docs
echo ====================================
echo.
echo Starting Backend (Terminal 1)...
start cmd /k "cd backend && venv\Scripts\activate && python main.py"

timeout /t 3 /nobreak >nul

echo Starting Frontend (Terminal 2)...
start cmd /k "cd frontend && npm run dev"

echo.
echo All services started!
echo Press any key to stop all services...
pause >nul

echo Stopping services...
docker-compose down
taskkill /FI "WINDOWTITLE eq *python main.py*" /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq *npm run dev*" /F >nul 2>&1
echo Services stopped.
