# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import CO2LUnit


title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
i2c0 = None
co2l_0 = None


def setup():
    global title0, label0, label1, label2, label3, i2c0, co2l_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "CO2LUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 1, 44, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 1, 95, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 1, 146, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 1, 198, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    co2l_0 = CO2LUnit(i2c0)
    co2l_0.set_start_periodic_measurement()


def loop():
    global title0, label0, label1, label2, label3, i2c0, co2l_0
    if co2l_0.is_data_ready():
        label0.setText(str("Data is ready."))
        label1.setText(str((str("CO2 ppm:") + str((co2l_0.co2)))))
        label2.setText(str((str("Humidity:") + str((co2l_0.humidity)))))
        label3.setText(str((str("Temperature:") + str((co2l_0.temperature)))))
    else:
        label0.setText(str("Data not ready."))


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
