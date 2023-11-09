import os, sys, io
import M5
from M5 import *
import time
from unit import *


label0 = None
label1 = None
label2 = None
light_0 = None


def setup():
    global label0, label1, label2, light_0

    light_0 = LightUnit((1, 2))
    M5.begin()
    label0 = Widgets.Label("Text", 2, 2, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Text", 2, 30, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Text", 2, 58, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)


def loop():
    global label0, label1, label2, light_0
    M5.update()
    label0.setText(str(((str("digital ") + str((light_0.get_digital_value()))))))
    label1.setText(str(((str("analog ") + str((light_0.get_analog_value()))))))
    label2.setText(str(((str("ohm ") + str((light_0.get_ohm()))))))
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
