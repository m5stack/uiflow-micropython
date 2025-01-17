# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import ByteSwitchUnit
import time


title0 = None
label0 = None
label1 = None
i2c0 = None
byteswitch_0 = None


state_byte = None
i = None


def setup():
    global title0, label0, label1, i2c0, byteswitch_0, state_byte, i

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "ByteSwitch CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 4, 87, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 5, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    byteswitch_0 = ByteSwitchUnit(i2c0, 0x46)
    byteswitch_0.set_led_show_mode(ByteSwitchUnit.BYTESWITCH_LED_USER_MODE)
    byteswitch_0.set_indicator_color(0x33FF33)
    for i in range(8):
        byteswitch_0.set_led_color(i, 0xFF0000, ByteSwitchUnit.BYTESWITCH_LED_USER_MODE)
        byteswitch_0.set_indicator_brightness(255)
        time.sleep(0.2)
        if i != 7:
            byteswitch_0.set_led_color(i + 1, 0x000000, ByteSwitchUnit.BYTESWITCH_LED_USER_MODE)
    time.sleep(1)
    for i in range(7, -1, -1):
        byteswitch_0.set_led_color(i, 0x66FF99, ByteSwitchUnit.BYTESWITCH_LED_USER_MODE)
        time.sleep(0.2)
    time.sleep(1)
    byteswitch_0.set_led_show_mode(ByteSwitchUnit.BYTESWITCH_LED_SYS_MODE)
    for i in range(8):
        byteswitch_0.set_led_color(i, 0xFFFFFF, ByteSwitchUnit.BYTESWITCH_LED_SYS_MODE, False)
        byteswitch_0.set_led_color(i, 0xFF0000, ByteSwitchUnit.BYTESWITCH_LED_SYS_MODE, True)


def loop():
    global title0, label0, label1, i2c0, byteswitch_0, state_byte, i
    M5.update()
    state_byte = byteswitch_0.get_byte_switch_status()
    label0.setText(
        str(
            [
                (str("B0:") + str(((state_byte >> 0) & 0x01))),
                (str("B1:") + str(((state_byte >> 1) & 0x01))),
                (str("B2:") + str(((state_byte >> 2) & 0x01))),
                (str("B3:") + str(((state_byte >> 3) & 0x01))),
            ]
        )
    )
    label1.setText(
        str(
            [
                (str("B4:") + str(((state_byte >> 4) & 0x01))),
                (str("B5:") + str(((state_byte >> 5) & 0x01))),
                (str("B6:") + str(((state_byte >> 6) & 0x01))),
                (str("B7:") + str(((state_byte >> 7) & 0x01))),
            ]
        )
    )


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
