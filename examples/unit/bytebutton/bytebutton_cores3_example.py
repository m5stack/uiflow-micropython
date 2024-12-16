# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ByteButtonUnit
import time


title0 = None
label0 = None
label1 = None
i2c0 = None
bytebutton_0 = None


state_byte = None
i = None


def setup():
    global title0, label0, label1, i2c0, bytebutton_0, state_byte, i

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "ByteButton CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 4, 87, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 5, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    bytebutton_0 = ByteButtonUnit(i2c0, 0x47)
    bytebutton_0.set_led_show_mode(ByteButtonUnit.BYTEBUTTON_LED_USER_MODE)
    bytebutton_0.set_indicator_color(0x33FF33)
    for i in range(8):
        bytebutton_0.set_led_color(i, 0xFF0000, ByteButtonUnit.BYTEBUTTON_LED_USER_MODE)
        bytebutton_0.set_indicator_brightness(255)
        time.sleep(0.2)
        bytebutton_0.set_led_color(i + 1, 0x333300, ByteButtonUnit.BYTEBUTTON_LED_USER_MODE)
    time.sleep(1)
    for i in range(7, -1, -1):
        bytebutton_0.set_led_color(i, 0x66FF99, ByteButtonUnit.BYTEBUTTON_LED_USER_MODE)
        time.sleep(0.2)
    time.sleep(1)
    bytebutton_0.set_led_show_mode(ByteButtonUnit.BYTEBUTTON_LED_SYS_MODE)
    for i in range(8):
        bytebutton_0.set_led_color(i, 0xFFFFFF, ByteButtonUnit.BYTEBUTTON_LED_SYS_MODE, False)
        bytebutton_0.set_led_color(i, 0xFF0000, ByteButtonUnit.BYTEBUTTON_LED_SYS_MODE, True)


def loop():
    global title0, label0, label1, i2c0, bytebutton_0, state_byte, i
    M5.update()
    state_byte = bytebutton_0.get_byte_button_status()
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
