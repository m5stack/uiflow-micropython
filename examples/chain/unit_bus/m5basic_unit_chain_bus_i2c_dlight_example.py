# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from chain import ChainBus
from chain import BusChainUnit
import time
from unit import DLightUnit


title = None
label_brightness = None
label_mode = None
i2c0 = None
bus2 = None
dlight_0 = None
unit_chain_bus_0 = None
last_time = None
brightness = None


def setup():
    global \
        title, \
        label_brightness, \
        label_mode, \
        i2c0, \
        bus2, \
        dlight_0, \
        unit_chain_bus_0, \
        last_time, \
        brightness

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title = Widgets.Title(
        "Unit Chain Bus Example: I2C", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label_brightness = Widgets.Label(
        "Brightness: -- lux", 10, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_mode = Widgets.Label(
        "Unit Chain Bus GPIO1&2: I2C", 10, 54, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    bus2 = ChainBus(2, tx=21, rx=22)
    unit_chain_bus_0 = BusChainUnit(bus2, 1)
    unit_chain_bus_0.set_i2c(BusChainUnit.I2C_SPEED_100K)
    dlight_0 = DLightUnit(unit_chain_bus_0)


def loop():
    global \
        title, \
        label_brightness, \
        label_mode, \
        i2c0, \
        bus2, \
        dlight_0, \
        unit_chain_bus_0, \
        last_time, \
        brightness
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 500:
        last_time = time.ticks_ms()
        brightness = int(dlight_0.get_lux())
        label_brightness.setText(str((str("Brightness: ") + str((str(brightness) + str(" lux"))))))
        print((str("Brightness: ") + str((str(brightness) + str(" lux")))))


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
