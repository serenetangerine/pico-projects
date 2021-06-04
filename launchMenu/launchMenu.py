from machine import ADC, I2C, Pin
from ssd1306 import SSD1306_I2C
from temp import temperatureLoop
from time import sleep


# turn on LED so we know the pico is powered on
led = Pin(25, Pin.OUT)
led.on()


# initialize buttons
upButton = Pin(14, Pin.IN, Pin.PULL_DOWN)
downButton = Pin(15, Pin.IN, Pin.PULL_DOWN)
enterButton = Pin(13, Pin.IN, Pin.PULL_DOWN)


# initialize screen
width = 128
height = 64

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
oled = SSD1306_I2C(width, height, i2c)

scripts = ['temp.py', 'osciliscope.py', 'heart.py']


def drawScreen(selection):
    oled.fill(0)
    oled.text('Select Program:', 0, 0)
    for i in range(len(scripts)):
        oled.text(scripts[i], 0, (15 * (i + 1)))
    oled.text('*', 0, (15 * selection))
    oled.show()


selection = 1
while True:
    if upButton.value():
        if selection > 1:
            selection -= selection
            drawScreen(selection)

    if downButton.value():
        if selection <= len(scripts):
            selection += selection
            drawScreen(selection)

    if enterButton.value():
        oled.fill(0)
        oled.text('Running %s' % scripts[selection - 1])
        oled.show()

    sleep(0.5)
        
