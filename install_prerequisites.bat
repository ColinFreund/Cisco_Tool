@echo off
echo Checking prerequisites for Cisco Device Manager...
echo.

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please download and install Python 3.8 or higher from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation.
    goto :ERROR
) else (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set pyver=%%i
    echo [OK] %pyver% is installed
)

REM Check if Node.js is installed
where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Node.js is not installed or not in PATH.
    echo Please download and install Node.js 14 or higher from:
    echo https://nodejs.org/
    goto :ERROR
) else (
    for /f "tokens=*" %%i in ('node --version') do set nodever=%%i
    echo [OK] Node.js %nodever% is installed
)

REM Check if pip is installed
where pip >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] pip is not installed or not in PATH.
    echo Please ensure your Python installation includes pip.
    goto :ERROR
) else (
    echo [OK] pip is installed
)

REM Check if npm is installed
where npm >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] npm is not installed or not in PATH.
    echo Please ensure your Node.js installation includes npm.
    goto :ERROR
) else (
    for /f "tokens=*" %%i in ('npm --version') do set npmver=%%i
    echo [OK] npm %npmver% is installed
)

echo.
echo All prerequisites are installed!
echo.
echo To start the application:
echo 1. Run 'start_all.bat' to start both the backend and frontend servers
echo 2. Open your browser and navigate to http://localhost:3000
echo.
echo Press any key to exit...
pause > nul
exit /b 0

:ERROR
echo.
echo Please install the missing prerequisites and try again.
echo.
echo Press any key to exit...
pause > nul
exit /b 1