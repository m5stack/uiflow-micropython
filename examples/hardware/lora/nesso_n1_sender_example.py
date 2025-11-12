# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import LoRa
import time


title0 = None
label0 = None
lora = None


last_time = None
count = None
text = None


def setup():
    global title0, label0, lora, last_time, count, text

    M5.begin()
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("Sender", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("label0", 2, 40, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    lora = LoRa(
        pin_irq=15,
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
    global title0, label0, lora, last_time, count, text
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
        last_time = time.ticks_ms()
        text = str("M5") + str(count)
        count = (count if isinstance(count, (int, float)) else 0) + 1
        lora.send(text, None)
        label0.setText(str(text))


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
