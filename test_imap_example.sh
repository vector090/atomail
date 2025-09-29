#!/bin/bash

# Example usage of test_imap.py with environment variables

# Method 1: Set environment variables and run
echo "Method 1: Using environment variables"
export IMAP_HOST="imap.126.com"
export IMAP_PORT="993"
export IMAP_USER="your-email@126.com"
export IMAP_PASSWORD="your-password-or-app-password"
python3 test_imap.py

# Method 2: Inline environment variables
echo -e "\nMethod 2: Inline environment variables"
IMAP_HOST="imap.gmail.com" \
IMAP_PORT="993" \
IMAP_USER="your-email@gmail.com" \
IMAP_PASSWORD="your-app-password" \
python3 test_imap.py

# Method 3: Interactive mode (will prompt for missing values)
echo -e "\nMethod 3: Interactive mode"
python3 test_imap.py