#!/usr/bin/env python3
# ==============================================================================
# Script Name: api_client_requests.py
# Description: Connects and parses REST APIs using Python's requests library.
# Author:      Muhammad Rayyan
# ==============================================================================

import sys

# Validate if 'requests' package is installed before execution
try:
    import requests
except ImportError:
    print("🚨 ERROR: The 'requests' library is required but not installed.")
    print("Please install it by running: pip install requests")
    sys.exit(1)

def fetch_mock_users():
    url = "https://jsonplaceholder.typicode.com/users"
    print(f"[*] Dispatching GET Request to: {url}...")
    
    try:
        # Fetch REST payload with a 10s connection timeout
        response = requests.get(url, timeout=10)
        
        # Check HTTP response status codes
        print(f"[+] HTTP Status Code: {response.status_code}")
        
        if response.status_code == 200:
            users = response.json()
            print(f"🟢 Successfully retrieved {len(users)} users.")
            print("\nDisplaying first 3 users:")
            print("-" * 52)
            for user in users[:3]:
                print(f"ID:    {user['id']}")
                print(f"Name:  {user['name']}")
                print(f"Email: {user['email']}")
                print(f"City:  {user['address']['city']}")
                print("-" * 52)
        else:
            print(f"🔴 Abnormal server response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("🔴 ERROR: Connection timeout reached.")
    except requests.exceptions.RequestException as e:
        print(f"🔴 ERROR: Connection failed. Detail: {str(e)}")

def main():
    print("====================================================")
    print("            PYTHON API REQUESTS PRACTICE            ")
    print("====================================================")
    
    fetch_mock_users()
    
    print("====================================================")

if __name__ == "__main__":
    main()
