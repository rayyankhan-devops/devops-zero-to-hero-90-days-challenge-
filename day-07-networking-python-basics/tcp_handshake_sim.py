#!/usr/bin/env python3
# ==============================================================================
# Script Name: tcp_handshake_sim.py
# Description: Console-based TCP 3-Way Handshake connection state simulator.
#              Perfect for interview prep visualization.
# Author:      Muhammad Rayyan
# ==============================================================================

import time
import sys

def print_delay(text, delay=0.8):
    print(text)
    time.sleep(delay)

def simulate_handshake():
    print("=============================================================")
    print("                TCP 3-WAY HANDSHAKE SIMULATOR                ")
    print("=============================================================")
    
    # Starting States
    print_delay("[*] Server Initialization: Setting socket to state: [LISTEN]")
    print_delay("[*] Client Initialization: Preparing to connect to remote host...")
    print("-" * 61)
    
    # Step 1: SYN
    print_delay("\n[+] STEP 1: Client sends SYN (Synchronize)")
    print_delay("    [Client] ---- ( SYN = 1, Seq = 1000 ) ----> [Server]")
    print_delay("    [Client State]: Transition to [SYN-SENT]")
    print_delay("    [Server State]: Received SYN; Transition to [SYN-RECEIVED]")
    
    # Step 2: SYN-ACK
    print_delay("\n[+] STEP 2: Server replies with SYN-ACK (Synchronize-Acknowledge)")
    print_delay("    [Client] <---- ( SYN = 1, ACK = 1, Seq = 5000, Ack_Num = 1001 ) ---- [Server]")
    print_delay("    [Server State]: Waiting for final verification...")
    
    # Step 3: ACK
    print_delay("\n[+] STEP 3: Client sends ACK (Acknowledge)")
    print_delay("    [Client] ---- ( ACK = 1, Seq = 1001, Ack_Num = 5001 ) ----> [Server]")
    
    # Connection Established
    print_delay("\n[+] CONNECTION ESTABLISHED SUCCESSFULLY! 🎉")
    print_delay("    [Client State]: [ESTABLISHED]")
    print_delay("    [Server State]: [ESTABLISHED]")
    print_delay("    Connection: Ready for data transmission (HTTP, SSH, etc.)")
    print("=============================================================")

if __name__ == "__main__":
    try:
        simulate_handshake()
    except KeyboardInterrupt:
        print("\nSimulation aborted.")
        sys.exit(0)
