from machine import ADC, Pin
import time
import _thread


class Battery:
    def __init__(self, tick_rate):
        # this is hard coded for the built in pimoroni pico lipo battery support
        # this pin may vary depending on your setup
        self.voltage_sensor = ADC(29)

        # these are hard coded and may vary by battery 
        self.full_battery = 4.2
        self.empty_battery = 3.25

        self.uptime = 0
        self.tick_rate = tick_rate
        self.daemonize()

    
    def checkVoltage(self):
        conversion_factor = 3 * 3.3 / 65545
        self.voltage = self.voltage_sensor.read_u16() * conversion_factor
        self.percentage = 100 * ((self.voltage - self.empty_battery) / (self.full_battery - self.empty_battery))
        if self.percentage > 100:
            self.percentage = 100
    
    def checkCharging(self):
        self.power_sensor = Pin(24, Pin.IN)
    
    def tick(self):
        self.checkCharging()
        self.checkVoltage()
        self.uptime = self.uptime + self.tick_rate
    
    def daemon(self):
        while True:
            self.tick()
            time.sleep(self.tick_rate)

    def daemonize(self):
        self.thread = _thread.start_new_thread(self.daemon, ())



def main():
    print('\n\ncall this module using the following syntax')
    print('\nfrom battery import Battery')
    print('\nbattery = Battery(tick_rate)')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)