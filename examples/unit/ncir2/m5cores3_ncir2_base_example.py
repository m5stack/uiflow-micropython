# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import NCIR2Unit
import time



title0 = None
label_temp = None
label_la = None
label_ha = None
label_temp_val = None
label_la_val = None
label_ha_val = None
i2c0 = None
ncir2_0 = None
last_time = None


def setup():
    global title0, label_temp, label_la, label_ha, label_temp_val, label_la_val, label_ha_val, i2c0, ncir2_0, last_time
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Temperature meassure", 3, 0xffffff, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_temp = Widgets.Label("Temp: ", 10, 116, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu24)
    label_la = Widgets.Label("low temp alarm value: ", 10, 50, 1.0, 0x0000ff, 0x222222, Widgets.FONTS.DejaVu18)
    label_ha = Widgets.Label("high temp alarm value: ", 10, 80, 1.0, 0xff0000, 0x222222, Widgets.FONTS.DejaVu18)
    label_temp_val = Widgets.Label(" ", 95, 116, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu24)
    label_la_val = Widgets.Label(" ", 232, 50, 1.0, 0x0000ff, 0x222222, Widgets.FONTS.DejaVu18)
    label_ha_val = Widgets.Label(" ", 239, 80, 1.0, 0xff0000, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    ncir2_0 = NCIR2Unit(i2c0, 0x5A)
    last_time = time.ticks_ms()
    label_la_val.setText(str(ncir2_0.get_temperature_threshold(0x20)))
    label_ha_val.setText(str(ncir2_0.get_temperature_threshold(0x22)))


def loop():
    global title0, label_temp, label_la, label_ha, label_temp_val, label_la_val, label_ha_val, i2c0, ncir2_0, last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) > 500:
        last_time = time.ticks_ms()
        label_temp.setText(str((str((ncir2_0.get_temperature_value)) + str(' C'))))


if __name__ == '__main__':
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
