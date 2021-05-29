from machine import ADC, I2C, Pin
from ssd1306 import SSD1306_I2C
from time import sleep


# turn on LED so we know the pico is powered on
led = Pin(25, Pin.OUT)
led.on()


# initialize screen
width = 128
height = 64

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
oled = SSD1306_I2C(width, height, i2c)

# start loop to read temperature and write to screen
while True:
    # take temperature reading
    temp_sensor = ADC(4)
    temp = temp_sensor.read_u16()

    # convert analogue input to volts
    to_volts = 3.3 / 65535
    temp = temp * to_volts

    # convert volts to celsius and celsius to fahrenheit
    tempC = 27 - (temp - 0.706) / 0.001721
    tempF = tempC * 9 / 5 + 32


    # clear the oled screen
    oled.fill(0)
    
    # write text
    oled.text('Current temp:', 0, 0)
    oled.text('%s C' % str(tempC), 0, 15)
    oled.text('%s F' % str(tempF), 0, 30)
    
    # update the display to display text
    oled.show()
    
    print('Current temp: %s C (%s F)' % (str(tempC), str(tempF)))

    sleep(15)
