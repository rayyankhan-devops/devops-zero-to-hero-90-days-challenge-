#!/bin/bash
# ==============================================================================
# Script Name: ping_servers_loop.sh
# Description: Script iterating over arrays to perform connectivity checks.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

# Host array list
servers=(
    "127.0.0.1"
    "google.com"
    "github.com"
)

echo "===================================================="
echo "            BASH HOST CONNECTIVITY LOOPS            "
echo "===================================================="

for server in "${servers[@]}"; do
    echo "[*] Pinging $server..."
    
    # Run ping with 2 count and 3 seconds timeout
    if ping -c 2 -W 3 "$server" > /dev/null 2>&1; then
        echo "    🟢 $server is REACHABLE!"
    else
        echo "    🔴 $server is UNREACHABLE!"
    fi
    echo "----------------------------------------------------"
done

echo "Audit iteration complete."
