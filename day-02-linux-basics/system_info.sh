#!/bin/bash
# ==============================================================================
# Script Name: system_info.sh
# Description: Audits and prints essential server hardware and OS metrics.
#              Perfect for interview prep to demonstrate command line execution.
# Author:      Muhammad Rayyan
# ==============================================================================

# Exit immediately if a command exits with a non-zero status
set -e

# Clear screen for readability
clear

echo "============================================================"
echo "                   SYSTEM AUDIT REPORT                      "
echo "============================================================"
echo "Generated on: $(date)"
echo "------------------------------------------------------------"

# 1. Host and Kernel Information
echo "[+] HOST & KERNEL:"
echo "    Hostname:   $(hostname)"
echo "    OS Type:    $(uname -o 2>/dev/null || echo 'Unix/Linux')"
echo "    Kernel:     $(uname -r)"
echo "    Architecture: $(uname -m)"
echo ""

# 2. Operating System Release Details
echo "[+] OS RELEASE DETAILS:"
if [ -f /etc/os-release ]; then
    # Parse os-release variables without executing arbitrary lines
    grep -E "^(NAME|VERSION)=" /etc/os-release | tr -d '"' | sed 's/^/    /'
else
    echo "    Details: /etc/os-release not found."
fi
echo ""

# 3. CPU Information
echo "[+] CPU HARDWARE:"
if command -v lscpu >/dev/null 2>&1; then
    lscpu | grep -E 'Model name|CPU\(s\):|Thread\(s\) per core|Core\(s\) per socket' | sed 's/^/    /'
else
    # Fallback for macOS or minimal systems
    echo "    Architecture: $(uname -m)"
    echo "    Processors:   $(sysctl -n hw.ncpu 2>/dev/null || echo 'Unknown')"
fi
echo ""

# 4. Memory (RAM) Consumption
echo "[+] SYSTEM MEMORY USAGE:"
if command -v free >/dev/null 2>&1; then
    free -h | sed 's/^/    /'
else
    # Fallback memory check
    echo "    Memory info:"
    top -l 1 | grep -E "PhysMem|VM" | sed 's/^/    /' 2>/dev/null || vm_stat | head -n 5 | sed 's/^/    /'
fi
echo ""

# 5. Storage (Disk Space) Allocation
echo "[+] DISK SPACE ALLOCATION:"
df -h | grep -E 'Filesystem|/$|/dev/' | sed 's/^/    /'
echo ""

# 6. Active Network Interfaces
echo "[+] ACTIVE IP INTERFACES:"
if command -v ip >/dev/null 2>&1; then
    ip -4 addr show | grep -E 'inet|state' | sed 's/^/    /'
else
    # Fallback to ifconfig
    ifconfig -a | grep -E 'inet |flags' | sed 's/^/    /' 2>/dev/null || echo "    No network utility found."
fi

echo "------------------------------------------------------------"
echo "============================================================"
