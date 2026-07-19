#!/bin/bash
# ==============================================================================
# Script Name: permission_fixer.sh
# Description: Demonstrates how chmod, permissions, and file modes are checked.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

TARGET="practice_permission_file.txt"

echo "=== Permission and Chmod Operations Demo ==="

# 1. Create a practice file
echo "Creating practice file..."
echo "Temp contents" > "$TARGET"

# 2. View current permissions
echo "[+] Initial File Stats:"
ls -l "$TARGET"

# 3. Apply standard Read/Write (644) permissions
echo "[+] Applying chmod 644..."
chmod 644 "$TARGET"
ls -l "$TARGET"

# 4. Check if file is executable before running chmod +x
if [ -x "$TARGET" ]; then
    echo "    File is executable."
else
    echo "    File is NOT executable (Expected)."
fi

# 5. Apply Owner-Only Execution (700) permissions
echo "[+] Applying chmod 700 (Owner-Only Access)..."
chmod 700 "$TARGET"
ls -l "$TARGET"

# 6. Apply standard scripts permission (755)
echo "[+] Applying chmod 755 (Public Read & Execute)..."
chmod 755 "$TARGET"
ls -l "$TARGET"

if [ -x "$TARGET" ]; then
    echo "    File is now executable."
fi

# Cleanup temp file
rm -f "$TARGET"
echo "=== Demo Completed & Cleared ==="
