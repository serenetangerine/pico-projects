# takes an analogue input and graphs on oled screen


from machine import Pin, I2C
from ssd1306 import SSD1306_I2C


def oscilliscope():
    ## assumes the screen has already been initialized

    # initialize ADC for analogue input
    from machine import ADC
    # ADC channel 1 for input (can be microphone or any analogue input)
    adc = ADC(1)

    # flip display to place 0,0 at lower-left corner
    oled.write_cmd(0xc0)
    
    # start reading analogue input and convert to pixels to plot on oled
    while True:
        # clear the oled screen
        oled.fill(0)
    
        # loop through horizontal display resolution
        # this generates 1 frame by taking the width number of analogue inputs
        for i in range(width):
            # read adc and get 16-bit data point
            adc_pt = adc.read_u16()
    
            # convert to oled pixels
            plot_pt = (adc_pt / ((2 ** 16) - 1)) * (height - 1)
    
            # add data point 
            oled.text('.', i, int(plot_pt))
    
        # display the oled frame
        oled.show()


# initialize oled screen
width  = 128
height = 64

i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=200000)
oled = SSD1306_I2C(width, height, i2c)

oscilliscope()
