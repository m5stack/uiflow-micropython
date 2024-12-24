import os, sys, io
import M5
from M5 import *
from unit import WateringUnit


label0 = None
label1 = None
label2 = None
label3 = None
watering_0 = None


def setup():
    global label0, label1, label2, label3, watering_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Voltage:", 50, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("ADC:", 50, 140, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 150, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 150, 140, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    watering_0 = WateringUnit((8, 9))


def loop():
    global label0, label1, label2, label3, watering_0
    M5.update()
    label2.setText(str(watering_0.get_voltage()))
    label3.setText(str(watering_0.get_raw()))
    if (watering_0.get_raw()) > 30000:
        watering_0.on()
    else:
        watering_0.off()


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
