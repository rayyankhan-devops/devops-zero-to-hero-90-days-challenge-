#!/bin/bash
# ==============================================================================
# Script Name: git_hooks_setup.sh
# Description: Installs a local Git pre-commit hook to audit staged files.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

HOOK_PATH=".git/hooks/pre-commit"

if [ ! -d ".git" ]; then
    echo "🚨 ERROR: Run this script inside the root of a Git repository."
    exit 1
fi

echo "[*] Installing pre-commit hook at $HOOK_PATH..."

cat <<'EOF' > "$HOOK_PATH"
#!/bin/bash
echo "[Git Hook] Checking for accidental .env commits..."
if git diff --cached --name-only | grep -E "^\.env$"; then
    echo "❌ ERROR: Cannot commit .env file! Unstage it using: git restore --staged .env"
    exit 1
fi
echo "🟢 Pre-commit security check passed."
EOF

chmod +x "$HOOK_PATH"
echo "🟢 Git pre-commit hook installed successfully."
