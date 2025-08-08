#!/usr/bin/env python3
"""
Test script to directly test the insurance_api.py functionality
This will help you see the output in the terminal
"""

import requests
import json
import os

def test_python_api():
    """Test the Python API directly"""
    print("=" * 60)
    print("TESTING PYTHON API DIRECTLY")
    print("=" * 60)
    
    # Test data
    test_query = "46-year-old male, knee surgery in Pune, 3-month-old insurance policy"
    
    # Create a simple test file content
    test_content = """Insurance Policy Document

This is a sample insurance policy document containing standard terms and conditions.

1. Hospitalization Coverage
   - Inpatient hospitalization is covered up to the sum insured
   - Pre and post hospitalization expenses are covered
   - Room rent and boarding expenses are covered

2. Waiting Periods
   - Pre-existing conditions: 36-month waiting period
   - Maternity benefits: 24-month waiting period
   - Specific diseases: 12-month waiting period

3. Exclusions
   - Cosmetic surgery
   - Dental treatment (except due to accident)
   - Treatment outside India (except emergency)

4. Claim Process
   - Submit claim within 30 days of discharge
   - Provide all medical documents
   - Cashless facility available at network hospitals"""
    
    # Save test content to a temporary file
    test_file_path = "test_policy.txt"
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(test_content)
    
    try:
        # Prepare the request
        url = "http://127.0.0.1:8000/process"
        
        with open(test_file_path, "rb") as f:
            files = {"file": ("test_policy.txt", f, "text/plain")}
            data = {"query": test_query}
            
            print(f"Sending request to: {url}")
            print(f"Query: {test_query}")
            print(f"File: {test_file_path}")
            print("-" * 60)
            
            # Make the request
            response = requests.post(url, files=files, data=data, timeout=60)
            
            print(f"Response status: {response.status_code}")
            print("-" * 60)
            
            if response.status_code == 200:
                result = response.json()
                print("SUCCESS! API Response:")
                print("=" * 60)
                print(json.dumps(result, indent=2, ensure_ascii=False))
                print("=" * 60)
                
                # Print key information
                print("\nKEY INFORMATION:")
                print(f"Decision: {result.get('Decision', 'N/A')}")
                print(f"Amount: {result.get('Amount', 'N/A')}")
                print(f"Relevant Clauses: {len(result.get('RelevantClauses', []))}")
                print(f"Query Details: {result.get('QueryDetails', {})}")
                
            else:
                print(f"ERROR: {response.status_code}")
                print(response.text)
                
    except requests.exceptions.ConnectionError:
        print("ERROR: Could not connect to Python API")
        print("Make sure insurance_api.py is running on http://127.0.0.1:8000")
        print("\nTo start the API, run:")
        print("python insurance_api.py")
        
    except Exception as e:
        print(f"ERROR: {e}")
        
    finally:
        # Clean up
        if os.path.exists(test_file_path):
            os.remove(test_file_path)
            print(f"\nCleaned up: {test_file_path}")

if __name__ == "__main__":
    test_python_api()
