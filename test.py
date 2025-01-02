import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    state = GPIO.input(11)
    print(f"GPIO4 state: {state}")
    time.sleep(1)
