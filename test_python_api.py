import requests
import json

def test_python_api():
    """Test the Python API directly"""
    
    # Test data
    test_query = "46-year-old male, knee surgery in Pune, 3-month-old insurance policy"
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

    try:
        # Create form data
        files = {
            'file': ('test_policy.txt', test_content, 'text/plain'),
            'query': (None, test_query)
        }
        
        print("Testing Python API...")
        print(f"Query: {test_query}")
        print(f"File content length: {len(test_content)} characters")
        
        # Make request to Python API
        response = requests.post(
            'http://127.0.0.1:8000/process',
            files=files,
            timeout=30
        )
        
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Python API is working!")
            print("Response:")
            print(json.dumps(result, indent=2))
            
            # Check if RelevantClauses exists and is an array
            if 'RelevantClauses' in result:
                if isinstance(result['RelevantClauses'], list):
                    print(f"✅ RelevantClauses is an array with {len(result['RelevantClauses'])} items")
                else:
                    print(f"❌ RelevantClauses is not an array: {type(result['RelevantClauses'])}")
            else:
                print("❌ RelevantClauses not found in response")
                
        else:
            print(f"❌ Python API returned error: {response.status_code}")
            print(f"Error response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Python API. Make sure insurance_api.py is running on port 8000")
    except Exception as e:
        print(f"❌ Error testing Python API: {e}")

if __name__ == "__main__":
    test_python_api()
