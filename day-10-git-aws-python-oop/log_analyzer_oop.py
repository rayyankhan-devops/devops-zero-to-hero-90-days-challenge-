#!/usr/bin/env python3
# ==============================================================================
# Script Name: log_analyzer_oop.py
# Description: Python OOP Log Analyzer for parsing server log metrics.
# Author:      Muhammad Rayyan
# ==============================================================================

import re
import sys

class LogAnalyzer:
    """Class representing a server log auditing engine."""
    
    def __init__(self, log_lines):
        self.log_lines = log_lines
        self.stats = {"INFO": 0, "WARNING": 0, "ERROR": 0, "CRITICAL": 0}
        self.errors_list = []
        
    def analyze(self):
        """Parse log lines and populate metrics."""
        for line in self.log_lines:
            line_str = line.strip()
            if not line_str:
                continue
                
            if "CRITICAL" in line_str:
                self.stats["CRITICAL"] += 1
                self.errors_list.append(line_str)
            elif "ERROR" in line_str:
                self.stats["ERROR"] += 1
                self.errors_list.append(line_str)
            elif "WARNING" in line_str:
                self.stats["WARNING"] += 1
            elif "INFO" in line_str:
                self.stats["INFO"] += 1

    def generate_report(self):
        """Print formatted audit report."""
        total = sum(self.stats.values())
        print("============================================================")
        print("                SERVER LOG ANALYSIS REPORT                  ")
        print("============================================================")
        print(f"Total Log Events Processed: {total}")
        print("------------------------------------------------------------")
        for level, count in self.stats.items():
            pct = (count / total * 100) if total > 0 else 0
            print(f"  {level:<10}: {count:>4} ({pct:>5.1f}%)")
        print("------------------------------------------------------------")
        print("Identified Error/Critical Logs:")
        if self.errors_list:
            for err in self.errors_list:
                print(f"  ❌ {err}")
        else:
            print("  🟢 No critical errors detected.")
        print("============================================================")

def main():
    sample_logs = [
        "2026-07-24 10:00:01 [INFO] Server Started on port 8080",
        "2026-07-24 10:01:15 [WARNING] High Memory Utilization (84%)",
        "2026-07-24 10:02:30 [ERROR] Database Connection Failed: timeout",
        "2026-07-24 10:03:00 [INFO] User login from 192.168.1.10",
        "2026-07-24 10:04:45 [CRITICAL] Kernel Panic: out of memory",
        "2026-07-24 10:05:00 [ERROR] Failed to write session to Redis"
    ]
    
    analyzer = LogAnalyzer(sample_logs)
    analyzer.analyze()
    analyzer.generate_report()

if __name__ == "__main__":
    main()
