@echo off
title AI Resume Analyzer & Job Matcher - Full Stack Launcher
color 0A
cls

echo ======================================================================
echo           AI RESUME ANALYZER & JOB MATCHER - LAUNCHER
echo ======================================================================
echo.

:: 1. Setup Backend Environment if needed
echo [*] Checking Backend virtual environment...
if not exist "backend\venv" (
    echo [*] Creating Python virtual environment...
    py -m venv backend\venv 2>nul || python -m venv backend\venv
)

echo [*] Installing / verifying Backend dependencies...
call backend\venv\Scripts\pip install -q -r backend\requirements.txt

:: 2. Verify & Initialize MySQL Database
echo [*] Initializing MySQL Database and Demo Data...
backend\venv\Scripts\python backend\init_db.py --seed
if %errorlevel% neq 0 (
    echo.
    echo [!] MySQL connection failed.
    echo [!] Please make sure Apache and MySQL are running in XAMPP Control Panel.
    echo.
    pause
    exit /b 1
)

:: 3. Setup Frontend dependencies if needed
echo [*] Checking Frontend dependencies...
if not exist "frontend\node_modules" (
    echo [*] Installing frontend npm packages...
    cd frontend && call npm install && cd ..
)

:: 4. Launch Backend & Frontend Servers
echo.
echo [*] Starting Flask Backend Server (http://127.0.0.1:5000)...
start "AI Resume Matcher - Backend" cmd /k "cd backend && venv\Scripts\python app.py"

echo [*] Starting Vite Frontend Server (http://localhost:5173)...
start "AI Resume Matcher - Frontend" cmd /k "cd frontend && npm run dev"

:: 5. Open Browser
echo [*] Waiting for servers to initialize...
timeout /t 3 >nul

echo [*] Opening application in default browser...
start http://localhost:5173

echo.
echo ======================================================================
echo   SUCCESS! Full stack application is now running:
echo   - Frontend: http://localhost:5173
echo   - Backend:  http://127.0.0.1:5000
echo   - Database: XAMPP MySQL (ai_resume_matcher)
echo.
echo   Demo Accounts:
echo   - Student: alex.student@example.com / Student@123
echo   - Company: hr@technova.com / Company@123
echo   - Admin:   admin@airesume.com / Admin@123
echo ======================================================================
echo.
pause
