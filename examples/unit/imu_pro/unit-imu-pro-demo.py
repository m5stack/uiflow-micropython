import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import IMUProUnit
import time


i2c0 = None
imupro_0 = None


def setup():
    global i2c0, imupro_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    imupro_0 = IMUProUnit(i2c0)


def loop():
    global i2c0, imupro_0
    M5.update()
    print((str("Acc:") + str((imupro_0.get_accelerometer()))))
    print((str("Gryo:") + str((imupro_0.get_gyroscope()))))
    print((str("Magneto:") + str((imupro_0.get_magnetometer()))))
    print((str("Compass:") + str((imupro_0.get_compass()))))
    print((str("Attitude") + str((imupro_0.get_attitude()))))
    print((str("Temperature") + str((imupro_0.get_temperature()))))
    print((str("Pressure:") + str((imupro_0.get_pressure()))))
    time.sleep_ms(100)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
