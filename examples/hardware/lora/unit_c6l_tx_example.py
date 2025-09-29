# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import LoRa
import time


title0 = None
label_tx = None
lora = None
last_time = None
count = None
tx = None


def setup():
    global title0, label_tx, lora, last_time, count, tx
    M5.begin()
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("Tx", 3, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu12)
    label_tx = Widgets.Label("label0", 2, 23, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu12)
    lora = LoRa(
        freq_khz=868000,
        bw="250",
        sf=8,
        coding_rate=8,
        preamble_len=12,
        syncword=0x12,
        output_power=10,
    )
    last_time = time.ticks_ms()
    count = 0


def loop():
    global title0, label_tx, lora, last_time, count, tx
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
        last_time = time.ticks_ms()
        tx = str("M5 ") + str(count)
        count = (count if isinstance(count, (int, float)) else 0) + 1
        lora.send(tx, None)
        label_tx.setText(str(tx))


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
