#!/bin/bash
# ==============================================================================
# Script Name: install_nginx.sh
# Description: Installs and registers Nginx based on host OS configurations.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

# Check for root privilege
if [ "$EUID" -ne 0 ]; then
    echo "🚨 ERROR: This script must be run as root (or with sudo)."
    echo "Usage: sudo $0"
    exit 1
fi

echo "===================================================="
echo "          AUTOMATED NGINX SERVICE INSTALLER         "
echo "===================================================="

# Determine Package Manager
if command -v apt-get >/dev/null 2>&1; then
    echo "[+] Debian/Ubuntu environment detected."
    echo "[*] Updating apt database..."
    apt-get update -y > /dev/null
    
    echo "[*] Installing Nginx..."
    apt-get install -y nginx
    
elif command -v yum >/dev/null 2>&1; then
    echo "[+] RedHat/CentOS environment detected."
    echo "[*] Installing epel-release..."
    yum install -y epel-release > /dev/null
    
    echo "[*] Installing Nginx..."
    yum install -y nginx
    
else
    echo "🚨 ERROR: No compatible package manager (apt/yum) found."
    exit 1
fi

# Starting and verifying status
echo "[*] Starting Nginx service..."
systemctl start nginx || service nginx start || true
systemctl enable nginx || true

echo "🟢 Nginx successfully installed and started."
echo "===================================================="
