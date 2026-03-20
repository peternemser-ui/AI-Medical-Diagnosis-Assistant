@echo off
echo ==========================================
echo    AI Medical Diagnosis Assistant
echo ==========================================
echo.

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://python.org/
    pause
    exit /b 1
)

REM Navigate to project directory
pushd "%~dp0"

REM Install backend dependencies if needed
echo Installing backend dependencies...
pushd backend
pip install -r requirements.txt >nul 2>&1
popd

REM Install frontend dependencies if needed
echo Installing frontend dependencies...
pushd frontend
if not exist "node_modules" (
    npm install
)
popd

REM Start Backend Server
echo Starting backend server...
pushd backend
start "AI Health Backend" cmd /k "uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
popd

REM Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 3 /nobreak >nul

REM Start Frontend Server
echo Starting frontend server...
pushd frontend
start "AI Health Frontend" cmd /k "npm run dev"
popd

echo.
echo ==========================================
echo    AI Health Assistant is starting...
echo ==========================================
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000  
echo API Docs: http://localhost:8000/docs
echo ==========================================
echo.
echo Press any key to close this launcher...
pause >nul
