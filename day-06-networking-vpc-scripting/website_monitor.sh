#!/bin/bash
# ==============================================================================
# Script Name: website_monitor.sh
# Description: Validates website response codes and reports status.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

# Configurations
URL="${1:-https://google.com}"
EMAIL="${2:-your-email@example.com}"
LOG_FILE="/tmp/website_monitor.log"

echo "============================================================"
echo "                 WEBSITE STATUS AUDIT                       "
echo "============================================================"
echo "Target URL:   $URL"
echo "Timestamp:    $(date)"

# Check if curl is available
if ! command -v curl >/dev/null 2>&1; then
    echo "🚨 ERROR: 'curl' utility is required but not installed."
    exit 1
fi

# Fetch http response status
echo "[*] Launching HTTP connection request..."
STATUS=$(curl -o /dev/null -s -w "%{http_code}" --connect-timeout 5 "$URL")

echo "[*] HTTP status code returned: $STATUS"

# Validation
if [ "$STATUS" -ne 200 ] && [ "$STATUS" -ne 301 ] && [ "$STATUS" -ne 302 ]; then
    echo "🚨 WARNING: Website status is abnormal ($STATUS)!"
    
    # Alert Payload
    PAYLOAD="Alert: Website $URL is DOWN. Status code: $STATUS at $(date)"
    
    # Log incident
    echo "$(date) - [DOWN] - Status $STATUS" >> "$LOG_FILE"
    
    # Mail service trigger (simulated print for cross-platform robustness)
    if command -v mail >/dev/null 2>&1; then
        echo "$PAYLOAD" | mail -s "Website Alert: $URL is DOWN" "$EMAIL"
        echo "[*] Notification dispatch: Success."
    else
        echo "[*] Notification dispatch (Simulated): $PAYLOAD"
    fi
else
    echo "🟢 Service is active and responding."
    echo "$(date) - [UP] - Status $STATUS" >> "$LOG_FILE"
fi

echo "============================================================"
