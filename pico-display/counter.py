from machine import ADC, Pin
import time

from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
from battery import Battery
import _thread

def batteryDaemon():
    # create a battery with tick rate of 1
    tick_rate = 1
    bat = Battery(tick_rate)
    while True:
        bat.tick()
        time.sleep(tick_rate)


def main():
    led = _thread.start_new_thread(batteryDaemon, ())

    display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0)
    #display.set_backlight(0.42)
    display.set_backlight(1)

    BLACK = display.create_pen(0, 0, 0)
    TEXT = display.create_pen(175, 100, 192)

    count = 0
    tick_rate = 1

    display.set_pen(TEXT)
    display.clear()
    time.sleep(2)
    
    while True:
        display.set_pen(BLACK)
        display.clear()
        
        display.set_pen(TEXT)
        display.text(str(count), 15, 10, 240, 5)

        display.update()
        count += 1
        time.sleep(tick_rate)


if __name__ == '__main__':
    main()