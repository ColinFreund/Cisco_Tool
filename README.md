# Cisco Device Manager

A web-based Cisco network device management tool that allows you to connect to Cisco switches and routers via both console cable and network connections, then manage them through a user-friendly interface similar to Cisco SDM (Security Device Manager).

## Features

- Connect to Cisco devices via network (SSH, Telnet, HTTP, HTTPS)
- Connect to Cisco devices via console cable with configurable serial port settings
- Manage and monitor device interfaces
- Configure routing settings
- Set up VPN tunnels
- Access interactive terminal for direct CLI commands
- View, edit and compare device configurations
- Track connection history and command logs

## Architecture

The application consists of two main components:

1. **Python Backend**: A Flask API server that handles communication with Cisco devices using libraries like Netmiko and PySerial
2. **Next.js Frontend**: A React-based web interface that provides a modern, responsive user interface

## Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- Cisco devices or emulator (like Cisco Packet Tracer, GNS3, or EVE-NG)

## Installation

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Set up the Python environment and start the backend server:
   ```
   start_server.bat
   ```

   This will:
   - Create a virtual environment
   - Install required Python packages
   - Start the Flask API server on port 5000

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies and start the development server:
   ```
   start_frontend.bat
   ```

   This will:
   - Install necessary Node.js packages
   - Start the Next.js development server on port 3000

3. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

## Configuration

### Backend Configuration

- The backend server configuration can be adjusted in `backend/.env`
- Database settings can be modified in `backend/app.py`

### Frontend Configuration

- API endpoint URLs can be configured in `frontend/.env.local`

## Usage

1. Start both the backend and frontend servers
2. Open your browser and navigate to http://localhost:3000
3. Use the dashboard to manage your Cisco devices
4. Connect to devices using either network or console connection
5. Configure and monitor your devices through the web interface

## Development

### Backend Development

- Python source files are in the `backend` directory
- API endpoints are defined in `backend/app.py`
- Cisco command parsers are in `backend/utils.py`

### Frontend Development

- React components are in the `frontend/src/components` directory
- Pages are in the `frontend/src/app` directory
- API services are in the `frontend/src/lib/api.ts`

## License

This software is provided as-is without warranty.