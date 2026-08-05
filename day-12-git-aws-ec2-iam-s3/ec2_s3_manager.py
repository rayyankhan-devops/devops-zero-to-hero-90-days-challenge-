#!/usr/bin/env python3
# ==============================================================================
# Script Name: ec2_s3_manager.py
# Description: Automates EC2 auditing and S3 bucket operations using Python.
# Author:      Muhammad Rayyan
# ==============================================================================

import sys

def audit_ec2_instances():
    print("[*] Auditing EC2 Instance configurations...")
    mock_instances = [
        {"id": "i-0123456789abcdef0", "type": "t2.micro", "state": "running", "subnet": "subnet-public-1a"},
        {"id": "i-0fe43210987654321", "type": "t3.medium", "state": "stopped", "subnet": "subnet-private-1b"}
    ]
    print("------------------------------------------------------------")
    print(f"{'Instance ID':<22} {'Type':<12} {'State':<10} {'Subnet'}")
    print("------------------------------------------------------------")
    for inst in mock_instances:
        state_icon = "🟢" if inst["state"] == "running" else "🔴"
        print(f"{inst['id']:<22} {inst['type']:<12} {state_icon} {inst['state']:<8} {inst['subnet']}")
    print("")

def audit_s3_buckets():
    print("[*] Auditing S3 Buckets and Security policies...")
    mock_buckets = [
        {"name": "rayyan-devops-backups", "region": "us-east-1", "public_access": False, "versioning": True},
        {"name": "app-static-assets-2026", "region": "us-east-1", "public_access": True, "versioning": True}
    ]
    print("------------------------------------------------------------")
    print(f"{'Bucket Name':<28} {'Region':<12} {'Public Access':<15} {'Versioning'}")
    print("------------------------------------------------------------")
    for b in mock_buckets:
        pub_status = "⚠️ Allowed" if b["public_access"] else "🔒 Blocked"
        ver_status = "🟢 Enabled" if b["versioning"] else "🔴 Disabled"
        print(f"{b['name']:<28} {b['region']:<12} {pub_status:<15} {ver_status}")
    print("")

def main():
    print("============================================================")
    print("              AWS EC2 & S3 MANAGEMENT SUITE                 ")
    print("============================================================")
    audit_ec2_instances()
    audit_s3_buckets()
    print("============================================================")

if __name__ == "__main__":
    main()
