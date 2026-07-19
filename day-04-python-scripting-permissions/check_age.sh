#!/bin/bash
# ==============================================================================
# Script Name: check_age.sh
# Description: Demonstrates Bash conditionals, inputs, and validation checks.
# Author:      Muhammad Rayyan
# ==============================================================================

set -euo pipefail

name="Rayyan"

echo "=== Bash Conditional & Input Practice ==="

# Read interactive user input
read -p "Enter your age: " input_age

# Remove any leading or trailing whitespace
age=$(echo "$input_age" | xargs)

# Validate if the input is an integer (uses regex)
if [[ ! "$age" =~ ^-?[0-9]+$ ]]; then
    echo "Error: Input must be a valid integer."
    exit 1
fi

# Logic checks
if [ "$age" -ge 18 ]; then
    echo "Welcome $name! You are allowed."
elif [ "$age" -gt 0 ]; then
    echo "You are young."
else
    echo "Error: Age must be a positive integer."
    exit 1
fi
