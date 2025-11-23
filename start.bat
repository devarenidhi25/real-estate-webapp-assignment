@echo off
REM Quick Start Script for Real Estate Chatbot

echo.
echo ========================================
echo Real Estate Chatbot - Quick Start
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    exit /b 1
)

echo [1/4] Starting Django Backend...
echo.
cd backend
start "Django Backend" cmd /k "python manage.py runserver"
echo Backend starting on http://localhost:8000

timeout /t 3 /nobreak

echo.
echo [2/4] Installing Frontend Dependencies...
echo.
cd ..\frontend
if not exist node_modules (
    call npm install
)

echo.
echo [3/4] Starting React Frontend...
echo.
start "React Frontend" cmd /k "npm start"
echo Frontend starting on http://localhost:3000

echo.
echo ========================================
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo ========================================
echo.
echo Press any key to close this window...
pause >nul
