import React, { useState, useEffect } from 'react';
import Head from 'next/head';
import { 
  getDevices, 
  addDevice, 
  connectNetwork, 
  sendCommand, 
  disconnect,
  getDeviceInfo
} from '../lib/api';

export default function Home() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [connectionId, setConnectionId] = useState(null);
  const [command, setCommand] = useState('');
  const [commandOutput, setCommandOutput] = useState('');
  const [newDevice, setNewDevice] = useState({
    name: '',
    ip_address: '',
    device_type: 'router',
    protocol: 'ssh',
    username: '',
    password: ''
  });

  // Fetch devices on component mount
  useEffect(() => {
    fetchDevices();
  }, []);

  const fetchDevices = async () => {
    setLoading(true);
    try {
      const data = await getDevices();
      setDevices(data);
      setError(null);
    } catch (err) {
      console.error('Error fetching devices:', err);
      setError('Failed to load devices. Is the backend server running?');
    } finally {
      setLoading(false);
    }
  };

  const handleDeviceSelect = (device) => {
    setSelectedDevice(device);
    setConnectionId(null);
    setCommandOutput('');
  };

  const handleConnect = async () => {
    if (!selectedDevice) return;

    setLoading(true);
    try {
      const data = await connectNetwork(selectedDevice.id, selectedDevice.protocol);
      setConnectionId(data.connection_id);
      setCommandOutput(`Connected to ${selectedDevice.name} (${selectedDevice.ip_address}) via ${selectedDevice.protocol}\\n`);
      setError(null);
    } catch (err) {
      console.error('Error connecting to device:', err);
      setError('Failed to connect to device');
    } finally {
      setLoading(false);
    }
  };

  const handleDisconnect = async () => {
    if (!connectionId) return;

    setLoading(true);
    try {
      await disconnect(connectionId);
      setConnectionId(null);
      setCommandOutput(prev => `${prev}\\nDisconnected from device\\n`);
      setError(null);
    } catch (err) {
      console.error('Error disconnecting from device:', err);
      setError('Failed to disconnect from device');
    } finally {
      setLoading(false);
    }
  };

  const handleSendCommand = async () => {
    if (!connectionId || !command) return;

    setLoading(true);
    try {
      const data = await sendCommand(connectionId, command);
      setCommandOutput(prev => `${prev}\\n\\n> ${command}\\n${data.output}`);
      setCommand('');
      setError(null);
    } catch (err) {
      console.error('Error sending command:', err);
      setError('Failed to send command');
    } finally {
      setLoading(false);
    }
  };

  const handleAddDevice = async (e) => {
    e.preventDefault();
    
    setLoading(true);
    try {
      await addDevice(newDevice);
      setNewDevice({
        name: '',
        ip_address: '',
        device_type: 'router',
        protocol: 'ssh',
        username: '',
        password: ''
      });
      await fetchDevices();
      setError(null);
    } catch (err) {
      console.error('Error adding device:', err);
      setError('Failed to add device');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setNewDevice(prev => ({ ...prev, [name]: value }));
  };

  const getDeviceInfo = async () => {
    if (!connectionId) return;

    try {
      const response = await fetch(`http://localhost:5000/api/device_info/${connectionId}`);
      
      if (response.ok) {
        const data = await response.json();
        const formattedInfo = `
Device Information:
------------------
IOS Version: ${data.ios_version}
Total Interfaces: ${data.total_interfaces}
Interfaces Up: ${data.interfaces_up}
        `;
        setCommandOutput(prev => `${prev}\\n\\n${formattedInfo}`);
      } else {
        const data = await response.json();
        setError(`Failed to get device info: ${data.error}`);
      }
    } catch (error) {
      console.error('Error getting device info:', error);
      setError('Error retrieving device information');
    }
  };

  // Common Cisco commands
  const commonCommands = [
    { name: 'Show Version', cmd: 'show version' },
    { name: 'Show Interfaces', cmd: 'show interfaces' },
    { name: 'Show IP Interfaces', cmd: 'show ip interface brief' },
    { name: 'Show Running Config', cmd: 'show running-config' },
    { name: 'Show CDP Neighbors', cmd: 'show cdp neighbors' }
  ];

  const runCommonCommand = (cmd) => {
    setCommand(cmd);
  };

  return (
    <div className="container">
      <Head>
        <title>Cisco Device Manager</title>
        <meta name="description" content="Manage your Cisco devices" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <header className="header">
        <h1>Cisco Device Manager</h1>
      </header>

      {error && (
        <div style={{ padding: '1rem', backgroundColor: '#ffebee', color: '#d32f2f', marginBottom: '1rem', borderRadius: '5px' }}>
          {error}
        </div>
      )}

      <div style={{ display: 'flex', gap: '2rem' }}>
        {/* Left column - Device list and add device form */}
        <div style={{ flex: 1 }}>
          <div className="card">
            <h2>Devices</h2>
            {loading && <p>Loading...</p>}
            
            {devices.length === 0 ? (
              <p>No devices found. Add a device to get started.</p>
            ) : (
              <ul style={{ listStyle: 'none', padding: 0 }}>
                {devices.map(device => (
                  <li 
                    key={device.id} 
                    style={{ 
                      padding: '0.5rem', 
                      margin: '0.25rem 0', 
                      backgroundColor: selectedDevice?.id === device.id ? '#e3f2fd' : 'transparent',
                      borderRadius: '5px',
                      cursor: 'pointer'
                    }}
                    onClick={() => handleDeviceSelect(device)}
                  >
                    <strong>{device.name}</strong> ({device.ip_address}) - {device.device_type}
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="card">
            <h2>Add New Device</h2>
            <form onSubmit={handleAddDevice} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div>
                <label htmlFor="name">Device Name:</label>
                <input 
                  type="text" 
                  id="name" 
                  name="name" 
                  value={newDevice.name} 
                  onChange={handleInputChange}
                  required
                  style={{ width: '100%', padding: '0.5rem' }}
                />
              </div>
              
              <div>
                <label htmlFor="ip_address">IP Address:</label>
                <input 
                  type="text" 
                  id="ip_address" 
                  name="ip_address" 
                  value={newDevice.ip_address} 
                  onChange={handleInputChange}
                  required
                  style={{ width: '100%', padding: '0.5rem' }}
                />
              </div>
              
              <div>
                <label htmlFor="device_type">Device Type:</label>
                <select 
                  id="device_type" 
                  name="device_type" 
                  value={newDevice.device_type} 
                  onChange={handleInputChange}
                  style={{ width: '100%', padding: '0.5rem' }}
                >
                  <option value="router">Router</option>
                  <option value="switch">Switch</option>
                  <option value="firewall">Firewall</option>
                </select>
              </div>
              
              <div>
                <label htmlFor="protocol">Protocol:</label>
                <select 
                  id="protocol" 
                  name="protocol" 
                  value={newDevice.protocol} 
                  onChange={handleInputChange}
                  style={{ width: '100%', padding: '0.5rem' }}
                >
                  <option value="ssh">SSH</option>
                  <option value="telnet">Telnet</option>
                </select>
              </div>
              
              <div>
                <label htmlFor="username">Username:</label>
                <input 
                  type="text" 
                  id="username" 
                  name="username" 
                  value={newDevice.username} 
                  onChange={handleInputChange}
                  style={{ width: '100%', padding: '0.5rem' }}
                />
              </div>
              
              <div>
                <label htmlFor="password">Password:</label>
                <input 
                  type="password" 
                  id="password" 
                  name="password" 
                  value={newDevice.password} 
                  onChange={handleInputChange}
                  style={{ width: '100%', padding: '0.5rem' }}
                />
              </div>
              
              <button 
                type="submit" 
                className="button" 
                disabled={loading}
                style={{ marginTop: '1rem' }}
              >
                Add Device
              </button>
            </form>
          </div>
        </div>

        {/* Right column - Terminal and commands */}
        <div style={{ flex: 2 }}>
          <div className="card">
            <h2>Device Control</h2>
            
            <div style={{ marginBottom: '1rem' }}>
              <strong>Selected Device:</strong> {selectedDevice ? `${selectedDevice.name} (${selectedDevice.ip_address})` : 'None'}
            </div>
            
            <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
              <button 
                className="button" 
                onClick={handleConnect} 
                disabled={!selectedDevice || connectionId || loading}
              >
                Connect
              </button>
              
              <button 
                className="button" 
                onClick={handleDisconnect} 
                disabled={!connectionId || loading}
                style={{ backgroundColor: '#f44336' }}
              >
                Disconnect
              </button>
              
              <button 
                className="button" 
                onClick={getDeviceInfo} 
                disabled={!connectionId || loading}
                style={{ backgroundColor: '#4caf50' }}
              >
                Get Device Info
              </button>
            </div>
            
            {/* Terminal output */}
            <div className="terminal" style={{ marginBottom: '1rem' }}>
              {commandOutput || 'Terminal ready. Connect to a device to start...'}
            </div>
            
            {/* Command input */}
            <div style={{ display: 'flex', gap: '1rem' }}>
              <input 
                type="text" 
                value={command} 
                onChange={(e) => setCommand(e.target.value)} 
                placeholder="Enter Cisco IOS command..." 
                disabled={!connectionId}
                style={{ flex: 1, padding: '0.5rem' }}
                onKeyPress={(e) => e.key === 'Enter' && handleSendCommand()}
              />
              
              <button 
                className="button" 
                onClick={handleSendCommand} 
                disabled={!connectionId || !command || loading}
              >
                Send
              </button>
            </div>
            
            {/* Common commands */}
            <div style={{ marginTop: '1rem' }}>
              <h3>Common Commands</h3>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem' }}>
                {commonCommands.map((cmd, index) => (
                  <button 
                    key={index} 
                    onClick={() => runCommonCommand(cmd.cmd)} 
                    disabled={!connectionId}
                    style={{ 
                      padding: '0.25rem 0.5rem', 
                      fontSize: '0.875rem',
                      border: '1px solid #ccc',
                      borderRadius: '3px',
                      backgroundColor: '#f5f5f5',
                      cursor: connectionId ? 'pointer' : 'not-allowed'
                    }}
                  >
                    {cmd.name}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}