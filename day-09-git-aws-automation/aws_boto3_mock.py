#!/usr/bin/env python3
# ==============================================================================
# Script Name: aws_boto3_mock.py
# Description: Demonstrates Boto3 AWS automation for S3 and EC2.
#              Simulates calls safely if actual credentials are not set up.
# Author:      Muhammad Rayyan
# ==============================================================================

import sys

# Try importing Boto3 package
BOTO3_AVAILABLE = False
try:
    import boto3
    from botocore.exceptions import NoCredentialsError, ClientError
    BOTO3_AVAILABLE = True
except ImportError:
    pass

def simulate_ec2_management():
    print("------------------------------------------------------------")
    print("[+] AWS EC2 AUTOMATION (Provisioning & Controlling)")
    print("------------------------------------------------------------")
    
    if BOTO3_AVAILABLE:
        try:
            # Try initializing client
            ec2 = boto3.client("ec2", region_name="us-east-1")
            print("[*] Retrieving active EC2 instances...")
            response = ec2.describe_instances()
            print("🟢 Connection Successful. Instances mapped:")
            print(response)
            return
        except (NoCredentialsError, ClientError) as e:
            print(f"[!] Active AWS credentials not configured ({str(e)}).")
            print("[*] Switching to local simulation mode...")
            
    # Mock Simulation output for interview practice
    print("[Simulated] Initializing Boto3 EC2 client...")
    print("[Simulated] Launching t2.micro EC2 Instance...")
    instance_mock = {
        "InstanceId": "i-0abcd1234efgh5678",
        "State": "pending",
        "ImageId": "ami-0c7217cdde317cfec",
        "LaunchTime": "2026-07-23 12:00:00"
    }
    print(f"🟢 [Simulated] Instance launched successfully:")
    print(f"    - ID:         {instance_mock['InstanceId']}")
    print(f"    - State:      {instance_mock['State']}")
    print(f"    - AMI Image:  {instance_mock['ImageId']}")
    print("")

def simulate_s3_management():
    print("------------------------------------------------------------")
    print("[+] AWS S3 BUCKETS AUTOMATION")
    print("------------------------------------------------------------")
    
    if BOTO3_AVAILABLE:
        try:
            s3 = boto3.client("s3")
            print("[*] Fetching S3 Buckets...")
            response = s3.list_buckets()
            print("🟢 Buckets found:")
            for bucket in response.get("Buckets", []):
                print(f"    - {bucket['Name']}")
            return
        except (NoCredentialsError, ClientError):
            pass
            
    print("[Simulated] Fetching S3 Buckets...")
    mock_buckets = ["rayyan-devops-backups", "app-prod-static-assets", "lambda-trigger-source"]
    print("🟢 [Simulated] Buckets found:")
    for b in mock_buckets:
        print(f"    - {b}")
    print("")

def main():
    print("============================================================")
    print("            AWS BOTO3 AUTOMATION PRACTICE                   ")
    print("============================================================")
    
    if not BOTO3_AVAILABLE:
        print("[!] Info: 'boto3' package is not installed globally.")
        print("    Run: pip install boto3 to practice with actual libraries.")
        print("")
        
    simulate_ec2_management()
    simulate_s3_management()
    
    print("============================================================")

if __name__ == "__main__":
    main()
