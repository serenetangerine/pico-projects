from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from time import sleep


# turn on LED so we know the pico is powered on
led = Pin(25, Pin.OUT)
led.on()


def temperatureLoop():
    # initialize ADC 4 for temperature reading
    from machine import ADC
    temp_sensor = ADC(4)

    # start loop to read temperature and write to screen
    while True:
        # take temperature reading
        temp = temp_sensor.read_u16()
    
        # convert analogue input to volts
        to_volts = 3.3 / 65535
        temp = temp * to_volts
    
        # convert volts to celsius and celsius to fahrenheit
        #
        # default volts to celsius conversion
        # tempC = 27 - (temp - 0.706) / 0.001721
        # 
        # calibrate temperature
        tempC = 34 - (temp - 0.706) / 0.001721
        tempF = tempC * 9 / 5 + 32
    
    
        # clear the oled screen
        oled.fill(0)
        
        # write text
        oled.text('Current temp:', 0, 0)
        oled.text('%s C' % str(tempC), 0, 15)
        oled.text('%s F' % str(tempF), 0, 30)
        
        
        print('Current temp: %s C (%s F)' % (str(tempC), str(tempF)))
    
        # display progress bar for refresh
        oled.text('|', 75, 45)
        for i in range(15):
            oled.text('|', (5 * i), 45)
            oled.show()
            i += 1
            sleep(1)


# initialize screen
width = 128
height = 64

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
oled = SSD1306_I2C(width, height, i2c)

temperatureLoop()
