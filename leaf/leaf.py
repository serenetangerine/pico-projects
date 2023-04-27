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


def render(sprite):
    oled.fill(0)
    oled.blit(sprite, 0, 0)
    oled.show()


# initialize the display
width = 128
height = 64
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
oled = SSD1306_I2C(width, height, i2c)


def main():
    # load sprites into memory
    leaf = load_sprite('leaf.pbm', 16)
    render(leaf)



if __name__ == '__main__':
    main()