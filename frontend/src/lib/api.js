/**
 * API Client for interacting with the Cisco Manager Backend
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000/api';

/**
 * Get all devices
 * @returns {Promise<Array>} List of devices
 */
export async function getDevices() {
  const response = await fetch(`${API_BASE_URL}/devices`);
  if (!response.ok) {
    throw new Error('Failed to fetch devices');
  }
  return response.json();
}

/**
 * Add a new device
 * @param {Object} device Device data
 * @returns {Promise<Object>} New device data
 */
export async function addDevice(device) {
  const response = await fetch(`${API_BASE_URL}/devices`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(device),
  });
  
  if (!response.ok) {
    throw new Error('Failed to add device');
  }
  
  return response.json();
}

/**
 * Connect to a device via network (SSH/Telnet)
 * @param {number} deviceId Device ID
 * @param {string} protocol Connection protocol (ssh or telnet)
 * @returns {Promise<Object>} Connection data
 */
export async function connectNetwork(deviceId, protocol) {
  const response = await fetch(`${API_BASE_URL}/connect/network`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ device_id: deviceId, protocol }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to connect to device');
  }
  
  return response.json();
}

/**
 * Send a command to a connected device
 * @param {number} connectionId Connection ID
 * @param {string} command Command to send
 * @returns {Promise<Object>} Command result
 */
export async function sendCommand(connectionId, command) {
  const response = await fetch(`${API_BASE_URL}/send_command/${connectionId}`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ command }),
  });
  
  if (!response.ok) {
    throw new Error('Failed to send command');
  }
  
  return response.json();
}

/**
 * Disconnect from a device
 * @param {number} connectionId Connection ID
 * @returns {Promise<Object>} Disconnect result
 */
export async function disconnect(connectionId) {
  const response = await fetch(`${API_BASE_URL}/disconnect/${connectionId}`, {
    method: 'POST',
  });
  
  if (!response.ok) {
    throw new Error('Failed to disconnect from device');
  }
  
  return response.json();
}

/**
 * Get device information
 * @param {number} connectionId Connection ID
 * @returns {Promise<Object>} Device information
 */
export async function getDeviceInfo(connectionId) {
  const response = await fetch(`${API_BASE_URL}/device_info/${connectionId}`);
  
  if (!response.ok) {
    throw new Error('Failed to get device info');
  }
  
  return response.json();
}