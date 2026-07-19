#!/usr/bin/env python3
# ==============================================================================
# Script Name: check_age.py
# Description: Demonstrates Python conditionals and user input validation.
# Author:      Muhammad Rayyan
# ==============================================================================

import sys

def main():
    name = "Rayyan"
    
    print("=== Python Conditional & Input Practice ===")
    
    # Read user input from stdout
    try:
        user_input = input("Enter your age: ").strip()
        
        # Check if input is empty
        if not user_input:
            print("Error: Input age cannot be empty.")
            sys.exit(1)
            
        # Convert input string to integer
        age = int(user_input)
        
    except ValueError:
        print("Error: Please enter a valid integer numeric value for age.")
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):
        print("\nOperation cancelled by user.")
        sys.exit(0)

    # Business logic conditionals
    if age >= 18:
        print(f"Welcome {name}! You are allowed.")
    elif age > 0:
        print("You are young.")
    else:
        print("Error: Age must be a positive integer.")
        sys.exit(1)

if __name__ == "__main__":
    main()
