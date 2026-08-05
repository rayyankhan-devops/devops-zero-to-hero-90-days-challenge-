#!/bin/bash
# ==============================================================================
# Script Name: docker_scout_audit.sh
# Description: Demonstrates Docker Scout vulnerability scanning on local images.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

IMAGE_NAME="${1:-nginx:latest}"

echo "============================================================"
echo "          DOCKER SCOUT VULNERABILITY INSPECTOR              "
echo "============================================================"
echo "[*] Target Image: $IMAGE_NAME"

# Check if Docker Scout CLI plugin is available
if docker scout --help >/dev/null 2>&1; then
    echo "[*] Running Docker Scout Quickview..."
    docker scout quickview "$IMAGE_NAME" || true
    echo ""
    echo "[*] Fetching Vulnerability Recommendations..."
    docker scout recommendations "$IMAGE_NAME" || true
else
    echo "⚠️ Docker Scout plugin not enabled. Displaying command usage:"
    echo "  1. docker scout quickview $IMAGE_NAME"
    echo "  2. docker scout cves $IMAGE_NAME"
    echo "  3. docker scout recommendations $IMAGE_NAME"
fi

echo "============================================================"
