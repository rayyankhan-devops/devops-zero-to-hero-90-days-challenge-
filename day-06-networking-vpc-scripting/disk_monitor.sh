#!/bin/bash
# ==============================================================================
# Script Name: disk_monitor.sh
# Description: Checks root disk usage levels and warns if capacity is exceeded.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

# Threshold percentage to alert
THRESHOLD=${1:-85}
EMAIL="${2:-your-email@example.com}"

echo "============================================================"
echo "                 DISK STORAGE AUDITOR                       "
echo "============================================================"
echo "Safety Threshold: ${THRESHOLD}%"

# 1. Fetch current usage (handles Linux, fallback to macOS syntax)
if [ "$(uname)" = "Darwin" ]; then
    # macOS syntax
    USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
else
    # Linux syntax
    USAGE=$(df -h / | awk 'NR==2 {print $5}' | tr -d '%')
fi

echo "Current consumption level: ${USAGE}%"

# 2. Assert capacity status
if [ "$USAGE" -gt "$THRESHOLD" ]; then
    echo "🚨 WARNING: Disk utilization is CRITICAL at ${USAGE}%!"
    
    PAYLOAD="Critical: Partition '/' capacity is at ${USAGE}% (threshold: ${THRESHOLD}%) on $(hostname) at $(date)."
    
    if command -v mail >/dev/null 2>&1; then
        echo "$PAYLOAD" | mail -s "Storage Alert: $(hostname) Disk Critical" "$EMAIL"
        echo "[*] Disk alert dispatch: Success."
    else
        echo "[*] Disk alert dispatch (Simulated): $PAYLOAD"
    fi
else
    echo "🟢 Storage parameters are clean and safe."
fi

echo "============================================================"
