from machine import ADC, Pin
import time

from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
from pimoroni import RGBLED


class Battery:
    def __init__(self, tick_rate):
        self.voltage_sensor = ADC(29)
        self.led = RGBLED(6, 7, 8)

        self.full_battery = 4.2
        self.empty_battery = 3.25

        self.uptime = 0
        self.tick_rate = tick_rate
        
        self.tick()
    
    def checkVoltage(self):
        conversion_factor = 3 * 3.3 / 65545
        self.voltage = self.voltage_sensor.read_u16() * conversion_factor
        self.percentage = 100 * ((self.voltage - self.empty_battery) / (self.full_battery - self.empty_battery))
        if self.percentage > 100:
            self.percentage = 100
    
    def checkCharging(self):
        self.power_sensor = Pin(24, Pin.IN)
    
    def setLED(self):
        modifier = self.percentage / 100

        if self.power_sensor.value() == 1:
            self.led.set_rgb(int(170 * modifier), 120, int(180 * modifier))
        else:
            if self.percentage > 73:
                self.led.set_rgb(42, int(242 * modifier), 180)
            elif self.percentage > 23:
                self.led.set_rgb(int(255 * modifier), int(204 * modifier), 0)
            else:
                self.led.set_rgb(int(255 * modifier), 0, 0)
    
    def tick(self):
        self.checkCharging()
        self.checkVoltage()
        self.setLED()
        self.uptime = self.uptime + self.tick_rate
    
    def daemon(self):
        while True:
            self.tick()
            time.sleep(self.tick_rate)


def main():
    tick_rate = 0.5
    battery = Battery(tick_rate)

    display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0)
    #display.set_backlight(0.42)
    display.set_backlight(1)

    BLACK = display.create_pen(0, 0, 0)
    SEA = display.create_pen(42, 242, 180)

    while True:
        battery.tick()

        display.set_pen(BLACK)
        display.clear()

        display.set_pen(SEA)
        display.text('{:.2f}v'.format(battery.voltage), 15, 100, 240, 2)
        display.text('{:.0f}%'.format(battery.percentage), 150, 100, 240, 2)

        hours = battery.uptime / 3600
        minutes = battery.uptime / 60
        display.text('{:.3f} hours'.format(hours), 15, 10, 240, 4)    
        display.text('{:.2f} minutes'.format(minutes), 15, 40, 240, 3)
        display.text('{:.0f} seconds'.format(battery.uptime), 15, 60, 240, 2)

        display.update()
        time.sleep(tick_rate)





if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)