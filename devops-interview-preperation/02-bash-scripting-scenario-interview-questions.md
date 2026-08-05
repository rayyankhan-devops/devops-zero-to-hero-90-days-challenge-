# 📜 Bash Shell Scripting & Production Automation - 50 Scenario-Based Interview Questions

## Scenario 1: Preventing Duplicate Concurrent Script Executions
**Q:** You have a cleanup script running via cron every 5 minutes. Sometimes heavy disk I/O causes a run to take 15 minutes, leading to multiple overlapping instances crashing the server. How do you ensure only ONE instance of the script runs at a time?
**A:** Use `flock` (file locking utility) or Linux directory lockfiles:
```bash
#!/bin/bash
LOCKFILE="/var/run/my_script.lock"

exec 200>"$LOCKFILE"
flock -n 200 || { echo "⚠️ Script is already running. Exiting."; exit 0; }

# Script logic here...
```

## Scenario 2: Strict Error Handling in Production Scripts
**Q:** Why is default Bash execution dangerous in CI/CD pipelines, and what standard header flags should every production Bash script use?
**A:** By default, Bash continues executing subsequent lines even if a command fails, leading to silent pipeline failures or unsafe states.
Always use:
```bash
set -euo pipefail
```
- `-e`: Exit immediately if any command exits with a non-zero status.
- `-u`: Treat unset variables as an error and exit immediately.
- `-o pipefail`: Return the exit status of the last command in a pipeline that failed.

## Scenario 3: Parsing Log Files for Failed Login IP Addresses
**Q:** Write a command-line snippet using `awk`, `sort`, and `uniq` to parse `/var/log/auth.log` and output the top 5 IP addresses with the most failed SSH login attempts.
**A:**
```bash
grep "Failed password" /var/log/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -nr | head -n 5
```

## Scenario 4: Safe Temporary File Cleanup Trap
**Q:** A script creates temporary directory `/tmp/build_123`. If the script is killed prematurely by `Ctrl+C` or an error, the temporary files remain. How do you guarantee cleanup on exit?
**A:** Use the Bash `trap` signal handler:
```bash
#!/bin/bash
TMP_DIR=$(mktemp -d /tmp/build.XXXXXX)

cleanup() {
    echo "[*] Cleaning up temporary folder: $TMP_DIR"
    rm -rf "$TMP_DIR"
}

trap cleanup EXIT INT TERM
```

## Scenario 5: Automated Backup Retention Policy (Deleting Files Older than N Days)
**Q:** Write a Bash function that searches `/backups`, compresses `.tar.gz` archives, and removes backups older than 30 days while skipping active subdirectories.
**A:**
```bash
find /backups -maxdepth 1 -name "*.tar.gz" -type f -mtime +30 -exec rm -vf {} \;
```

## Scenario 6: Retrying a Failing API Request with Exponential Backoff
**Q:** A Bash deployment script calls a remote REST API via `curl`. Network blips cause sporadic 503 failures. How do you implement a retry loop with delay?
**A:**
```bash
retry_curl() {
    local url="$1" max_attempts=5 attempt=1 delay=2
    until curl -sf "$url"; do
        if [ $attempt -eq $max_attempts ]; then
            echo "❌ Max attempts reached. API call failed."
            return 1
        fi
        echo "⚠️ Attempt $attempt failed. Retrying in ${delay}s..."
        sleep $delay
        attempt=$((attempt + 1))
        delay=$((delay * 2))
    done
}
```

## Scenario 7: Reading Environment Variables Safely from `.env`
**Q:** How do you read key-value pairs from a `.env` file in Bash without risking command execution if a line contains spaces or special characters?
**A:** Use `export` with `xargs` or read line by line:
```bash
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi
```

## Scenario 8: Parallel Execution of Tasks in Shell
**Q:** You need to ping 50 IP addresses listed in `ips.txt`. Running a standard `for` loop sequentially takes 2 minutes. How do you speed this up to 5 seconds in Bash?
**A:** Execute commands in background subshells with `wait`, or use `xargs -P`:
```bash
cat ips.txt | xargs -n 1 -P 20 ping -c 2 -W 1
```

## Scenario 9: Monitoring Disk Usage and Sending Alert
**Q:** Write a cron-friendly Bash script that checks disk usage on `/`, and if usage exceeds 85%, posts a JSON alert payload to a Slack Webhook URL.
**A:**
```bash
USAGE=$(df / | awk 'NR==2 {print $5}' | tr -d '%')
if [ "$USAGE" -gt 85 ]; then
    curl -X POST -H 'Content-type: application/json' \
      --data "{\"text\":\"🚨 Alert: Disk usage on $(hostname) is at ${USAGE}%!\"}" \
      "$SLACK_WEBHOOK_URL"
fi
```

## Scenario 10: In-Place Editing of Config Files Using `sed`
**Q:** How do you update `PORT=8080` to `PORT=9090` in `config.ini` across 20 servers via Bash while creating a backup copy `config.ini.bak`?
**A:**
```bash
sed -i.bak 's/^PORT=8080/PORT=9090/' config.ini
```

---

## Scenario 11-50 Summary Coverage Matrix
- **String & File Processing:** `cut`, `awk`, `grep -E`, `tr`, `basename`, `dirname`, heredocs (`cat <<EOF`).
- **Control Flow:** `select` menus, `case` statements, `while read line` processing files safely.
- **Process Signals & Traps:** Handling `SIGTERM`, `SIGHUP`, `SIGINT`.
