from typing import Dict, Any, List

def parse_show_version(output: str) -> Dict[str, Any]:
    """
    Parse the output of 'show version' command to extract version information
    
    Args:
        output: The string output from the 'show version' command
        
    Returns:
        Dictionary containing parsed version information
    """
    result = {
        "version": None,
        "model": None,
        "serial": None,
        "uptime": None,
        "system_image": None,
    }
    
    lines = output.splitlines()
    
    for line in lines:
        if "Version" in line and result["version"] is None:
            parts = line.split("Version")
            if len(parts) > 1:
                result["version"] = parts[1].split(",")[0].strip()
        
        if "uptime is" in line:
            parts = line.split("uptime is")
            if len(parts) > 1:
                result["uptime"] = parts[1].strip()
        
        if "System image file is" in line:
            parts = line.split("System image file is")
            if len(parts) > 1:
                result["system_image"] = parts[1].strip().strip('"')
    
    return result

def parse_show_interfaces(output: str) -> List[Dict[str, Any]]:
    """
    Parse the output of 'show interfaces' command to extract interface information
    
    Args:
        output: The string output from the 'show interfaces' command
        
    Returns:
        List of dictionaries containing parsed interface information
    """
    interfaces = []
    current_interface = None
    
    lines = output.splitlines()
    
    for line in lines:
        # New interface entry starts with the interface name
        if line and not line.startswith(" "):
            if "is " in line:
                parts = line.split("is ")
                if_name = parts[0].strip()
                status = parts[1].split(",")[0].strip()
                
                # Save previous interface if exists
                if current_interface:
                    interfaces.append(current_interface)
                
                # Start new interface
                current_interface = {
                    "name": if_name,
                    "status": status,
                    "protocol": None,
                    "ip_address": None,
                    "mtu": None,
                    "bandwidth": None,
                    "duplex": None,
                    "speed": None,
                    "description": None
                }
                
                # Get protocol status
                if "line protocol is " in line:
                    protocol = line.split("line protocol is ")[1].split()[0]
                    current_interface["protocol"] = protocol
        
        # Parse additional interface information
        elif current_interface:
            if "Internet address is" in line:
                ip = line.split("Internet address is ")[1].split()[0]
                current_interface["ip_address"] = ip
            
            elif "MTU" in line and "bytes" in line:
                mtu_part = line.split("MTU")[1].split("bytes")[0].strip()
                current_interface["mtu"] = mtu_part
            
            elif "BW" in line:
                try:
                    bw_part = line.split("BW")[1].split()[0].strip()
                    current_interface["bandwidth"] = bw_part
                except:
                    pass
            
            elif "duplex" in line.lower():
                duplex_parts = line.lower().split("duplex")[0].strip()
                current_interface["duplex"] = duplex_parts
                
                if "mb/s" in line.lower():
                    speed_parts = line.lower().split("duplex")[1]
                    speed = speed_parts.split("mb/s")[0].strip()
                    current_interface["speed"] = f"{speed} Mb/s"
            
            elif "Description:" in line:
                desc = line.split("Description:")[1].strip()
                current_interface["description"] = desc
    
    # Add the last interface
    if current_interface:
        interfaces.append(current_interface)
    
    return interfaces

def parse_show_running_config(output: str) -> Dict[str, Any]:
    """
    Parse the output of 'show running-config' command to extract configuration sections
    
    Args:
        output: The string output from the 'show running-config' command
        
    Returns:
        Dictionary containing parsed configuration sections
    """
    config = {
        "hostname": None,
        "interfaces": {},
        "routing": {
            "static_routes": []
        },
        "services": [],
        "access_lists": {},
        "users": []
    }
    
    # Extract hostname
    for line in output.splitlines():
        if line.startswith('hostname'):
            config["hostname"] = line.split()[1]
            break
    
    # Extract interfaces
    current_if = None
    for line in output.splitlines():
        if line.startswith('interface'):
            current_if = line.split()[1]
            config["interfaces"][current_if] = []
        elif current_if and line.startswith(' '):
            config["interfaces"][current_if].append(line.strip())
        elif current_if and not line.startswith(' '):
            current_if = None
    
    # Extract static routes
    for line in output.splitlines():
        if line.startswith('ip route'):
            parts = line.split()
            if len(parts) >= 4:
                route = {
                    "destination": parts[2],
                    "mask": parts[3],
                    "next_hop": parts[4] if len(parts) > 4 else None
                }
                config["routing"]["static_routes"].append(route)
    
    # Extract services
    for line in output.splitlines():
        if line.startswith('service'):
            config["services"].append(line.strip())
    
    # Extract access lists
    current_acl = None
    for line in output.splitlines():
        if line.startswith('access-list'):
            parts = line.split()
            acl_num = parts[1]
            if acl_num not in config["access_lists"]:
                config["access_lists"][acl_num] = []
            config["access_lists"][acl_num].append(line.strip())
        elif line.startswith('ip access-list'):
            parts = line.split()
            acl_name = parts[3]
            current_acl = acl_name
            if current_acl not in config["access_lists"]:
                config["access_lists"][current_acl] = []
        elif current_acl and line.startswith(' '):
            config["access_lists"][current_acl].append(line.strip())
        elif current_acl and not line.startswith(' '):
            current_acl = None
    
    # Extract user accounts
    for line in output.splitlines():
        if line.startswith('username'):
            parts = line.split()
            if len(parts) >= 4:
                user = {
                    "username": parts[1],
                    "privilege": parts[3] if parts[2] == "privilege" else None
                }
                config["users"].append(user)
    
    return config