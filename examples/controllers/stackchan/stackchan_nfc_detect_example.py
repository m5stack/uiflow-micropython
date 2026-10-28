# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time
from hardware.stackchan import StackChan


page0 = None
label_title = None
label_uid = None
label_type = None
label_size = None
stackchan = None
card_0 = None
card_uid = None
new = None
card_type = None
card_size = None
last_time = None


def setup():
    global \
        page0, \
        label_title, \
        label_uid, \
        label_type, \
        label_size, \
        stackchan, \
        card_0, \
        card_uid, \
        new, \
        card_type, \
        card_size, \
        last_time

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "NFC Card detect",
        x=58,
        y=5,
        text_c=0x13C2EB,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_uid = m5ui.M5Label(
        "UID:",
        x=18,
        y=70,
        text_c=0xFFFFFF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_type = m5ui.M5Label(
        "Tyep:",
        x=10,
        y=100,
        text_c=0xFFFFFF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_size = m5ui.M5Label(
        "Size:",
        x=16,
        y=130,
        text_c=0xFFFFFF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )

    page0.screen_load()
    stackchan = StackChan(i2c=1, uart=1)
    Speaker.begin()
    Speaker.setVolumePercentage(0.6)


def loop():
    global \
        page0, \
        label_title, \
        label_uid, \
        label_type, \
        label_size, \
        stackchan, \
        card_0, \
        card_uid, \
        new, \
        card_type, \
        card_size, \
        last_time
    M5.update()
    card_0 = stackchan.nfc.detect()
    if card_0:
        card_uid = card_0.uid_str
        card_type = card_0.type_name
        card_size = card_0.user_memory
        label_uid.set_text(str((str("UID: ") + str(card_uid))))
        label_type.set_text(str((str("Tyep: ") + str(card_type))))
        label_size.set_text(str((str("Size: ") + str(card_size))))
        if (time.ticks_diff((time.ticks_ms()), last_time)) >= 3000 or new:
            last_time = time.ticks_ms()
            stackchan.set_rgb_color(0x009900)
            Speaker.tone(1234, 100)
            time.sleep_ms(100)
            stackchan.set_rgb_color(0x000000)
        new = False
    else:
        new = True


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
