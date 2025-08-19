"""
Manual API Testing Script
========================

Test your LaughRx API with different symptoms manually.
"""

import requests
import json

def test_symptom(symptom_text):
    """Test a specific symptom"""
    url = "http://localhost:8000/analyze"
    data = {"symptoms": symptom_text}
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            result = response.json()
            print(f"🎭 SYMPTOM: {symptom_text}")
            print("=" * 60)
            print(result["response"])
            print("=" * 60)
            return True
        else:
            print(f"❌ Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def main():
    """Test various symptoms"""
    print("🧪 LaughRx API Manual Testing")
    print("=" * 60)
    print("Testing your live API with different symptoms...")
    print("=" * 60)
    
    # Test cases
    symptoms = [
        "I have a severe headache and nausea",
        "I've been coughing for 3 days",
        "My knee hurts when I walk",
        "I can't concentrate and feel anxious",
        "I have chest pain and shortness of breath"
    ]
    
    for i, symptom in enumerate(symptoms, 1):
        print(f"\n🧪 TEST {i}:")
        success = test_symptom(symptom)
        if not success:
            print("⚠️ API might not be running. Start with: python run_server.py")
            break
        print("\n" + "="*60)
    
    print("\n🎉 Manual testing complete!")
    print("\n🔗 Try these URLs in your browser:")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/health")
    print("📋 Examples: http://localhost:8000/examples")

if __name__ == "__main__":
    main()