import os, sys, io
import M5
from M5 import *
from hardware import *
import time
from unit import *


label0 = None
label1 = None
i2c0 = None
ncir_0 = None


def setup():
    global label0, label1, i2c0, ncir_0

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    ncir_0 = NCIR(i2c0)
    M5.begin()
    label0 = Widgets.Label("Text", 5, 12, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Text", 14, 44, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)


def loop():
    global label0, label1, i2c0, ncir_0
    M5.update()
    label0.setText(str((ncir_0.get_ambient_temperature())))
    label1.setText(str((ncir_0.get_object_temperature())))
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
