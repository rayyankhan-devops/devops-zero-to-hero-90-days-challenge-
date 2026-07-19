#!/usr/bin/env python3
# ==============================================================================
# Script Name: package_installer.py
# Description: Demonstrates dynamic platform checks and package installations.
# Author:      Muhammad Rayyan
# ==============================================================================

import os
import sys
import subprocess

def check_root():
    """Verifies that the script is run with administrator privileges."""
    # os.geteuid() is not available on Windows
    if sys.platform.startswith("win"):
        # Windows privilege checking placeholder
        return True
    return os.geteuid() == 0

def get_package_manager():
    """Determines host package installer utility."""
    managers = ["apt-get", "yum", "brew"]
    for mgr in managers:
        # Check if installer commands exist in PATH
        check = subprocess.run(["which", mgr], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if check.returncode == 0:
            return mgr
    return None

def install_utility(mgr, package):
    print(f"[*] Package manager detected: {mgr}")
    print(f"[*] Installing '{package}'...")
    
    if mgr == "apt-get":
        # Run update registry first
        subprocess.run(["sudo", "apt-get", "update", "-y"])
        cmd = ["sudo", "apt-get", "install", "-y", package]
    elif mgr == "yum":
        cmd = ["sudo", "yum", "install", "-y", package]
    elif mgr == "brew":
        cmd = ["brew", "install", package]
    else:
        print("Error: Unsupported package installer.")
        return False
        
    try:
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"    🟢 '{package}' successfully installed.")
            return True
        else:
            print(f"    🔴 Installation failed. Error: {res.stderr}")
            return False
    except Exception as e:
        print(f"    🔴 Execution error: {str(e)}")
        return False

def main():
    print("=== Python Package Management Automation ===")
    
    # Check permissions
    if not check_root():
        print("🚨 WARNING: You may need root privileges (sudo) to install packages.")
        
    mgr = get_package_manager()
    if not mgr:
        print("Error: No supported package manager (apt/yum/brew) found.")
        sys.exit(1)
        
    # Attempt to install a lightweight tool (e.g. curl)
    success = install_utility(mgr, "curl")
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
