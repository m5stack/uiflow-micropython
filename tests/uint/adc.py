import time
from machine import I2C, Pin
from unit.adc import ADC

i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
ads = ADC(i2c0)
ads.set_operating_mode(ads.CONTINUOUS)
ads.set_data_rate(8) #8 16 32 128
ads.set_gain(1) # 1 2 4 8

while True:
    print("ADC value: {0}, voltage: {1}".format(ads.get_value(), ads.get_voltage()))
    time.sleep(1)
