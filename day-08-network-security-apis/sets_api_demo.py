#!/usr/bin/env python3
# ==============================================================================
# Script Name: sets_api_demo.py
# Description: Demonstrates Python Sets operations and simulates API requests.
# Author:      Muhammad Rayyan
# ==============================================================================

import json
import time

def demo_sets():
    print("------------------------------------------------------------")
    print("[+] PYTHON SETS (Unordered & Unique Collections)")
    print("------------------------------------------------------------")
    
    # 1. Deduplication
    raw_ports = [80, 443, 80, 22, 443, 8080, 22]
    unique_ports = set(raw_ports)
    print(f"    Raw port list:   {raw_ports}")
    print(f"    Deduplicated Set: {unique_ports}")
    print("")
    
    # 2. Set Mathematics (VPC/Security Group analysis)
    allowed_security_group = {22, 80, 443}
    active_listening_ports = {80, 443, 8080}
    
    print(f"    Allowed Ports (Firewall): {allowed_security_group}")
    print(f"    Active Ports (Listening): {active_listening_ports}")
    
    # Intersection (Ports allowed and active)
    safe_active = allowed_security_group.intersection(active_listening_ports)
    print(f"    Intersection (Allowed & Active): {safe_active}")
    
    # Difference (Ports active but blocked by firewall)
    unprotected = active_listening_ports.difference(allowed_security_group)
    print(f"    Difference (Active but Blocked):  {unprotected}")
    
    # Union (All mapped ports)
    all_ports = allowed_security_group.union(active_listening_ports)
    print(f"    Union (Total Port Scope):        {all_ports}")
    print("")

def simulate_api_interaction():
    print("------------------------------------------------------------")
    print("[+] MOCK API REQUEST & RESPONSE LOGS")
    print("------------------------------------------------------------")
    
    # Client sends Request
    request_headers = {
        "Method": "GET",
        "Path": "/api/users/1",
        "Host": "api.example.com",
        "Accept": "application/json"
    }
    
    print("[Client] Sending Request:")
    print(f"    {request_headers['Method']} {request_headers['Path']} HTTP/1.1")
    print(f"    Host: {request_headers['Host']}")
    print(f"    Accept: {request_headers['Accept']}")
    print("    ...")
    
    time.sleep(0.5)
    
    # Server returns Response
    response_payload = {
        "status": 200,
        "headers": {
            "Content-Type": "application/json",
            "Server": "Nginx/1.22.0"
        },
        "body": {
            "id": 1,
            "name": "Muhammad Rayyan",
            "role": "DevOps Engineer",
            "skills": ["Linux", "AWS", "Python", "Networking"]
        }
    }
    
    print("\n[Server] Returned Response:")
    print(f"    HTTP/1.1 {response_payload['status']} OK")
    print(f"    Content-Type: {response_payload['headers']['Content-Type']}")
    print(f"    Server: {response_payload['headers']['Server']}")
    print("    Body payload:")
    print(json.dumps(response_payload["body"], indent=8))
    print("")

def main():
    print("============================================================")
    print("             SETS & API STRUCTURES PRACTICE                 ")
    print("============================================================")
    
    demo_sets()
    simulate_api_interaction()
    
    print("============================================================")

if __name__ == "__main__":
    main()
