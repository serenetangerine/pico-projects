import time
from pimoroni import Button
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4

import _thread

class Buttons:
    def __init__(self, tick_rate):
        self.button_a = Button(12)
        self.button_b = Button(13)
        self.button_x = Button(14)
        self.button_y = Button(15)

        self.tick_rate = tick_rate
        self.queue = ''
    
    def read(self):
        value = self.queue
        self.queue = ''
        return value
    
    def tick(self):
        if self.button_a.read():
            self.queue = 'a'
        elif self.button_b.read():
            self.queue = 'b'
        elif self.button_x.read():
            self.queue = 'x'
        elif self.button_y.read():
            self.queue = 'y'
        time.sleep(self.tick_rate)
    
    def daemon(self):
        while True:
            self.tick()

    def daemonize(self):
        self.thread = _thread.start_new_thread(self.daemon, ())


def main():
    tick_rate = 0.1
    buttons = Buttons(tick_rate)
    buttons.daemonize()

    display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0)
    display.set_backlight(1)

    BLACK = display.create_pen(0, 0, 0)
    TEXT = display.create_pen(195, 23, 200)

    while True:
        buttons.tick()

        display.set_pen(BLACK)
        display.clear()

        b = buttons.read()
        if b != '':
            display.set_pen(TEXT)
            display.text('Button %s pressed!' % b, 15, 10, 240, 5)
            time.sleep(2)
        time.sleep(0.5)

       



if __name__ == '__main__':
    main()