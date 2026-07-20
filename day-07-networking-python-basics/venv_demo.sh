#!/bin/bash
# ==============================================================================
# Script Name: venv_demo.sh
# Description: Automates Python Virtual Environment creation, package installation,
#              isolation check, and deactivation.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

ENV_NAME="my_practice_env"

echo "============================================================"
echo "         PYTHON VIRTUAL ENVIRONMENT BOOTSTRAPPER            "
echo "============================================================"

# 1. Check if Python is installed
if ! command -v python3 >/dev/null 2>&1; then
    echo "🚨 ERROR: Python3 is required but not installed."
    exit 1
fi

# 2. Check if venv module is available
if ! python3 -c "import venv" >/dev/null 2>&1; then
    echo "🚨 ERROR: Python3 venv module is not installed."
    echo "On Ubuntu/Debian, install with: sudo apt-get install python3-venv"
    exit 1
fi

# 3. Create Virtual Environment
echo "[*] Creating virtual environment: '$ENV_NAME'..."
python3 -m venv "$ENV_NAME"
echo "🟢 Virtual environment created successfully."
echo ""

# 4. Activate Environment
echo "[*] Activating virtual environment..."
# Detect shell and source accordingly
if [ -f "$ENV_NAME/bin/activate" ]; then
    # Linux / macOS activation
    source "$ENV_NAME/bin/activate"
elif [ -f "$ENV_NAME/Scripts/activate" ]; then
    # Windows/Git Bash activation fallback
    source "$ENV_NAME/Scripts/activate"
else
    echo "🚨 ERROR: Activation script not found."
    exit 1
fi

# Verify active Python path
echo "    Active python binary: $(which python)"
echo ""

# 5. Install a package inside the environment
echo "[*] Installing 'requests' package inside '$ENV_NAME'..."
pip install --quiet requests
echo "🟢 Installation complete."
echo ""

# 6. Verify isolation
echo "[*] Auditing installed packages inside environment (pip list):"
pip list | grep -E 'Package|Version|requests' | sed 's/^/    /'
echo ""

# 7. Deactivate
echo "[*] Deactivating environment..."
deactivate
echo "🟢 Virtual environment deactivated."
echo "    System python binary restored: $(which python)"

# Clean up environment files
echo "[*] Cleaning up environment folder..."
rm -rf "$ENV_NAME"
echo "============================================================"
