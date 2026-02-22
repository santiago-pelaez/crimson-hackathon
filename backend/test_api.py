import requests

def test_security_system():
    print("🚀 Starting Unit Test: Security Breach Scenario")
    
    # Simulate 5 failed login attempts
    for i in range(5):
        payload = {
            "username": "hacker_man",
            "status": "failed",
            "ip": "99.99.99.99"
        }
        res = requests.post("http://localhost:8000/log-event", json=payload)
        print(f"Attempt {i+1}: {res.json()['analysis_result']['summary']}")

    # Check if system locked
    status = requests.get("http://localhost:8000/status").json()
    if status['is_locked']:
        print("✅ TEST PASSED: System locked successfully.")
    else:
        print("❌ TEST FAILED: System stayed open.")

if __name__ == "__main__":
    test_security_system()