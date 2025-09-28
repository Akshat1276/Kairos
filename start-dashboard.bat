@echo off
echo Starting Kairos Frontend Dashboard...
echo.

echo [1/3] Installing Python dependencies...
if exist venv (
    echo Using existing virtual environment...
    call venv\Scripts\activate
    pip install -r requirements.txt
) else (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
)

echo.
echo [2/3] Installing Frontend dependencies...
cd frontend
call npm install

echo.
echo [3/3] Starting servers...
echo.
echo Starting API Server (Port 8000)...
start "Kairos API" cmd /k "cd .. && call venv\Scripts\activate && python api_server.py"

timeout /t 5 /nobreak > nul

echo Starting Frontend (Port 3000)...
start "Kairos Frontend" cmd /k "npm run dev"

echo.
echo ======================================
echo Kairos Dashboard is starting up!
echo ======================================
echo Frontend: http://localhost:3000
echo API Server: http://localhost:8000
echo ======================================
echo.
echo Both servers are running in separate windows.
echo Close this window when you're done.
echo.

pause