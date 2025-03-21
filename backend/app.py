import os
import logging
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

# Setup logging
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Database setup
DB_PATH = os.path.join(os.path.dirname(__file__), 'cisco_devices.db')

def init_db():
    """Initialize the SQLite database with tables if they don't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create devices table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        ip_address TEXT,
        device_type TEXT,
        model TEXT,
        protocol TEXT DEFAULT 'ssh',
        username TEXT,
        password TEXT,
        enable_password TEXT,
        last_connected TEXT,
        is_active BOOLEAN DEFAULT 1
    )
    ''')
    
    # Create connections table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS connections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_id INTEGER,
        connection_type TEXT,
        start_time TEXT,
        end_time TEXT,
        status TEXT,
        FOREIGN KEY (device_id) REFERENCES devices (id)
    )
    ''')
    
    # Create command_logs table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS command_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        connection_id INTEGER,
        command TEXT,
        output TEXT,
        timestamp TEXT,
        FOREIGN KEY (connection_id) REFERENCES connections (id)
    )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

# Initialize database on startup
init_db()

# API Routes
@app.route('/api/devices', methods=['GET'])
def get_devices():
    """Get all devices from the database"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM devices WHERE is_active = 1')
    devices = [dict(row) for row in cursor.fetchall()]
    
    conn.close()
    return jsonify(devices)

@app.route('/api/devices', methods=['POST'])
def add_device():
    """Add a new device to the database"""
    data = request.json
    required_fields = ['name', 'ip_address', 'device_type', 'protocol']
    
    # Validate required fields
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO devices (name, ip_address, device_type, model, protocol, username, password, enable_password)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        data['name'], 
        data['ip_address'], 
        data['device_type'], 
        data.get('model', ''),
        data['protocol'], 
        data.get('username', ''), 
        data.get('password', ''), 
        data.get('enable_password', '')
    ))
    
    device_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return jsonify({"id": device_id, "message": "Device added successfully"}), 201

@app.route('/api/connect/network', methods=['POST'])
def connect_network():
    """Connect to a device via network (SSH/Telnet)"""
    data = request.json
    
    # Validate request
    if not all(key in data for key in ['device_id', 'protocol']):
        return jsonify({"error": "Missing required fields"}), 400
    
    # In a real application, you would establish a connection to the device here
    # For this example, we'll just record the connection in the database
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Record connection start
    current_time = datetime.now().isoformat()
    cursor.execute('''
    INSERT INTO connections (device_id, connection_type, start_time, status)
    VALUES (?, ?, ?, ?)
    ''', (data['device_id'], data['protocol'], current_time, 'active'))
    
    connection_id = cursor.lastrowid
    
    # Update device last_connected timestamp
    cursor.execute('''
    UPDATE devices SET last_connected = ? WHERE id = ?
    ''', (current_time, data['device_id']))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        "connection_id": connection_id,
        "status": "connected",
        "message": f"Connected to device via {data['protocol']}"
    })

@app.route('/api/send_command/<int:connection_id>', methods=['POST'])
def send_command(connection_id):
    """Send a command to a connected device"""
    data = request.json
    
    if 'command' not in data:
        return jsonify({"error": "Command is required"}), 400
    
    command = data['command']
    
    # In a real application, you would send the command to the device and get the response
    # For this example, we'll simulate a command response
    
    # Example simulated response
    if command == 'show version':
        output = """Cisco IOS Software, C2600 Software (C2600-IPBASE-M), Version 12.4(25d), RELEASE SOFTWARE (fc1)
Technical Support: http://www.cisco.com/techsupport
Copyright (c) 1986-2010 by Cisco Systems, Inc.
Compiled Wed 18-Aug-10 10:49 by prod_rel_team

ROM: System Bootstrap, Version 12.2(8r) [fcz 8r], RELEASE SOFTWARE (fc1)

Router uptime is 2 days, 5 hours, 37 minutes
System returned to ROM by power-on
System image file is "flash:c2600-ipbase-mz.124-25d.bin"
"""
    elif command == 'show interfaces':
        output = """FastEthernet0/0 is up, line protocol is up 
  Hardware is AmdFE, address is 0001.42c3.f401 (bia 0001.42c3.f401)
  Internet address is 192.168.1.1/24
  MTU 1500 bytes, BW 100000 Kbit/sec, DLY 100 usec, 
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full-duplex, 100Mb/s, 100BaseTX/FX
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:08, output 00:00:05, output hang never
  Last clearing of "show interface" counters never
"""
    elif command == 'show ip interface brief':
        output = """Interface                  IP-Address      OK? Method Status                Protocol
FastEthernet0/0            192.168.1.1     YES NVRAM  up                    up      
FastEthernet0/1            unassigned      YES NVRAM  administratively down down    
Serial0/0                  unassigned      YES NVRAM  administratively down down    
Serial0/1                  unassigned      YES NVRAM  administratively down down    
Loopback0                  10.1.1.1        YES NVRAM  up                    up      
"""
    elif command == 'show running-config':
        output = """Building configuration...

Current configuration : 1112 bytes
!
version 12.4
service timestamps debug datetime msec
service timestamps log datetime msec
no service password-encryption
!
hostname Router1
!
boot-start-marker
boot-end-marker
!
enable secret 5 $1$rE8r$jL0Y3DAqz1M.hBBbV0lgg.
!
no aaa new-model
memory-size iomem 5
!
ip cef
!
interface FastEthernet0/0
 description LAN Interface
 ip address 192.168.1.1 255.255.255.0
 duplex auto
 speed auto
!
interface Serial0/0
 no ip address
 shutdown
!
ip route 0.0.0.0 0.0.0.0 FastEthernet0/0
!
access-list 101 permit ip any any
!
line con 0
line aux 0
line vty 0 4
 password cisco
 login
!
end
"""
    else:
        output = f"Command '{command}' not recognized or simulated in this example."
    
    # Record command in the database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO command_logs (connection_id, command, output, timestamp)
    VALUES (?, ?, ?, ?)
    ''', (connection_id, command, output, datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        "command": command,
        "output": output,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/disconnect/<int:connection_id>', methods=['POST'])
def disconnect(connection_id):
    """Disconnect from a device"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if connection exists
    cursor.execute('SELECT * FROM connections WHERE id = ? AND status = "active"', (connection_id,))
    connection = cursor.fetchone()
    
    if not connection:
        conn.close()
        return jsonify({"error": "Connection not found or already closed"}), 400
    
    # Update connection end time and status
    cursor.execute('''
    UPDATE connections SET end_time = ?, status = 'closed'
    WHERE id = ?
    ''', (datetime.now().isoformat(), connection_id))
    
    conn.commit()
    conn.close()
    
    return jsonify({
        "status": "disconnected",
        "message": "Successfully disconnected from device"
    })

@app.route('/api/device_info/<int:connection_id>', methods=['GET'])
def get_device_info(connection_id):
    """Get device information based on previous commands"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Check if connection exists
    cursor.execute('''
    SELECT connections.*, devices.name, devices.model, devices.device_type 
    FROM connections 
    JOIN devices ON connections.device_id = devices.id
    WHERE connections.id = ?
    ''', (connection_id,))
    
    connection = cursor.fetchone()
    
    if not connection:
        conn.close()
        return jsonify({"error": "Connection not found"}), 404
    
    # Get stored command outputs to extract information
    cursor.execute('''
    SELECT command, output FROM command_logs
    WHERE connection_id = ? AND (command LIKE 'show version' OR command LIKE 'show interfaces')
    ''', (connection_id,))
    
    command_logs = cursor.fetchall()
    conn.close()
    
    # Extract device information
    device_info = {
        "name": connection['name'],
        "model": connection['model'] or "Unknown",
        "device_type": connection['device_type'],
        "ios_version": "Unknown",
        "total_interfaces": 0,
        "interfaces_up": 0
    }
    
    for log in command_logs:
        if 'show version' in log['command']:
            # Extract version information from output
            for line in log['output'].splitlines():
                if 'Version' in line:
                    device_info['ios_version'] = line.split('Version')[1].split(',')[0].strip()
                    break
        
        if 'show interfaces' in log['command']:
            # Count interfaces
            interfaces = 0
            up_interfaces = 0
            for line in log['output'].splitlines():
                if "Ethernet" in line or "Serial" in line or "GigabitEthernet" in line:
                    interfaces += 1
                    if "is up" in line:
                        up_interfaces += 1
            
            device_info['total_interfaces'] = interfaces
            device_info['interfaces_up'] = up_interfaces
    
    return jsonify(device_info)

# Main entry point
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)