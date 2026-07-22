#!/bin/bash
# ==============================================================================
# Script Name: ufw_manager.sh
# Description: Safely audits and configures firewall rules using UFW.
#              Demonstrates root validation checks.
# Author:      Muhammad Rayyan
# ==============================================================================

# Strict mode
set -euo pipefail

# Ensure script is executed as root
if [ "$EUID" -ne 0 ]; then
    echo "============================================================"
    echo "🚨 ERROR: This script must be run as root (or with sudo)."
    echo "Usage: sudo $0"
    echo "============================================================"
    exit 1
fi

echo "============================================================"
echo "                 UFW FIREWALL MANAGER                       "
echo "============================================================"

# Check if ufw is installed
if ! command -v ufw >/dev/null 2>&1; then
    echo "🚨 ERROR: 'ufw' utility is not installed."
    echo "On Debian/Ubuntu: sudo apt-get install ufw"
    exit 1
fi

# Print current state
echo "[*] Fetching UFW Status..."
ufw status verbose || true
echo ""

show_menu() {
    echo "------------------------------------------------------------"
    echo "Select UFW Action:"
    echo "1) Enable Firewall (Warning: Ensure SSH port 22 is allowed!)"
    echo "2) Allow Standard Ports (SSH:22, HTTP:80, HTTPS:443)"
    echo "3) Block a Custom Port"
    echo "4) Reset Firewall Rules to Default"
    echo "5) Exit"
    echo "------------------------------------------------------------"
}

# Run loop
while true; do
    show_menu
    read -p "Enter Choice [1-5]: " choice
    case "$choice" in
        1)
            echo "[*] Allowing SSH port 22 first to prevent lockout..."
            ufw allow 22/tcp
            echo "[*] Enabling UFW..."
            ufw --force enable
            echo "🟢 UFW active."
            ;;
        2)
            echo "[*] Allowing standard services..."
            ufw allow 22/tcp comment 'SSH Port'
            ufw allow 80/tcp comment 'HTTP Web Server'
            ufw allow 443/tcp comment 'HTTPS Secure Web Server'
            echo "🟢 Ports allowed successfully."
            ;;
        3)
            read -p "Enter port number to block: " block_port
            if [[ "$block_port" =~ ^[0-9]+$ ]]; then
                echo "[*] Blocking port $block_port..."
                ufw deny "$block_port"
                echo "🟢 Port $block_port blocked."
            else
                echo "🚨 Invalid port number."
            fi
            ;;
        4)
            echo "[*] Resetting rules to factory default..."
            ufw --force reset
            echo "🟢 Rules reset."
            ;;
        5)
            echo "Exiting..."
            break
            ;;
        *)
            echo "🚨 Invalid option. Select [1-5]."
            ;;
    esac
    echo ""
    echo "[*] Current rules:"
    ufw status numbered || true
done

echo "============================================================"
