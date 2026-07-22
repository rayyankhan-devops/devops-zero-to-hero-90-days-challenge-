#!/bin/bash
# ==============================================================================
# Script Name: git_practice_helper.sh
# Description: Interactive Git sandbox simulator demonstrating initialization,
#              staging, committing, restoring, and branches.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

# Create a isolated temp sandbox folder inside the day folder
SANDBOX_DIR="git_sandbox_env"

cleanup() {
    if [ -d "$SANDBOX_DIR" ]; then
        echo "[*] Cleaning up sandbox environment..."
        rm -rf "$SANDBOX_DIR"
    fi
}

# Trap exits to ensure cleanup is run
trap cleanup EXIT

echo "============================================================"
echo "                 GIT COMMAND WORKFLOW SIMULATOR             "
echo "============================================================"

# Prepare workspace
cleanup
mkdir -p "$SANDBOX_DIR"
cd "$SANDBOX_DIR"

# 1. Initialize local repository
echo "[+] Step 1: Initializing empty Git Repository (git init)"
git init -q
echo "🟢 Git repository initialized successfully."
echo ""

# 2. Configure mock local user for git commits inside sandbox
git config user.name "Rayyan Practice"
git config user.email "practice@example.com"

# 3. Create file and check status
echo "[+] Step 2: Creating a source file and checking status"
echo "print('Hello DevOps!')" > main.py
git status -s
echo ""

# 4. Stage file
echo "[+] Step 3: Staging file (git add)"
git add main.py
git status -s
echo "🟢 File added to staging index."
echo ""

# 5. Commit changes
echo "[+] Step 4: Committing staged changes (git commit)"
git commit -m "initial: add main.py program"
git status
echo ""

# 6. Branch creation & Checkout
echo "[+] Step 5: Creating and switching to a feature branch"
git branch feature-login
git switch feature-login
echo "🟢 Currently on branch: $(git branch --show-current)"
echo ""

# 7. Modify file and demonstrate Git Restore
echo "[+] Step 6: Modifying file & demonstrating Git Restore"
echo "print('Unstaged changes')" >> main.py
echo "--- File status before restore ---"
git status -s
echo "--- Running git restore ---"
git restore main.py
echo "--- File status after restore ---"
git status -s
echo "🟢 Unstaged changes discarded successfully."
echo ""

# 8. Git log output
echo "[+] Step 7: Printing Commit Logs (git log --oneline)"
git log --oneline
echo "============================================================"
