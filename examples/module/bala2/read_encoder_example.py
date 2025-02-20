# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import Bala2Module
import time


title0 = None
label_enc1 = None
label_enc2 = None
label_enc1_val = None
label_enc2_val = None
module_bala2_0 = None
last_time = None
enc_value = None
enc1 = None
enc2 = None


def setup():
    global \
        title0, \
        label_enc1, \
        label_enc2, \
        label_enc1_val, \
        label_enc2_val, \
        module_bala2_0, \
        last_time, \
        enc_value, \
        enc1, \
        enc2
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Bala2 Encoder Read", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_enc1 = Widgets.Label("Enc1", 54, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_enc2 = Widgets.Label("Enc2", 208, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_enc1_val = Widgets.Label("0", 50, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_enc2_val = Widgets.Label("0", 202, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    module_bala2_0 = Bala2Module(0)
    module_bala2_0.set_encoder_value(0, 0)
    last_time = time.ticks_ms()


def loop():
    global \
        title0, \
        label_enc1, \
        label_enc2, \
        label_enc1_val, \
        label_enc2_val, \
        module_bala2_0, \
        last_time, \
        enc_value, \
        enc1, \
        enc2
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) > 100:
        last_time = time.ticks_ms()
        enc_value = module_bala2_0.get_encoder_value()
        enc1 = enc_value[0]
        enc2 = enc_value[1]
        label_enc1_val.setText(str(enc1))
        label_enc2_val.setText(str(enc2))


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
