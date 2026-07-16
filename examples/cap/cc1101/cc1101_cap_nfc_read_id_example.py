# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from cap import NFCCap
import time


label_title = None
label_status = None
label_uid = None
label_type = None
label_mem = None
cap_nfc = None
last_scan_ms = None
card_0 = None
last_uid = None
card_uid = None
card_type = None
card_size = None


def setup():
    global \
        label_title, \
        label_status, \
        label_uid, \
        label_type, \
        label_mem, \
        cap_nfc, \
        last_scan_ms, \
        card_0, \
        last_uid, \
        card_uid, \
        card_type, \
        card_size

    M5.begin()
    Widgets.fillScreen(0x101418)
    label_title = Widgets.Label(
        "NFC card detect", 44, 3, 1.0, 0x22D3A6, 0x101418, Widgets.FONTS.Montserrat18
    )
    label_status = Widgets.Label(
        "Scanning...", 5, 28, 1.0, 0x22D3A6, 0x101418, Widgets.FONTS.Montserrat14
    )
    label_uid = Widgets.Label("UID: -", 5, 50, 1.0, 0xEAF2F8, 0x101418, Widgets.FONTS.Montserrat14)
    label_type = Widgets.Label(
        "Type: -", 5, 72, 1.0, 0xEAF2F8, 0x101418, Widgets.FONTS.Montserrat14
    )
    label_mem = Widgets.Label(
        "Memory: -", 5, 94, 1.0, 0xEAF2F8, 0x101418, Widgets.FONTS.Montserrat14
    )

    Speaker.begin()
    Speaker.setVolumePercentage(0.6)
    cap_nfc = NFCCap()
    last_uid = ""
    last_scan_ms = time.ticks_ms()
    label_status.setText(str("Scanning..."))
    label_uid.setText(str("UID: -"))
    label_type.setText(str("Type: -"))
    label_mem.setText(str("Memory: -"))
    Speaker.tone(3600, 40)
    time.sleep_ms(35)
    Speaker.tone(4800, 45)


def loop():
    global \
        label_title, \
        label_status, \
        label_uid, \
        label_type, \
        label_mem, \
        cap_nfc, \
        last_scan_ms, \
        card_0, \
        last_uid, \
        card_uid, \
        card_type, \
        card_size
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_scan_ms)) >= 180:
        last_scan_ms = time.ticks_ms()
        card_0 = cap_nfc.detect()
        if card_0:
            card_uid = card_0.uid_str
            if card_uid != last_uid:
                last_uid = card_uid
                card_type = card_0.type_name
                card_size = card_0.user_memory
                label_status.setText(str("Card detected"))
                label_uid.setText(str((str("UID: ") + str(card_uid))))
                label_type.setText(str((str("Type: ") + str(card_type))))
                label_mem.setText(str((str((str("Memory: ") + str(card_size))) + str(" bytes"))))
                Speaker.tone(4200, 45)
                time.sleep_ms(35)
                Speaker.tone(5600, 55)
            cap_nfc.halt()
        else:
            last_uid = ""
            label_status.setText(str("Scanning..."))
            label_uid.setText(str("UID: -"))
            label_type.setText(str("Type: -"))
            label_mem.setText(str("Memory: -"))


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
