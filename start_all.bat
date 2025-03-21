@echo off
echo Starting Cisco Device Manager...

REM Start the backend server in a new window
start cmd /k "cd backend && start_server.bat"

REM Wait a moment for the backend to initialize
timeout /t 5

REM Start the frontend server in a new window
start cmd /k "cd frontend && start_frontend.bat"

echo Both servers started!
echo.
echo Backend running at: http://localhost:5000
echo Frontend running at: http://localhost:3000
echo.
echo Open your browser and navigate to http://localhost:3000 to access the application
echo.