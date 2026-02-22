#!/usr/bin/env python3
"""
Aegis Labyrinth - Complete Demo Test Script
Run this to verify all components are working
"""

import requests
import time
import os
import sys

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"

def print_header(text):
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)

def print_result(test_name, success, message=""):
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status} - {test_name}")
    if message:
        print(f"      {message}")

def test_backend_connection():
    """Test if backend is reachable"""
    try:
        r = requests.get(f"{BACKEND_URL}/status", timeout=2)
        return r.status_code == 200, r.json()
    except:
        return False, None

def test_frontend_connection():
    """Test if frontend is reachable"""
    try:
        r = requests.get(FRONTEND_URL, timeout=2)
        return r.status_code == 200, None
    except:
        return False, None

def test_lock_endpoint():
    """Test manual lock endpoint"""
    try:
        r = requests.post(f"{BACKEND_URL}/lock", timeout=2)
        return r.status_code == 200, r.json()
    except:
        return False, None

def test_unlock_endpoint():
    """Test unlock endpoint"""
    try:
        r = requests.post(f"{BACKEND_URL}/unlock", timeout=2)
        return r.status_code == 200, r.json()
    except:
        return False, None

def test_login_attempt():
    """Test login attempt endpoint"""
    try:
        data = {
            "username": "test_user",
            "password": "wrong_password",
            "ip": "192.168.1.100"
        }
        r = requests.post(f"{BACKEND_URL}/login-attempt", json=data, timeout=2)
        return r.status_code == 200, r.json()
    except:
        return False, None

def test_status_updates():
    """Test if status updates after lock/unlock"""
    try:
        # Get initial status
        r1 = requests.get(f"{BACKEND_URL}/status")
        initial = r1.json()
        
        # Lock the system
        requests.post(f"{BACKEND_URL}/lock")
        time.sleep(1)
        
        # Get status after lock
        r2 = requests.get(f"{BACKEND_URL}/status")
        after_lock = r2.json()
        
        # Unlock
        requests.post(f"{BACKEND_URL}/unlock")
        time.sleep(1)
        
        # Get final status
        r3 = requests.get(f"{BACKEND_URL}/status")
        after_unlock = r3.json()
        
        return (after_lock.get('is_locked') == True and 
                after_unlock.get('is_locked') == False), {
            "initial": initial,
            "after_lock": after_lock,
            "after_unlock": after_unlock
        }
    except:
        return False, None

def main():
    print_header("AEGIS LABYRINTH - DEMO TEST SUITE")
    print("Make sure all terminals are running:")
    print("  Terminal 1: Backend (uvicorn)")
    print("  Terminal 2: Frontend (npm run dev)")
    print("  Terminal 3: Hardware daemon")
    print("\nStarting tests...\n")
    
    # Test 1: Backend connection
    success, data = test_backend_connection()
    print_result("Backend connection", success, 
                f"Status: {data.get('is_locked')} / Threat: {data.get('threat_level')}" if success else "")
    
    # Test 2: Frontend connection
    success, _ = test_frontend_connection()
    print_result("Frontend connection", success)
    
    # Test 3: Lock endpoint
    success, data = test_lock_endpoint()
    print_result("Lock endpoint", success, f"Response: {data}" if success else "")
    
    # Test 4: Status after lock
    time.sleep(1)
    r = requests.get(f"{BACKEND_URL}/status")
    data = r.json()
    print_result("System locked", data.get('is_locked') == True,
                f"Locked: {data.get('is_locked')}, Threat: {data.get('threat_level')}")
    
    # Test 5: Unlock endpoint
    success, data = test_unlock_endpoint()
    print_result("Unlock endpoint", success, f"Response: {data}" if success else "")
    
    # Test 6: Status after unlock
    time.sleep(1)
    r = requests.get(f"{BACKEND_URL}/status")
    data = r.json()
    print_result("System unlocked", data.get('is_locked') == False,
                f"Locked: {data.get('is_locked')}, Threat: {data.get('threat_level')}")
    
    # Test 7: Login attempt
    success, data = test_login_attempt()
    print_result("Login attempt endpoint", success, 
                f"AI Analysis: {data.get('analysis_result', {}).get('summary', 'N/A')[:50]}..." if success else "")
    
    # Test 8: Final status
    success, data = test_backend_connection()
    print_result("Final backend status", success,
                f"System ready - Locked: {data.get('is_locked')}" if success else "")
    
    print_header("MANUAL TESTS")
    print("1. Look at Terminal 3 - Hardware daemon should show activity")
    print("2. Listen for buzzer pattern when locked")
    print("3. Press physical button - should unlock and beep")
    print("4. Visit http://localhost:5173 in browser")
    print("5. Check admin page at http://localhost:5173/admin")
    print("6. Run attack: python3 burp-test.py")
    
    print_header("DEMO READY CHECK")
    all_passed = all([
        test_backend_connection()[0],
        test_frontend_connection()[0],
        test_lock_endpoint()[0],
        test_unlock_endpoint()[0]
    ])
    
    if all_passed:
        print("✅✅✅ ALL SYSTEMS GO! Your demo is ready! ✅✅✅")
        print("\nQuick demo flow:")
        print("1. Show homepage → http://localhost:5173")
        print("2. Go to /admin")
        print("3. Run: curl -X POST http://localhost:8000/lock")
        print("4. Buzzer pattern starts → 'System locked'")
        print("5. Press physical button → Unlocks")
        print("6. 'Physical authentication required – can't bypass remotely'")
    else:
        print("❌ Some tests failed. Check the outputs above.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTests interrupted.")
        sys.exit(0)
