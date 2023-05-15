from machine import ADC, Pin, I2C
from ssd1306 import SSD1306_I2C
from framebuf import FrameBuffer, MONO_HLSB

from random import randint
from time import sleep

# required for uptime for tick counts for animations and such
from battery import Battery
bat = Battery(0.5)


def debug():
    import gc
    gc.collect()
    mem = 1 - (gc.mem_free() / 270336)
    print(str(mem))



class Leaf:
    def __init__(self):
        # easy access parameters
        self.tick_rate = 0.5

        # initialize the display
        self.width = 128
        self.height = 64
        self.i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
        self.oled = SSD1306_I2C(self.width, self.height, self.i2c)

        # load sprites
        self.plant1 = self.load_sprite('sprites/plant1.pbm', 32)
        self.plant2 = self.load_sprite('sprites/plant2.pbm', 32)
        
        # set starting position and sprite
        self.x = randint(0,96)
        self.y = 32
        self.sprite = self.plant1

        # parameters for the animation loop
        self.animation_stage = 0
        self.animation_steps = 2

        # start loop
        self.loop()
    

    def tick(self):
        # process all checks and rolls for tick changes 
        # and process animation changes
        self.animation_stage = (self.animation_stage + 1) % self.animation_steps
        self.sun_status = bat.checkCharging()
        self.bounce()
        self.render()


    # backend methods for the game engine
    def load_sprite(self, file, size):
        with open(file, 'rb') as f:
            # skip over metadata
            for i in range(3):
                f.readline()
            data = bytearray(f.read())
            return FrameBuffer(data, size, size, MONO_HLSB)
    

    # animations and drawing to screen
    def bounce(self):
        # check the uptime from the battery library to determine which
        # sprite of the plant to use
        if self.animation_stage % 2 == 0:
            self.sprite = self.plant1
        else:
            self.sprite = self.plant2


    def render(self):
        debug()
        # blank out the screen
        self.oled.fill(0)

        # render HUD top 
        if bat.uptime / 60 < 1:
            time_display = float(bat.uptime)
            time_unit = 'sec'
        elif bat.uptime / (60 * 60) < 1:
            time_display = float(bat.uptime / 60)
            time_unit = 'min'
        elif bat.uptime / (60 * 60 * 24) < 1:
            time_display = float(bat.uptime / (60 * 60))
            time_unit = 'hours'
        else: 
            time_display = float(bat.uptime / (60 * 60 * 24))
            time_unit = 'days'
            
        self.oled.text('%.2f %s' % (time_display, time_unit), 0, 3)
        self.oled.text('%s%%' % str(int(bat.percentage)), 88, 3)

        # render sun in HUD
        if self.sun_status:
            sun_message = 'sun'
        else:
            sun_message = 'moon'
        self.oled.text(sun_message, 0, 18) 

        # render plant
        self.oled.blit(self.sprite, self.x, self.y)

        # draw screen
        self.oled.show()
    

    def loop(self):
        while True:
            self.tick()
            sleep(self.tick_rate)



def main():
    leaf = Leaf()



if __name__ == '__main__':
    main()