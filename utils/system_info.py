import platform
import socket
import os

def get_system_info():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        os_info = platform.platform()
        processor = platform.processor()
        machine = platform.machine()
        username = os.getlogin()

        info = f"""
[SYSTEM INFO]
Username: {username}
Hostname: {hostname}
IP Address: {ip_address}
OS: {os_info}
Machine: {machine}
Processor: {processor}
"""
        return info
    except Exception as e:
        return f"[SYSTEM INFO ERROR]: {e}"
