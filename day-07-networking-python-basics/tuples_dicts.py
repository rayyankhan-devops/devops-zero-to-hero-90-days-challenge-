#!/usr/bin/env python3
# ==============================================================================
# Script Name: tuples_dicts.py
# Description: Practices Python Tuples and Dictionaries for DevOps tasks.
# Author:      Muhammad Rayyan
# ==============================================================================

import sys

def test_tuples():
    print("------------------------------------------------------------")
    print("[+] PYTHON TUPLES (Ordered & Immutable)")
    print("------------------------------------------------------------")
    
    # Define tuple
    fruits = ("Apple", "Banana", "Orange")
    print(f"Fruits tuple: {fruits}")
    print(f"First element fruits[0]: {fruits[0]}")
    
    # Try modifying tuple (Demonstrate immutability & handling error)
    print("\n[!] Attempting to modify index [0] to test immutability:")
    try:
        # Tuples do not support assignment
        fruits[0] = "Grapes"
    except TypeError as e:
        print(f"    🟢 Caught expected error: {e}")
        print("    Info: Tuples cannot be modified once created (immutable).")
        
    # Unpacking Tuples
    print("\n[+] Tuple Unpacking Example:")
    ip_port = ("192.168.1.100", 8080)
    ip, port = ip_port
    print(f"    Unpacked Target -> IP: {ip}, Port: {port}")
    print("")

def test_dictionaries():
    print("------------------------------------------------------------")
    print("[+] PYTHON DICTIONARIES (Key-Value Mappings)")
    print("------------------------------------------------------------")
    
    # Define dictionary
    student = {
        "Name": "John",
        "Age": 22,
        "City": "New York"
    }
    print(f"Student dict: {student}")
    print(f"Accessing student['Name']: {student['Name']}")
    
    # Adding / Modifying Key-Values
    student["Role"] = "DevOps Intern"
    student["Age"] = 23
    print(f"Updated student dict: {student}")
    
    # Safe access using get() to avoid KeyErrors
    print("\n[+] Safe Key Access:")
    non_existent = student.get("GPA", "N/A")
    print(f"    Accessing non-existent key 'GPA': {non_existent}")
    
    # Iteration
    print("\n[+] Iterating through Dictionary Key-Values:")
    for key, val in student.items():
        print(f"    {key}: {val}")
    print("")

def main():
    print("============================================================")
    print("             TUPLES & DICTIONARIES PRACTICE                 ")
    print("============================================================")
    
    test_tuples()
    test_dictionaries()
    
    print("============================================================")

if __name__ == "__main__":
    main()
