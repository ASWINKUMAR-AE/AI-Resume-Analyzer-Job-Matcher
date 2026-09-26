# AI Resume Analyzer & Job Matcher - PowerShell Unified Launcher
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "          AI RESUME ANALYZER & JOB MATCHER - LAUNCHER" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path

# 1. Test MySQL Port
Write-Host "[*] Checking XAMPP MySQL connectivity on localhost:3306..." -ForegroundColor Yellow
$mysqlCheck = Test-NetConnection -ComputerName localhost -Port 3306 -WarningAction SilentlyContinue
if (-not $mysqlCheck.TcpTestSucceeded) {
    Write-Host "[!] MySQL connection failed on localhost:3306!" -ForegroundColor Red
    Write-Host "[!] Please ensure MySQL is started from XAMPP Control Panel." -ForegroundColor Yellow
    exit 1
}

# 2. Virtual environment setup
$venvPython = Join-Path $Root "backend\venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) {
    Write-Host "[*] Creating Python virtual environment in backend/venv..." -ForegroundColor Yellow
    py -m venv (Join-Path $Root "backend\venv")
}

Write-Host "[*] Verifying Python dependencies..." -ForegroundColor Yellow
& (Join-Path $Root "backend\venv\Scripts\pip.exe") install -q -r (Join-Path $Root "backend\requirements.txt")

# 3. Database Initialization
Write-Host "[*] Checking and seeding MySQL Database..." -ForegroundColor Yellow
& $venvPython (Join-Path $Root "backend\init_db.py") --seed

# 4. Frontend node_modules check
$nodeModules = Join-Path $Root "frontend\node_modules"
if (-not (Test-Path $nodeModules)) {
    Write-Host "[*] Installing frontend npm dependencies..." -ForegroundColor Yellow
    Set-Location (Join-Path $Root "frontend")
    npm install
    Set-Location $Root
}

# 5. Start Backend Process
Write-Host "[*] Launching Backend Flask Server on port 5000..." -ForegroundColor Green
Start-Process -FilePath "cmd.exe" -ArgumentList "/k cd /d `"$Root\backend`" && venv\Scripts\python app.py" -WindowStyle Normal

# 6. Start Frontend Process
Write-Host "[*] Launching Frontend Vite Server on port 5173..." -ForegroundColor Green
Start-Process -FilePath "cmd.exe" -ArgumentList "/k cd /d `"$Root\frontend`" && npm run dev" -WindowStyle Normal

# 7. Open Browser
Start-Sleep -Seconds 3
Start-Process "http://localhost:5173"

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  SUCCESS: Both Frontend & Backend are running!" -ForegroundColor Green
Write-Host "  - Frontend: http://localhost:5173" -ForegroundColor White
Write-Host "  - Backend:  http://127.0.0.1:5000" -ForegroundColor White
Write-Host "  - Database: XAMPP MySQL (ai_resume_matcher)" -ForegroundColor White
Write-Host "======================================================================" -ForegroundColor Cyan
