#!/bin/bash
# ==============================================================================
# Script Name: run_text_filters.sh
# Description: Demonstrates AWK and GREP processing filters on practice logs.
#              Excellent for interview prep to demonstrate text automation.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

# Locate workspace files
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
USERS_FILE="$SCRIPT_DIR/practice_data/users.txt"
LOG_FILE="$SCRIPT_DIR/practice_data/app.log"

echo "============================================================"
echo "           AWK & GREP PRACTICAL FILTER RUNNER               "
echo "============================================================"
echo ""

# --- GREP DEMONSTRATIONS ---
echo "------------------------------------------------------------"
echo "[+] GREP DEMO: Filtering ERROR Logs"
echo "------------------------------------------------------------"
# Search for exact match
grep "ERROR" "$LOG_FILE"
echo ""

echo "------------------------------------------------------------"
echo "[+] GREP DEMO: Excluding Debug and Info (Show Warn/Error only)"
echo "------------------------------------------------------------"
# -E extended regex, -v invert match
grep -Ev "DEBUG|INFO" "$LOG_FILE"
echo ""

echo "------------------------------------------------------------"
echo "[+] GREP DEMO: Count of INFO messages"
echo "------------------------------------------------------------"
# -c count matches
count=$(grep -c "INFO" "$LOG_FILE")
echo "Number of INFO logs: $count"
echo ""

# --- AWK DEMONSTRATIONS ---
echo "------------------------------------------------------------"
echo "[+] AWK DEMO: Print Usernames and Roles (Splitting by ':')"
echo "------------------------------------------------------------"
# -F specifies field separator. NR>1 skips column headers.
awk -F: 'NR>1 {print "User: " $1 " \t-> Role: " $4}' "$USERS_FILE"
echo ""

echo "------------------------------------------------------------"
echo "[+] AWK DEMO: Filter Users with Age > 22"
echo "------------------------------------------------------------"
# $2 represents age column. Checks if integer is greater than 22.
awk -F: 'NR>1 && $2 > 22 {print "Found user: " $1 " (Age: " $2 ")"}' "$USERS_FILE"
echo ""

echo "------------------------------------------------------------"
echo "[+] AWK DEMO: Formatting columns into custom reports"
echo "------------------------------------------------------------"
# Demonstrates BEGIN and END blocks in AWK
awk -F: '
BEGIN { print "--- START REPORT ---" }
NR>1 { printf "%-10s resides in %-10s\n", $1, $3 }
END { print "--- END OF REPORT ---" }
' "$USERS_FILE"

echo "============================================================"
