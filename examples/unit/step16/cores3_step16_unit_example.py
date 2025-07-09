# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import Step16Unit


title0 = None
label1 = None
label_val = None
i2c0 = None
step16_0 = None
val = None


def setup():
    global title0, label1, label_val, i2c0, step16_0, val
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("UnitStep16 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label1 = Widgets.Label(
        "Encoder Value:", 10, 55, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24
    )
    label_val = Widgets.Label("0", 205, 55, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    step16_0 = Step16Unit(i2c0, 0x48)
    print((str("i2c addr: ") + str((step16_0.get_addr()))))
    print((str("version: ") + str((step16_0.get_firmware_version()))))
    step16_0.set_led_mode(Step16Unit.AUTO_OFF, 5)
    step16_0.set_led_brightness(80)
    print((str("rgb brightness: ") + str((step16_0.get_rgb_brightness()))))
    print((str("rgb value: ") + str((step16_0.get_rgb_value()))))
    if step16_0.get_rgb_power():
        print("RGB power on")
    else:
        print("RG B power off")
    step16_0.set_rgb_power(True)
    step16_0.set_rgb_value(0x3333FF)


def loop():
    global title0, label1, label_val, i2c0, step16_0, val
    M5.update()
    val = step16_0.get_encoder_value()
    label_val.setText(str(val))


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
