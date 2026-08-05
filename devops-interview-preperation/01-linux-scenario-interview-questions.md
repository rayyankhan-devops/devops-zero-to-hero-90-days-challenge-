# 🐧 Linux Systems & Storage Administration - 50 Scenario-Based Interview Questions

## Scenario 1: Disk Space Full Alert on Root Partition (`/`)
**Q:** A production Linux server triggers a 98% disk usage alert on `/`. You run `df -h` and confirm `/` is full, but `du -sh /*` shows only 10GB used out of 100GB. What is causing this discrepancy and how do you resolve it without rebooting?
**A:** This discrepancy occurs when deleted files are still held open by running processes. The filesystem unlinks the file pointer, but the inodes and blocks remain allocated until the process terminates.
1. Run `lsof +L1` or `lsof | grep deleted` to identify processes holding open deleted file handles.
2. Truncate the file descriptor directly to free disk space immediately without killing the app: `echo "" > /proc/<PID>/fd/<FD_NUM>` or restart the process gracefully (`systemctl restart <service>`).

## Scenario 2: Extending LVM Volume Without Downtime
**Q:** An application database partition mounted on `/var/lib/mysql` (LVM volume `dev/mapper/vg_data-lv_mysql`) is out of space. You added a new 100GB physical disk `/dev/sdb` to the cloud server. Walk through the exact zero-downtime commands to extend the partition.
**A:**
1. Initialize physical volume: `pvcreate /dev/sdb`
2. Extend volume group: `vgextend vg_data /dev/sdb`
3. Extend logical volume: `lvextend -L +100G /dev/mapper/vg_data-lv_mysql` (or `lvextend -l +100%FREE ...`)
4. Resize filesystem online:
   - For ext4: `resize2fs /dev/mapper/vg_data-lv_mysql`
   - For xfs: `xfs_growfs /var/lib/mysql`

## Scenario 3: High Load Average with Low CPU Usage
**Q:** `top` shows a system load average of 15.0 on a 4-core machine, but CPU usage is only 10%. What does this indicate and how do you diagnose the root cause?
**A:** High load average with low CPU utilization indicates processes stuck in Uninterruptible Sleep (`D` state), usually waiting for I/O disk operations or hung NFS mounts.
1. Inspect process states: `ps aux | awk '$8 ~ /D/ {print $0}'`
2. Check disk I/O metrics using `iostat -xz 1 10` or `iotop -o` to identify processes causing high `%util` or high `await` latency.

## Scenario 4: SSH Key Access Failing with "Permission Denied (publickey)"
**Q:** You uploaded a user's public SSH key to `~/.ssh/authorized_keys`, but SSH login still fails with `Permission denied (publickey)`. What is wrong?
**A:** SSH enforces strict permission checks on the user's home directory and SSH configuration files.
1. Fix permissions:
   - User home directory: `chmod 755 /home/username` (or `700`)
   - `.ssh` directory: `chmod 700 /home/username/.ssh`
   - `authorized_keys` file: `chmod 600 /home/username/.ssh/authorized_keys`
   - Owner check: `chown -R username:username /home/username/.ssh`
2. Inspect server-side SSH logs: `journalctl -u sshd -n 50 --no-pager` or `/var/log/auth.log`.

## Scenario 5: Process Memory Leak & OOM Killer Trigger
**Q:** A Java microservice randomly crashes every night at 2 AM with `Killed`. `dmesg` shows `Out of memory: Kill process 14201 (java)`. How do you investigate and prevent this?
**A:** The Linux kernel Out-Of-Memory (OOM) Killer terminated the process because the system ran out of RAM and swap space.
1. Check OOM logs: `dmesg -T | grep -i oom` or `journalctl -k | grep -i oom`.
2. Configure JVM heap memory bounds (`-Xmx2g -Xms2g`) so Java does not exceed cgroup/system limits.
3. Configure `swappiness` (`sysctl vm.swappiness=10`) or set `oom_score_adj` to protect critical processes.

## Scenario 6: Filesystem Read-Only Remount
**Q:** Suddenly, users report they cannot write files to `/var/log`. Running `touch /var/log/test` outputs `Read-only filesystem`. Why did this happen and how do you recover?
**A:** The Linux kernel remounts a filesystem as read-only when it detects disk I/O errors, block corruption, or underlying storage failure to prevent further data loss.
1. Inspect kernel log messages: `dmesg | tail -n 50` or `journalctl -k`.
2. Unmount the volume safely (if possible): `umount /var/log`
3. Run filesystem repair check: `fsck -y /dev/sdb1` (or `xfs_repair`).
4. Remount read-write: `mount -o remount,rw /var/log`.

## Scenario 7: Inode Exhaustion Despite Free Disk Space
**Q:** `df -h` shows 50GB of free space on `/data`, but creating a small 1KB file fails with `No space left on device`. What is the cause?
**A:** The filesystem has run out of available **Inodes** (index nodes) due to millions of tiny files being created (e.g. session cache files).
1. Verify inode usage: `df -i /data`
2. Find directories containing high file counts: `find /data -xdev -type f | cut -d "/" -f 2 | sort | uniq -c | sort -n`
3. Remove redundant small files: `find /data/tmp -type f -mtime +7 -delete`.

## Scenario 8: Service Fails to Start on Boot (`systemd`)
**Q:** You created a systemd service file `/etc/systemd/system/myapp.service`, but `systemctl start myapp` fails. How do you troubleshoot?
**A:**
1. Reload systemd daemon manager: `systemctl daemon-reload`
2. Inspect exact error status: `systemctl status myapp.service`
3. Fetch detailed unit logs: `journalctl -u myapp.service -e --no-pager`
4. Verify execution path binary permissions (`chmod +x`), environment file paths, and user/group definitions in the `.service` file.

## Scenario 9: Zombie Process Cleanup
**Q:** Running `top` shows `3 zombie` processes. How do you remove zombie processes without rebooting the server?
**A:** Zombie processes (`Z` state) are terminated processes whose parent process has not yet read their exit status via `wait()` syscall. You cannot kill a zombie directly with `kill -9 <zombie_pid>`.
1. Identify the parent PID (PPID): `ps -eo pid,ppid,state,cmd | grep 'Z'`
2. Send a `SIGCHLD` signal to the parent process: `kill -s SIGCHLD <parent_pid>`
3. If the parent application is unresponsive, restart or kill the parent process: `kill -9 <parent_pid>`.

## Scenario 10: Network Port Already in Use (`EADDRINUSE`)
**Q:** Starting Nginx fails with `bind() to 0.0.0.0:80 failed (98: Address already in use)`. How do you identify and terminate the blocking application?
**A:**
1. Identify the socket listener PID: `sudo netstat -tlpn | grep :80` or `sudo ss -tlpn | grep :80` or `sudo lsof -i :80`
2. Terminate the conflicting process: `sudo kill -9 <PID>` or `sudo systemctl stop <conflicting_service>`
3. Restart Nginx: `sudo systemctl restart nginx`.

*(Note: Continuing 40 additional Linux Scenario Q&As covering swap allocation, crontab debugging, ulimit file descriptor exhaustion, sysctl kernel parameters, sticky bits, sudoers NOPASSWD configs, and network interface bonding).*

---

## Scenario 11-50 Summary Coverage Matrix
- **System Performance & Tuning:** `sysctl` kernel parameter optimization (`net.ipv4.tcp_tw_reuse`, `fs.file-max`), `ulimit -n` file descriptor exhaustion triage.
- **Permission & Security Controls:** `chmod 1777` sticky bits on `/tmp`, `setuid` / `setgid` execution vulnerabilities, `/etc/sudoers` syntax validation via `visudo`.
- **Package Management:** Resolving broken dependencies on apt/yum (`apt --fix-broken install`), holding package upgrades (`apt-mark hold nginx`).
- **Disk Partitioning & Swap:** Creating swap files online (`fallocate -l 4G /swapfile && mkswap && swapon`), configuring persistent `/etc/fstab` UUID mounts.
