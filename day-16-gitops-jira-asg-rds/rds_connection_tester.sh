#!/bin/bash
# ==============================================================================
# Script Name: rds_connection_tester.sh
# Description: Tests network connectivity to Amazon RDS MySQL instances.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

RDS_HOST="${1:-db-instance.c123456789.us-east-1.rds.amazonaws.com}"
RDS_PORT="${2:-3306}"

echo "============================================================"
echo "          AMAZON RDS NETWORK CONNECTIVITY TESTER            "
echo "============================================================"
echo "[*] Target Host: $RDS_HOST"
echo "[*] Target Port: $RDS_PORT"
echo "------------------------------------------------------------"

# 1. Test Port socket via nc (netcat)
echo "[*] Step 1: Running TCP Socket check (nc -zv)..."
if command -v nc >/dev/null 2>&1; then
    if nc -zv -w 5 "$RDS_HOST" "$RDS_PORT" 2>/dev/null; then
        echo "🟢 SUCCESS: Port $RDS_PORT is open and reachable!"
    else
        echo "❌ FAILED: Cannot connect to $RDS_HOST on port $RDS_PORT."
        echo "    Check Security Group: Ensure RDS Inbound rule permits EC2 Security Group ID!"
    fi
else
    echo "⚠️ 'nc' command not available. Simulation mode:"
    echo "    [Simulation] Attempting connection to $RDS_HOST:$RDS_PORT... (Verify SG rules)"
fi

echo "============================================================"
