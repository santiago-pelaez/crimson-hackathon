#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import requests

BUTTON_PIN = 17
BUZZER_PIN = 18
API_URL = "http://localhost:8000"

class AegisDaemon:
    def __init__(self):
        self.setup_gpio()
        self.last_locked_state = None
        self.button_pressed = False

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(BUZZER_PIN, GPIO.OUT)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

    def play_lock_pattern(self):
        for _ in range(3):
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(0.1)
        time.sleep(0.3)
        for _ in range(3):
            GPIO.output(BUZZER_PIN, GPIO.HIGH)
            time.sleep(0.1)
            GPIO.output(BUZZER_PIN, GPIO.LOW)
            time.sleep(0.1)

    def play_unlock_pattern(self):
        GPIO.output(BUZZER_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(BUZZER_PIN, GPIO.LOW)

    def check_api_status(self):
        try:
            r = requests.get(f"{API_URL}/status", timeout=2)
            if r.status_code == 200:
                data = r.json()
                return data.get('is_locked', False)
        except Exception as e:
            print(f"Status check error: {e}")
        return None

    def unlock_via_api(self):
        try:
            r = requests.post(f"{API_URL}/unlock", timeout=2)
            if r.status_code == 200:
                print("Unlock API call successful")
                self.play_unlock_pattern()
            else:
                print(f"Unlock failed: {r.text}")
        except Exception as e:
            print(f"API error: {e}")

    def run(self):
        print("Aegis Hardware Daemon started (API-polling mode)")
        print(f"Monitoring button on GPIO {BUTTON_PIN}")
        print(f"Buzzer on GPIO {BUZZER_PIN}")
        try:
            while True:
                current_locked = self.check_api_status()
                if current_locked is not None:
                    if self.last_locked_state is not None and current_locked and not self.last_locked_state:
                        print("System just locked – playing alert")
                        self.play_lock_pattern()
                    self.last_locked_state = current_locked

                if GPIO.input(BUTTON_PIN) == GPIO.LOW and not self.button_pressed:
                    self.button_pressed = True
                    print("Button pressed – attempting unlock")
                    self.unlock_via_api()
                    time.sleep(0.3)
                elif GPIO.input(BUTTON_PIN) == GPIO.HIGH:
                    self.button_pressed = False

                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nShutting down daemon")
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    daemon = AegisDaemon()
    daemon.run()
