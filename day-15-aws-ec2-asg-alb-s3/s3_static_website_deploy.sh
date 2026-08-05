#!/bin/bash
# ==============================================================================
# Script Name: s3_static_website_deploy.sh
# Description: Configures S3 bucket for static website hosting via AWS CLI.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

BUCKET_NAME="${1:-rayyan-devops-static-site-2026}"
REGION="us-east-1"

echo "============================================================"
echo "          AWS S3 STATIC WEBSITE DEPLOYMENT                  "
echo "============================================================"
echo "[*] Target Bucket: s3://$BUCKET_NAME"

# Check AWS CLI
if ! command -v aws >/dev/null 2>&1; then
    echo "⚠️ AWS CLI not installed. Displaying CLI automation steps:"
    echo "  1. aws s3 mb s3://$BUCKET_NAME --region $REGION"
    echo "  2. aws s3 website s3://$BUCKET_NAME/ --index-document index.html"
    echo "  3. aws s3 sync ./html-site/ s3://$BUCKET_NAME/"
    exit 0
fi

echo "[*] Step 1: Creating Bucket..."
aws s3 mb "s3://$BUCKET_NAME" --region "$REGION" || true

echo "[*] Step 2: Configuring Static Website Hosting..."
aws s3 website "s3://$BUCKET_NAME/" --index-document index.html --error-document error.html || true

echo "🟢 Website endpoint: http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com"
echo "============================================================"
