#!/usr/bin/env python3
# ==============================================================================
# Script Name: jira_simulator.py
# Description: Simulates Jira Agile Sprint workflow and Fibonacci story points.
# Author:      Muhammad Rayyan
# ==============================================================================

class JiraIssue:
    def __init__(self, key, summary, issue_type="Story", points=3):
        self.key = key
        self.summary = summary
        self.issue_type = issue_type
        self.points = points
        self.status = "To Do"

    def transition(self, new_status):
        old_status = self.status
        self.status = new_status
        print(f"  [Jira] Ticket {self.key} moved: '{old_status}' -> '{new_status}'")

def calculate_fibonacci_sequence(n):
    sequence = [0, 1]
    while len(sequence) < n:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

def main():
    print("============================================================")
    print("                JIRA AGILE SPRINT SIMULATOR                 ")
    print("============================================================")
    
    # 1. Fibonacci story points
    fibs = calculate_fibonacci_sequence(8)
    print(f"[*] Agile Fibonacci Estimation Scale: {fibs[2:]}")
    print("")
    
    # 2. Create Jira issues under an Epic
    print("[*] Epic: [DEV-100] Deploy Microservices E-Commerce Stack")
    issue1 = JiraIssue("DEV-101", "Create Dockerfile for Go Backend", "Task", points=3)
    issue2 = JiraIssue("DEV-102", "Configure Postgres Database Volume", "Task", points=5)
    
    print(f"  [+] Issue Created: [{issue1.key}] {issue1.summary} ({issue1.points} pts)")
    print(f"  [+] Issue Created: [{issue2.key}] {issue2.summary} ({issue2.points} pts)")
    print("")
    
    # 3. Sprint transitions
    print("[*] Simulating Active Sprint Progress:")
    issue1.transition("In Progress")
    issue1.transition("Testing")
    issue1.transition("Done")
    issue2.transition("In Progress")
    print("============================================================")

if __name__ == "__main__":
    main()
