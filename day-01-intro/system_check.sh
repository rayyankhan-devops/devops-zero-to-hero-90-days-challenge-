#!/bin/bash
# ==============================================================================
# Script Name: system_check.sh
# Description: Checks local DevOps environment dependencies (Git, Python, Docker, OS).
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

echo "============================================================"
echo "          DEVOPS ENVIRONMENT DEPENDENCY AUDITOR             "
echo "============================================================"

echo "[*] Operating System Info:"
uname -a
echo ""

echo "[*] Checking Git:"
if command -v git >/dev/null 2>&1; then
    git --version
else
    echo "❌ Git is NOT installed."
fi

echo "[*] Checking Python 3:"
if command -v python3 >/dev/null 2>&1; then
    python3 --version
else
    echo "❌ Python 3 is NOT installed."
fi

echo "[*] Checking Docker:"
if command -v docker >/dev/null 2>&1; then
    docker --version
else
    echo "⚠️ Docker is NOT installed or running."
fi

echo "============================================================"
