@echo off
echo Starting Cisco Device Manager Frontend...

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo Node.js is not installed or not in PATH. Please install Node.js 14 or higher.
    exit /b 1
)

REM Install dependencies if not already installed
if not exist node_modules (
    echo Installing dependencies...
    npm install
)

REM Start the development server
echo Starting Next.js development server...
npm run dev