#!/bin/bash
# ==============================================================================
# Script Name: lvm_status.sh
# Description: Checks and displays current LVM states safely.
#              Demonstrates checking root permissions.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

# Ensure script is executed as root or with sudo
if [ "$EUID" -ne 0 ]; then
    echo "============================================================"
    echo "🚨 ERROR: This script must be run as root (or with sudo)."
    echo "Reason: Accessing LVM data requires privileges."
    echo "============================================================"
    echo "Please execute: sudo $0"
    exit 1
fi

echo "============================================================"
echo "                   LVM STATUS REPORT                        "
echo "============================================================"
echo "Checked on: $(date)"
echo "------------------------------------------------------------"

# 1. Physical Volumes
echo "[+] PHYSICAL VOLUMES (pvs):"
if command -v pvs >/dev/null 2>&1; then
    pvs || echo "    No physical volumes found."
else
    echo "    Error: 'pvs' command is not installed."
fi
echo ""

# 2. Volume Groups
echo "[+] VOLUME GROUPS (vgs):"
if command -v vgs >/dev/null 2>&1; then
    vgs || echo "    No volume groups found."
else
    echo "    Error: 'vgs' command is not installed."
fi
echo ""

# 3. Logical Volumes
echo "[+] LOGICAL VOLUMES (lvs):"
if command -v lvs >/dev/null 2>&1; then
    lvs || echo "    No logical volumes found."
else
    echo "    Error: 'lvs' command is not installed."
fi

echo "============================================================"
