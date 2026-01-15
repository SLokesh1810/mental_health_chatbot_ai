import requests
import json
import time

def comprehensive_test():
    print("🧪 Comprehensive Mental Health Chatbot Test")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:8000"
    
    # Test endpoints
    endpoints = ["/", "/info", "/health"]
    for endpoint in endpoints:
        try:
            resp = requests.get(f"{base_url}{endpoint}", timeout=5)
            print(f"✅ {endpoint}: {resp.status_code}")
            if endpoint == "/info":
                info = resp.json()
                print(f"   Model: {info.get('model')}")
                print(f"   Free: {info.get('free_tier')}")
        except Exception as e:
            print(f"❌ {endpoint}: Failed - {e}")
    
    print("\n💬 Testing Chat Responses:")
    print("-" * 30)
    
    test_cases = [
        "I'm feeling overwhelmed with work",
        "Can you suggest some relaxation techniques?",
        "I've been having trouble sleeping",
        "How can I practice mindfulness?",
        "I feel lonely sometimes"
    ]
    
    for i, message in enumerate(test_cases, 1):
        print(f"\n{i}. User: {message}")
        try:
            start_time = time.time()
            resp = requests.post(
                f"{base_url}/chat",
                json={"message": message},
                timeout=10
            )
            response_time = time.time() - start_time
            
            if resp.status_code == 200:
                data = resp.json()
                print(f"   🤖 Bot: {data['reply']}")
                print(f"   ⏱️  Response time: {response_time:.2f}s")
                print(f"   📊 Status: {data['status']}")
            else:
                print(f"   ❌ Error: {resp.status_code} - {resp.text}")
                
        except Exception as e:
            print(f"   💥 Request failed: {e}")
        
        time.sleep(1)  # Be respectful to the API

if __name__ == "__main__":
    comprehensive_test()