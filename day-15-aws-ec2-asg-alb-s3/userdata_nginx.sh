#!/bin/bash
# ==============================================================================
# Script Name: userdata_nginx.sh
# Description: EC2 User Data script to install and configure Nginx web server.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

echo "[*] Updating apt package repository..."
apt-get update -y

echo "[*] Installing Nginx..."
apt-get install -y nginx

echo "[*] Writing custom landing page..."
cat <<'EOF' > /var/www/html/index.html
<!DOCTYPE html>
<html>
<head>
    <title>DevOps 90 Days Challenge - Day 15</title>
    <style>
        body { font-family: sans-serif; background-color: #0d1117; color: #58a6ff; text-align: center; padding-top: 50px; }
        .card { background: #161b22; display: inline-block; padding: 40px; border-radius: 12px; border: 1px solid #30363d; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🚀 EC2 Nginx Web Instance Active!</h1>
        <p>Managed via AWS Launch Template & User Data Script</p>
    </div>
</body>
</html>
EOF

echo "[*] Enabling and starting Nginx service..."
systemctl enable nginx
systemctl restart nginx

echo "🟢 Nginx deployment complete."
