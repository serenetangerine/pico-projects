from machine import Pin


# turn on LED so we know the pico is powered on
led = Pin(15, Pin.OUT)
led.on()
