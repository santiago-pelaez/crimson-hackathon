#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time

BUTTON = 17
BUZZER = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUZZER, GPIO.OUT)

print("Buzzer test: 3 short beeps")
for _ in range(3):
    GPIO.output(BUZZER, GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output(BUZZER, GPIO.LOW)
    time.sleep(0.1)

print("Press the button within 10 seconds...")
start = time.time()
while time.time() - start < 10:
    if GPIO.input(BUTTON) == GPIO.LOW:
        print("Button pressed! Playing long beep.")
        GPIO.output(BUZZER, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(BUZZER, GPIO.LOW)
        break
    time.sleep(0.1)
else:
    print("No button press detected.")

GPIO.cleanup()
