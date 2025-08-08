#!/usr/bin/env python3
"""
Test script for the Insurance Claims Processing API
"""

import requests
import json
import time

def test_api_health():
    """Test the health endpoint."""
    try:
        response = requests.get("http://127.0.0.1:8000/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure it's running on port 8000")
        return False

def test_supported_languages():
    """Test the supported languages endpoint."""
    try:
        response = requests.get("http://127.0.0.1:8000/supported-languages")
        if response.status_code == 200:
            print("✅ Supported languages endpoint working")
            languages = response.json()["languages"]
            print(f"Supported languages: {list(languages.keys())}")
            return True
        else:
            print(f"❌ Supported languages failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API")
        return False

def test_claim_processing():
    """Test the claim processing endpoint."""
    try:
        # Create a sample policy document
        sample_policy = """
        Insurance Policy Document

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
           - Cashless facility available at network hospitals
        """
        
        # Prepare the request
        files = {
            'file': ('policy.txt', sample_policy, 'text/plain')
        }
        data = {
            'query': '46-year-old male, knee surgery in Pune, 3-month-old insurance policy'
        }
        
        print("🔄 Testing claim processing...")
        response = requests.post(
            "http://127.0.0.1:8000/process-claim",
            files=files,
            data=data,
            timeout=60  # 60 second timeout
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Claim processing successful!")
            print(f"Decision: {result.get('Decision', 'N/A')}")
            print(f"Amount: {result.get('Amount', 'N/A')}")
            print(f"Confidence: {result.get('Confidence', 'N/A')}")
            print(f"Language: {result.get('Language', 'N/A')}")
            print(f"Relevant Clauses: {len(result.get('RelevantClauses', []))}")
            return True
        else:
            print(f"❌ Claim processing failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API")
        return False
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error testing claim processing: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("INSURANCE API TESTING")
    print("=" * 60)
    
    # Wait a moment for API to be ready
    print("Waiting for API to be ready...")
    time.sleep(2)
    
    tests = [
        ("Health Check", test_api_health),
        ("Supported Languages", test_supported_languages),
        ("Claim Processing", test_claim_processing)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        if test_func():
            passed += 1
        print("-" * 40)
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the API logs for details.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
