# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import CardKBUnit


title0 = None
label0 = None
cardkb2_0 = None


key_id = None
key_status = None


def cardkb2_0_pressed_event(kb):
    global title0, label0, cardkb2_0, key_id, key_status
    key_id, key_status = kb
    if key_status == (CardKBUnit.KEY_STATE_PRESS):
        label0.setText(str((str("Key ID ") + str((str(key_id) + str(" Press"))))))
        print((str("Key ID ") + str((str(key_id) + str(" Press")))))
    elif key_status == (CardKBUnit.KEY_STATE_RELEASE):
        label0.setText(str((str("Key ID ") + str((str(key_id) + str(" Release"))))))
        print((str("Key ID ") + str((str(key_id) + str(" Release")))))


def setup():
    global title0, label0, cardkb2_0, key_id, key_status

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "CardKB2 ESPNOW Mode Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 3, 107, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    cardkb2_0 = CardKBUnit(mode=CardKBUnit.CardKB_ESP_NOW_MODE)
    cardkb2_0.set_callback(cardkb2_0_pressed_event)


def loop():
    global title0, label0, cardkb2_0, key_id, key_status
    M5.update()
    cardkb2_0.tick()


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
