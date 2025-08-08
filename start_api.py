#!/usr/bin/env python3
"""
Script to start the insurance_api.py with enhanced logging
"""

import subprocess
import sys
import os

def start_api():
    """Start the insurance API with enhanced output"""
    print("=" * 60)
    print("STARTING BAJAJBOT INSURANCE API")
    print("=" * 60)
    print("This will start the Python API on http://127.0.0.1:8000")
    print("You should see detailed logging output below:")
    print("=" * 60)
    print()
    
    try:
        # Check if insurance_api.py exists
        if not os.path.exists("insurance_api.py"):
            print("ERROR: insurance_api.py not found in current directory")
            print("Make sure you're in the correct directory")
            return
        
        # Start the API
        print("Starting insurance_api.py...")
        print("Press Ctrl+C to stop the API")
        print("-" * 60)
        
        # Run the API with subprocess to capture output
        process = subprocess.Popen(
            [sys.executable, "insurance_api.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Print output in real-time
        for line in iter(process.stdout.readline, ''):
            if line:
                print(line.rstrip())
        
        process.wait()
        
    except KeyboardInterrupt:
        print("\n" + "=" * 60)
        print("API stopped by user")
        print("=" * 60)
    except Exception as e:
        print(f"ERROR starting API: {e}")

if __name__ == "__main__":
    start_api()
