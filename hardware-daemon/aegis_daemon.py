import RPi.GPIO as GPIO
import requests
import time

# Pins
BUZZER_PIN = 18    # Buzzer on D18
BUTTON_PIN = 17    # Button on GPIO 17

# Backend endpoints
BACKEND_URL = "http://localhost:8000/status"
UNLOCK_URL = "http://localhost:8000/unlock"

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

last_locked = None
last_button = GPIO.HIGH

def beep(times=1, duration=0.1):
    for _ in range(times):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(duration)
        GPIO.output(BUZZER_PIN, GPIO.LOW)
        time.sleep(duration)

print("=" * 50)
print("AEGIS HARDWARE DAEMON - BUZZER EDITION")
print("=" * 50)
print(f"Buzzer: GPIO {BUZZER_PIN}")
print(f"Button: GPIO {BUTTON_PIN}")
print(f"Backend: {BACKEND_URL}")
print("Press Ctrl+C to stop")
print("=" * 50)

try:
    while True:
        # Fetch status from backend
        try:
            r = requests.get(BACKEND_URL, timeout=2)
            data = r.json()
            locked = data.get('is_locked', False)
            
            if last_locked is not None and locked != last_locked:
                if locked:
                    print("🔒 SYSTEM LOCKED – two beeps")
                    beep(2, 0.2)
                else:
                    print("🔓 SYSTEM UNLOCKED – one long beep")
                    beep(1, 0.5)
            last_locked = locked
            
        except requests.exceptions.ConnectionError:
            print("⚠️  Backend not reachable - waiting...")
        except Exception as e:
            print(f"⚠️  Status error: {e}")

        # Check button press
        button = GPIO.input(BUTTON_PIN)
        if button == GPIO.LOW and last_button == GPIO.HIGH:
            print("👉 Button pressed – sending unlock request")
            try:
                r = requests.post(UNLOCK_URL, timeout=2)
                if r.status_code == 200:
                    print("✅ Unlock successful")
                    beep(1, 0.1)  # quick confirmation beep
                else:
                    print(f"❌ Unlock failed: {r.status_code}")
            except Exception as e:
                print(f"❌ Unlock error: {e}")
            time.sleep(0.2)
            
        last_button = button
        time.sleep(1)

except KeyboardInterrupt:
    print("\n👋 Shutting down...")
    GPIO.cleanup()
    print("Done.")