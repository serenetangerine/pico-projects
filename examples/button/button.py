from machine import Pin
from time import sleep

led = Pin(25, Pin.OUT)
button = Pin(14, Pin.IN, Pin.PULL_DOWN)

led.on()

while True:
    if button.value():
        led.toggle()
        sleep(0.1)
