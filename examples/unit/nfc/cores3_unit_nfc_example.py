# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import Pin
from hardware import I2C
from unit import NFCUnit
import time


page0 = None
label_title = None
label_uid = None
label_type = None
label_size = None
i2c0 = None
nfc_0 = None
card_0 = None
card_uid = None
new = None
card_type = None
card_memory = None
write_buf = None
count = None
last_time = None


def setup():
    global \
        page0, \
        label_title, \
        label_uid, \
        label_type, \
        label_size, \
        i2c0, \
        nfc_0, \
        card_0, \
        card_uid, \
        new, \
        card_type, \
        card_memory, \
        write_buf, \
        count, \
        last_time

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "NFC Card detect",
        x=58,
        y=5,
        text_c=0x14ACDB,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_uid = m5ui.M5Label(
        "UID:",
        x=18,
        y=70,
        text_c=0xFFFFFF,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_type = m5ui.M5Label(
        "Type:",
        x=10,
        y=100,
        text_c=0xFFFFFF,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_size = m5ui.M5Label(
        "Size:",
        x=16,
        y=130,
        text_c=0xFFFFFF,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    nfc_0 = NFCUnit(i2c0)
    page0.screen_load()
    Speaker.begin()
    Speaker.setVolumePercentage(0.5)
    new = True
    write_buf = bytearray(16)
    write_buf[0] = 0x12
    count = 0


def loop():
    global \
        page0, \
        label_title, \
        label_uid, \
        label_type, \
        label_size, \
        i2c0, \
        nfc_0, \
        card_0, \
        card_uid, \
        new, \
        card_type, \
        card_memory, \
        write_buf, \
        count, \
        last_time
    M5.update()
    card_0 = nfc_0.detect()
    if card_0:
        card_uid = card_0.uid_str
        card_type = card_0.type_name
        card_memory = card_0.user_memory
        label_uid.set_text(str((str("UID: ") + str(card_uid))))
        label_type.set_text(str((str("Type: ") + str(card_type))))
        label_size.set_text(str((str("Size: ") + str(card_memory))))
        if (time.ticks_diff((time.ticks_ms()), last_time)) >= 3000 or new:
            last_time = time.ticks_ms()
            Speaker.tone(900, 100)
            print((str("read data befor write ") + str((nfc_0.read(card_0, 1)))))
            count = (count if isinstance(count, (int, float)) else 0) + 1
            write_buf[-1] = 0x12 + count
            time.sleep_ms(100)
            if nfc_0.write(card_0, 1, write_buf):
                print("write success")
                time.sleep_ms(100)
                print((str("read data after write ") + str((nfc_0.read(card_0, 1)))))
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
