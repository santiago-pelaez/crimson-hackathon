import requests
import time

BASE_URL = "http://127.0.0.1:8000"

def simulate_attack():
    print("🚀 Simulating Brute Force Attack...")
    attack_data = {
        "timestamp": "2026-02-21T20:45:00",
        "ip": "192.168.1.50",
        "event": "failed_login",
        "details": "Invalid password attempt for user 'admin' (Attempt 5 of 5)"
    }
    
    # 1. Send the attack log
    response = requests.post(f"{BASE_URL}/login-attempt", json=attack_data)
    print(f"Sent Log: {response.json()}")

    # 2. Check if system locked
    time.sleep(2) # Give AI a secc to think
    status = requests.get(f"{BASE_URL}/status").json()
    print(f"Current System State: {status}")

    if status["is_locked"]:
        print("SUCCESS: The AI detected the threat and LOCKED the system!")
    else:
        print("FAIL: The system is still open.")

if __name__ == "__main__":
    simulate_attack()