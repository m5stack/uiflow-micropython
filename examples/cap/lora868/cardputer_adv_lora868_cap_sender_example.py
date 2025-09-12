# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import MatrixKeyboard
from cap import LoRa868Cap
from unit import KeyCode


kb = None
cap_lora868 = None


keycode = None
key = None
buf = None


def kb_pressed_event(kb_0):
    global kb, cap_lora868, keycode, key, buf
    keycode = kb.get_key()
    if keycode >= 0x20 and keycode <= 0x7E:
        key = chr(keycode)
        buf = str(buf) + str(key)
        M5.Lcd.printf(key)
    elif keycode == (KeyCode.KEYCODE_ENTER):
        cap_lora868.send(buf, None)
        buf = ""
        M5.Lcd.fillScreen(0x000000)
        M5.Lcd.setCursor(0, 0)
        M5.Lcd.printf("\n")
        M5.Lcd.printf(">>> ")


def setup():
    global kb, cap_lora868, keycode, key, buf

    M5.begin()
    Widgets.fillScreen(0x000000)

    cap_lora868 = LoRa868Cap(
        freq_khz=868000,
        bw="250",
        sf=8,
        coding_rate=8,
        preamble_len=12,
        syncword=0x12,
        output_power=10,
    )
    kb = MatrixKeyboard()
    kb.set_callback(kb_pressed_event)
    M5.Lcd.setFont(Widgets.FONTS.DejaVu12)
    M5.Lcd.setTextColor(0xFFFFFF, 0x000000)
    M5.Lcd.setCursor(0, 0)
    M5.Lcd.printf(">>> ")
    buf = ""


def loop():
    global kb, cap_lora868, keycode, key, buf
    M5.update()


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
