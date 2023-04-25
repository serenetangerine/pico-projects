import machine
import network
import secrets
import time
import ubinascii

# turn on LED so we know the pi is powered on
led = machine.Pin("LED", machine.Pin.OUT)
led.on()

# connect to the network
#

class WIFI:
    def __init__(self):
        # import in wifi config from secrets.py
        #
        # format should follow
        #
        # SSID = "your ssid"
        # PASS = "your pass"

        # disable powersave mode
        #self.wlan.config(pm = 0xa11140)

        self.SSID = secrets.SSID
        self.PASS = secrets.PASS

        self.connect()




    def connect(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)

        self.wlan.connect(self.SSID, self.PASS)

        # keep trying to connect FOREVER until there is a valid connection
        while not self.wlan.isconnected() and self.wlan.status() >= 0:
            print('\n\nAttempting to connect to %s...' % self.SSID)
            time.sleep(1)

        # ip information
        self.ip = self.wlan.ifconfig()[0]
        self.subnetmask = self.wlan.ifconfig()[1]
        self.gateway = self.wlan.ifconfig()[2]
        self.dns = self.wlan.ifconfig()[3]

        # fun tidbits
        self.mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
        self.channel = self.wlan.config('channel')
        self.essid = self.wlan.config('essid')
        self.txpower = self.wlan.config('txpower')

        print('\nConnected successfully to %s!' % self.SSID)
        print('IP Address: %s\n\n' % str(self.ip))

    def disconnect(self):
        self.wlan.disconnect()


def main():
    wifi = WIFI()


if __name__ == '__main__':
    main()
    #try:
    #    main()
    #except Exception as e:
    #    print(e)