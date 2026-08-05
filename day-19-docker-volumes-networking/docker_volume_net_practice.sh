#!/bin/bash
# ==============================================================================
# Script Name: docker_volume_net_practice.sh
# Description: Demonstrates Docker Storage Volumes and User-Defined Networks.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

echo "============================================================"
echo "         DOCKER VOLUMES & CUSTOM NETWORKING PRACTICE        "
echo "============================================================"

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "⚠️ Docker daemon is not active. Displaying CLI command syntax:"
    echo "  1. docker network create app-net"
    echo "  2. docker volume create db-data"
    echo "  3. docker run -d --name db --network app-net -v db-data:/var/lib/postgresql/data postgres:17"
    echo "  4. docker run -d --name app --network app-net -p 8080:80 nginx:alpine"
    exit 0
fi

echo "[*] Step 1: Creating User-Defined Bridge Network 'custom-app-net'..."
docker network create custom-app-net || true

echo "[*] Step 2: Creating Named Volume 'app-data-vol'..."
docker volume create app-data-vol || true

echo "[*] Step 3: Inspecting Docker Networks..."
docker network ls | grep -E 'custom-app-net|bridge|host'

echo "[*] Step 4: Inspecting Docker Volumes..."
docker volume ls | grep 'app-data-vol'

echo "============================================================"
