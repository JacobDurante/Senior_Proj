from machine import Pin 
import time

pin = Pin(25, Pin.OUT)

while True:
    print("toggling LED on")
    pin.high()
    time.sleep_ms(1000)
    print("toggling LED off")
    pin.low()
    time.sleep_ms(1000)