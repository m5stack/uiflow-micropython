# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time

import M5
from M5 import Widgets
from module import LoRa1262Module


title0 = None
label_t = None
label_tx = None
label_ts = None
label_time = None
lora1262_0 = None
count = None
last_time = None
timestamp = None


def setup():
    global title0, label_t, label_tx, label_ts, label_time
    global lora1262_0, count, last_time, timestamp

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("LoRa1262 Module Tx", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_t = Widgets.Label("Send:", 5, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_tx = Widgets.Label("hello", 65, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_ts = Widgets.Label("timestamp:", 5, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_time = Widgets.Label("1", 118, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    lora1262_0 = LoRa1262Module()
    count = 0
    last_time = time.ticks_ms()


def loop():
    global title0, label_t, label_tx, label_ts, label_time
    global lora1262_0, count, last_time, timestamp

    M5.update()
    if time.ticks_diff(time.ticks_ms(), last_time) >= 1000:
        last_time = time.ticks_ms()
        count += 1
        message = "Module LoRa1262 %d" % count
        lora1262_0.send(message)
        timestamp = time.ticks_ms()
        label_tx.setText(str(message))
        label_time.setText(str(timestamp))


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
