#!/bin/bash
# ==============================================================================
# Script Name: backup.sh
# Description: Compresses, backs up, and preserves folders with timestamp handles.
#              Demonstrates clean log practices and script parameters.
# Author:      Muhammad Rayyan
# ==============================================================================

# Strict mode: exit immediately on errors, unset variables, or failed pipes
set -euo pipefail

# Configuration Parameters (Override via environment variables if desired)
SOURCE_DIR="${1:-/home/ec2-user/project}"
BACKUP_DIR="${2:-/home/ec2-user/backups}"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_FILE="$BACKUP_DIR/backup_$TIMESTAMP.tar.gz"

echo "============================================================"
echo "               SYSTEM COMPRESSION BACKUP                    "
echo "============================================================"
echo "Date:       $(date)"

# 1. Validate parameters
if [ ! -d "$SOURCE_DIR" ]; then
    echo "🚨 ERROR: Source directory '$SOURCE_DIR' does not exist."
    echo "Usage: $0 [source_directory] [backup_directory]"
    exit 1
fi

# 2. Prepare workspace
echo "[*] Creating backup destination: '$BACKUP_DIR'..."
mkdir -p "$BACKUP_DIR"

# 3. Perform compression
echo "[*] Compressing '$SOURCE_DIR' into '$BACKUP_FILE'..."
if tar -czf "$BACKUP_FILE" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"; then
    echo "🟢 Backup completed successfully!"
    echo "    Archive: $(basename "$BACKUP_FILE")"
    echo "    Size:    $(du -sh "$BACKUP_FILE" | awk '{print $1}')"
else
    echo "🚨 ERROR: Compression operation failed."
    exit 1
fi

# 4. Optional: Clean up backups older than 7 days
echo "[*] Cleaning up old archives (older than 7 days)..."
find "$BACKUP_DIR" -name "backup_*.tar.gz" -type f -mtime +7 -delete || true

echo "============================================================"
