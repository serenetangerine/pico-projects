from machine import ADC, Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf

from random import randint
from time import sleep

import gc


class Tomo:
    def __init__(self):
        # load sprites
        with open('tomor.pbm', 'rb') as t:
            t.readline()
            t.readline()
            t.readline()
            self.tomor = bytearray(t.read())
        with open('tomol.pbm', 'rb') as t:
            t.readline()
            t.readline()
            t.readline()
            self.tomol = bytearray(t.read())
        with open('burger.pbm', 'rb') as b:
            b.readline()
            b.readline()
            b.readline()
            self.burger = bytearray(b.read())
        self.dir = 1
        self.x = 64
        self.y = 32
        self.sprite = self.tomor

    def walk(self):
        self.dir = randint(0, 1)
        if self.dir == 0:
            if self.x <= 96:
                self.sprite = self.tomol
                self.x = self.x + 2
            else:
                print('wall')
        else:
            if self.x >= 0:
                self.sprite = self.tomor
                self.x = self.x - 2
            else:
                print('wall')
        if self.x % 3 == 0:
            self.y = 32
        else:
            self.y = 30 
        self.render()

    def render(self):
        oled.fill(0)
        tomo = framebuf.FrameBuffer(self.sprite, 32, 32, framebuf.MONO_HLSB)
        oled.blit(tomo, self.x, self.y)
        oled.show()
        sleep(0.5)

# turn on LED so we know the pico is powered on
led = Pin(25, Pin.OUT)
led.on()

# initialize screen
width = 128
height = 64

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
oled = SSD1306_I2C(width, height, i2c)

tomo = Tomo()
while True:
    #gc.collect()
    #mem = 1 - (gc.mem_free() / 270336)
    #print(str(mem))
    tomo.walk()
