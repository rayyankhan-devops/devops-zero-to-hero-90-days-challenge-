#!/bin/bash
# ==============================================================================
# Script Name: docker_container_auditor.sh
# Description: Checks local Docker engine status and audits running containers.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

echo "============================================================"
echo "               DOCKER ENGINE AUDITOR & UTILITY              "
echo "============================================================"

# Check if Docker is installed
if ! command -v docker >/dev/null 2>&1; then
    echo "🚨 Docker CLI not found. Install Docker Desktop or run:"
    echo "    sudo apt update && sudo apt install docker.io -y"
    exit 1
fi

echo "[*] Docker Client & Server Version:"
docker --version
echo ""

echo "[*] Active Containers (docker ps):"
docker ps || echo "⚠️ Cannot connect to Docker Daemon. Ensure Docker service is running!"
echo ""

echo "[*] Local Docker Images (docker images):"
docker images || true
echo ""

echo "[*] Docker Disk Usage Summary (docker system df):"
docker system df || true
echo "============================================================"
