# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import EncoderChain
from chain import ChainBus
import time



title0 = None
label_brightness = None
label_val = None
label_count = None
bus2 = None
chain_encoder_0 = None
count = None
last_time = None
value = None
brightness = None


def chain_encoder_0_click_event(args):
    global title0, label_brightness, label_val, label_count, bus2, chain_encoder_0, count, last_time, value, brightness
    count = (count if isinstance(count, (int, float)) else 0) + 1
    label_count.setText(str((str('Button Count: ') + str(count))))

def setup():
    global title0, label_brightness, label_val, label_count, bus2, chain_encoder_0, count, last_time, value, brightness
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Title", 3, 0xffffff, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_brightness = Widgets.Label("Brightness:", 5, 100, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu24)
    label_val = Widgets.Label("Value:", 5, 60, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu24)
    label_count = Widgets.Label("Button Count:", 5, 140, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu24)
    bus2 = ChainBus(2, tx=21, rx=22)
    chain_encoder_0 = EncoderChain(bus2, 1)
    chain_encoder_0.set_click_callback(chain_encoder_0_click_event)
    chain_encoder_0.set_button_mode(chain_encoder_0.MODE_EVENT)
    chain_encoder_0.set_rgb_color(0x00ff00)
    chain_encoder_0.set_rgb_brightness(80, save=False)
    chain_encoder_0.set_cw_increase(True, save=False)
    print(chain_encoder_0.get_encoder_increment())
    brightness = 0


def loop():
    global title0, label_brightness, label_val, label_count, bus2, chain_encoder_0, count, last_time, value, brightness
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        value = chain_encoder_0.get_encoder_value()
        label_val.setText(str((str('Value: ') + str(value))))
        brightness = min(max(brightness + (chain_encoder_0.get_encoder_increment()), 0), 100)
        label_brightness.setText(str((str('Brightness: ') + str(brightness))))
        chain_encoder_0.set_rgb_brightness(brightness, save=False)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
