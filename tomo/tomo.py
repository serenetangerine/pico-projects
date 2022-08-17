from machine import ADC, Pin, I2C
from ssd1306 import SSD1306_I2C
from framebuf import FrameBuffer, MONO_HLSB

from random import randint
from time import sleep



def load_sprite(file, size):
    with open(file, 'rb') as f:
        # skip over metadata
        for i in range(3):
            f.readline()
        data = bytearray(f.read())
        return FrameBuffer(data, size, size, MONO_HLSB)

def debug():
    import gc
    gc.collect()
    mem = 1 - (gc.mem_free() / 270336)
    print(str(mem))


class Tomo:
    def __init__(self):
        # load sprites
        self.tomoR = load_sprite('tomor.pbm', 32)
        self.tomoL = load_sprite('tomol.pbm', 32)
        
        self.heartFull = load_sprite('heart-full.pbm', 16)
        self.heartHalf = load_sprite('heart-half.pbm', 16)
        self.heartEmpty = load_sprite('heart-empty.pbm', 16)

        self.dead = load_sprite('dead.pbm', 32)

        self.egg1 = load_sprite('egg1.pbm', 32)
        self.egg2 = load_sprite('egg2.pbm', 32)
        self.egg3 = load_sprite('egg3.pbm', 32)
        
        # set default values
        self.dir = 1
        self.x = 64
        self.y = 32
        self.health = 8
        self.sprite = self.tomoR

    def walk(self):
        self.dir = randint(0, 1)
        if self.dir == 0:
            if self.x <= 96:
                self.sprite = self.tomoL
                self.x = self.x + 2
        else:
            if self.x >= 0:
                self.sprite = self.tomoR
                self.x = self.x - 2
        if self.x % 3 == 0:
            self.y = 30
        else:
            self.y = 32 
        if randint(0, 9) == 0:
            self.health = self.health - 1
            if self.health < 0:
                self.health = 8
            #print(self.health)
        self.render()

    def render_hearts(self):
        for i in range(4):
            if self.health >= (i + 1) * 2:
                sprite = self.heartFull
            elif self.health >= i * 2 and self.health % 2 == 1:
                sprite = self.heartHalf
            else:
                sprite = self.heartEmpty
            oled.blit(sprite, i * 13, 0)

    def render(self):
        oled.fill(0)
        self.render_hearts()
        oled.blit(self.sprite, self.x, self.y)
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

# initialize Tomo and start loop
tomo = Tomo()
while True:
    debug()
    tomo.walk()
