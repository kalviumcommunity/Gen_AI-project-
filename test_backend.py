"""
Test script for LaughRx backend
"""

import requests
import json

def test_backend():
    """Test all backend endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing LaughRx Backend API")
    print("=" * 50)
    
    # Test root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Root endpoint working")
            print(f"   Response: {response.json()['message']}")
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Root endpoint error: {e}")
    
    # Test health check
    print("\n2. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check: {data['status']}")
            print(f"   AI Status: {data['ai_status']}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test symptom analysis
    print("\n3. Testing symptom analysis...")
    try:
        test_data = {
            "symptoms": "I have a headache and feel tired"
        }
        response = requests.post(
            f"{base_url}/analyze",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Symptom analysis working")
            print(f"   Response preview: {data['response'][:100]}...")
        else:
            print(f"❌ Symptom analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Symptom analysis error: {e}")
    
    # Test quick advice
    print("\n4. Testing quick advice...")
    try:
        test_data = {
            "symptoms": "I have a runny nose"
        }
        response = requests.post(
            f"{base_url}/quick-advice",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Quick advice working")
            print(f"   Advice: {data['advice'][:100]}...")
        else:
            print(f"❌ Quick advice failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Quick advice error: {e}")
    
    print("\n🎉 Backend testing complete!")

if __name__ == "__main__":
    test_backend()
