#!/usr/bin/env python3
"""
Startup script for the Insurance Claims Processing API
"""

import subprocess
import sys
import os
import time
import signal
import threading

def run_python_api():
    """Run the Python insurance API."""
    try:
        print("Starting Insurance Claims Processing API...")
        print("API will be available at: http://127.0.0.1:8000")
        print("Health check: http://127.0.0.1:8000/health")
        print("Supported languages: http://127.0.0.1:8000/supported-languages")
        print("\nPress Ctrl+C to stop the API")
        print("-" * 50)
        
        # Run the insurance API
        process = subprocess.Popen([
            sys.executable, "insurance_api.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        
        # Stream output
        for line in process.stdout:
            print(line.rstrip())
            
    except KeyboardInterrupt:
        print("\nShutting down API...")
        if 'process' in locals():
            process.terminate()
            process.wait()
    except Exception as e:
        print(f"Error running API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Check if required files exist
    if not os.path.exists("insurance_api.py"):
        print("Error: insurance_api.py not found!")
        print("Please ensure you're in the correct directory.")
        sys.exit(1)
    
    # Check if required packages are installed
    required_packages = [
        "fastapi", "uvicorn", "sentence-transformers", 
        "transformers", "torch", "pdfplumber", "python-docx",
        "pdf2image", "pytesseract", "langdetect", "nltk"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("Missing required packages:")
        for package in missing_packages:
            print(f"  - {package}")
        print("\nInstall them with:")
        print(f"pip install {' '.join(missing_packages)}")
        sys.exit(1)
    
    # Run the API
    run_python_api()
