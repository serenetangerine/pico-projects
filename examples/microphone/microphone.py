from machine import ADC


# ADC channel 1 for input (can be microphone, or any analogue input)
adc = machine.ADC(1)

while True:
    # read adc and get 16-bit data point
    adc_pt = adc.read_u16()
    print(adc_pt)
