# Cisco Device Manager Backend

This is the Python backend server for the Cisco Device Manager application. It provides APIs for connecting to and managing Cisco routers and switches via both network (SSH/Telnet) and console connections.

## Features

- Connect to Cisco devices via SSH and Telnet
- Connect to Cisco devices via Serial Console connection
- Execute CLI commands and parse responses
- Manage device configurations
- Store connection history and command logs
- RESTful API for frontend integration

## Requirements

- Python 3.8 or higher
- Dependencies listed in requirements.txt

## Installation

### Windows

1. Make sure Python 3.8+ is installed and available in your PATH
2. Simply run the `start_server.bat` script which will:
   - Create a virtual environment if it doesn't exist
   - Install dependencies
   - Start the server

### Manual Installation

1. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Start the server:
   ```
   python start.py
   ```

## API Endpoints

### Devices

- `GET /api/devices` - Get all devices
- `POST /api/devices` - Add a new device
- `GET /api/devices/<device_id>` - Get a specific device by ID

### Connections

- `GET /api/connections` - Get connection history
- `POST /api/connect/network` - Connect to a device via network (SSH/Telnet)
- `POST /api/connect/console` - Connect to a device via console cable
- `POST /api/send_command/<connection_id>` - Send a command to a connected device
- `POST /api/disconnect/<connection_id>` - Disconnect from a device
- `GET /api/device_info/<connection_id>` - Get device information (version, interfaces, etc.)

## Database

The application uses SQLite by default, with the database file stored in `cisco_devices.db`. The following tables are created:

- `devices` - Stored device information
- `connections` - Connection history
- `command_logs` - Command history

## License

This software is provided as-is without warranty. See LICENSE for details.