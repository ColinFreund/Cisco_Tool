@echo off
echo Starting Cisco Device Manager Backend Server...

REM Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8 or higher.
    exit /b 1
)

REM Check if virtual environment exists, if not create it
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install requirements if not already installed
echo Installing dependencies...
pip install -r requirements.txt

REM Start the server
echo Starting server...
python start.py

REM Deactivate virtual environment on exit
call venv\Scripts\deactivate.bat