# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ADCV11Unit


title0 = None
label1 = None
label0 = None
i2c0 = None
adc_v11_0 = None


def setup():
    global title0, label1, label0, i2c0, adc_v11_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "ADCV11Unit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "ADC 16Bit Value:", 1, 130, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("ADC Value:", 1, 91, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    adc_v11_0 = ADCV11Unit(i2c0)
    adc_v11_0.set_sample_rate(0x00)
    adc_v11_0.set_mode(0x00)
    adc_v11_0.start_single_conversion()
    adc_v11_0.set_gain(0x00)


def loop():
    global title0, label1, label0, i2c0, adc_v11_0
    M5.update()
    label0.setText(str((str("ADC Value:") + str((adc_v11_0.get_voltage())))))
    label1.setText(str((str("ADC 16Bit Value:") + str((adc_v11_0.get_adc_raw_value())))))


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
