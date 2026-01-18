import requests
import os
import sys

# Add parent dir to path to import backend modules if needed, 
# but here we test the running API black-box style.

API_URL = "http://localhost:8000"

def test_health():
    print(f"Checking if API is reachable at {API_URL}...")
    try:
        # We don't have a health lookup, but let's try dashboard_data
        r = requests.get(f"{API_URL}/dashboard_data")
        if r.status_code == 200:
            print("✅ API is online.")
            return True
        else:
            print(f"❌ API returned {r.status_code}")
            return False
    except Exception as e:
        print(f"❌ Could not connect to API: {e}")
        return False

def test_upload():
    print("\nTesting CSV Upload...")
    # Create a dummy CSV
    csv_content = """timestamp,equipment_id,temp,vibration,pressure,failure_type
2023-11-01 10:00:00,TEST-EQ-01,70.5,15.1,100.2,0
2023-11-01 10:05:00,TEST-EQ-01,95.2,45.5,90.1,1
"""
    files = {'file': ('test_data.csv', csv_content, 'text/csv')}
    
    try:
        r = requests.post(f"{API_URL}/upload_csv", files=files)
        if r.status_code == 200:
            print(f"✅ Upload successful: {r.json()}")
        else:
            print(f"❌ Upload failed: {r.text}")
    except Exception as e:
        print(f"❌ Upload error: {e}")

def test_analysis():
    print("\nTesting Solar LLM Analysis (Mock check)...")
    # We will trigger analysis for TEST-EQ-01
    # Note: This will actually call the LLM if the key is valid.
    
    try:
        r = requests.post(f"{API_URL}/analyze/TEST-EQ-01")
        if r.status_code == 200:
            print("✅ Analysis successful!")
            print("Response preview:", str(r.json())[:200] + "...")
        else:
            print(f"❌ Analysis failed: {r.text}")
    except Exception as e:
        print(f"❌ Analysis error: {e}")

if __name__ == "__main__":
    print("=== AskUp PoC Integration Test ===\n")
    if test_health():
        test_upload()
        test_analysis()
    else:
        print("\nNOTE: Ensure the backend is running with 'uvicorn main:app --reload'")
