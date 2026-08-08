#!/bin/bash
# ==============================================================================
# Script Name: deploy_hardened.sh
# Description: Automated DevSecOps runner for SecureVault microservices.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

echo "============================================================"
echo "          SECUREVAULT DEVSECOPS HARDENED DEPLOYER           "
echo "============================================================"

echo "[*] Step 1: Auditing Security Scan Policies..."
if command -v trivy >/dev/null 2>&1; then
    echo "🟢 Running Trivy vulnerability scan on base images..."
    trivy image --severity CRITICAL,HIGH nginx:alpine || true
fi

echo "[*] Step 2: Creating Docker Network 'securevault_net'..."
docker network create securevault_net 2>/dev/null || true

echo "[*] Step 3: Launching Microservices Stack via Docker Compose..."
docker compose up -d --build

echo "🟢 SecureVault Microservices Active!"
echo "============================================================"
