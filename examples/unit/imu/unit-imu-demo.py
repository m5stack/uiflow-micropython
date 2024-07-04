import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import IMUUnit
import time


i2c0 = None
imu_0 = None


def setup():
    global i2c0, imu_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    imu_0 = IMUUnit(i2c0)
    imu_0.set_accel_unit(1)
    imu_0.set_gyro_unit(1)


def loop():
    global i2c0, imu_0
    M5.update()
    print((str("Acc:") + str((imu_0.get_accelerometer()))))
    print((str("Gryo:") + str((imu_0.get_gyroscope()))))
    print((str("Attitude") + str((imu_0.get_attitude()))))
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
