#!/usr/bin/env python3
# ==============================================================================
# Script Name: server_checker.py
# Description: Pings a list of servers using Python's subprocess module.
#              Demonstrates enterprise scripting practices over os.system.
# Author:      Muhammad Rayyan
# ==============================================================================

import subprocess
import sys

def ping_server(host):
    print(f"[*] Pinging: {host}...")
    
    # Configure ping arguments based on Operating System
    # -c 2 for Linux/macOS, -n 2 for Windows
    ping_param = "-n" if sys.platform.lower().startswith("win") else "-c"
    command = ["ping", ping_param, "2", "-W", "3", host]
    
    try:
        # Run command without launching a shell (protects against command injection)
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=10
        )
        
        # Check exit code
        if result.returncode == 0:
            print(f"    🟢 {host} is ONLINE!")
            return True
        else:
            print(f"    🔴 {host} is OFFLINE! (Return code: {result.returncode})")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"    🔴 {host} TIMED OUT!")
        return False
    except Exception as e:
        print(f"    🔴 Error checking {host}: {str(e)}")
        return False

def main():
    # Target list to check
    servers = ["127.0.0.1", "google.com", "github.com", "invalid-domain-test.local"]
    
    print("====================================================")
    print("             PYTHON SYSTEM PING CHECKER             ")
    print("====================================================")
    
    online_count = 0
    for server in servers:
        status = ping_server(server)
        if status:
            online_count += 1
        print("-" * 52)
        
    print(f"Summary: {online_count}/{len(servers)} servers are ONLINE.")
    print("====================================================")

if __name__ == "__main__":
    main()
