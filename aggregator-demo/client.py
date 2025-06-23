import requests
import json
import sys

# Configuration
API_URL = "http://localhost:8000/v1/aggregate"
API_KEY = "secret123"

def call_aggregator():
    """Call the aggregator service and print the response"""
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        print("Calling aggregator service...")
        print(f"URL: {API_URL}")
        print(f"Headers: {headers}")
        print("-" * 50)
        
        response = requests.get(API_URL, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS - Aggregated data received:")
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ ERROR - Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR - Cannot connect to aggregator service")
        print("Make sure the FastAPI service is running on http://localhost:8000")
        print("Run: uvicorn main:app --reload")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("❌ ERROR - Request timed out")
        sys.exit(1)
    except Exception as e:
        print(f"❌ ERROR - Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    call_aggregator()
