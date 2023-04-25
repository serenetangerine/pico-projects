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


# import in wifi config from secrets.py
#
# format should follow
#
# SSID = "your ssid"
# PASS = "your pass"

SSID = secrets.SSID
PASS = secrets.PASS

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
# disable powersave mode
#wlan.config(pm = 0xa11140)

wlan.connect(SSID, PASS)

# keep trying to connect FOREVER until there is a valid connection
while not wlan.isconnected() and wlan.status() >= 0:
    print('Waiting to connect to %s...' % SSID)
    time.sleep(1)

# print ip information
print(wlan.ifconfig())

# fun tidbits
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
channel = wlan.config('channel')
essid = wlan.config('essid')
txpower = wlan.config('txpower')

print(mac)
print(channel)
print(essid)
print(txpower)

# disconnect
# wlan.disconnect()