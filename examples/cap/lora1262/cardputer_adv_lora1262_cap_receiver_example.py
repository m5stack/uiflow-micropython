# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import time
from cap import LoRa1262Cap


cap_lora1262 = None


lora_data = None
cur_time = None
time_buf = None
rx_text = None


def cap_lora1262_receive_event(received_data):
    global cap_lora1262, lora_data, cur_time, time_buf, rx_text
    lora_data = received_data
    cur_time = time.gmtime()
    time_buf = ""
    time_buf = str(time_buf) + str("[")
    time_buf = str(time_buf) + str((cur_time[3]))
    time_buf = str(time_buf) + str(":")
    time_buf = str(time_buf) + str((cur_time[4]))
    time_buf = str(time_buf) + str(":")
    time_buf = str(time_buf) + str((cur_time[5]))
    time_buf = str(time_buf) + str("] -> ")
    M5.Lcd.print(time_buf, 0x33FF33)
    rx_text = lora_data.decode()
    M5.Lcd.print(rx_text, 0xFFFFFF)
    M5.Lcd.printf("\n")


def setup():
    global cap_lora1262, lora_data, cur_time, time_buf, rx_text

    M5.begin()
    Widgets.fillScreen(0x000000)

    cap_lora1262 = LoRa1262Cap(
        freq_khz=868000,
        bw="250",
        sf=8,
        coding_rate=8,
        preamble_len=12,
        syncword=0x12,
        output_power=10,
    )
    cap_lora1262.set_irq_callback(cap_lora1262_receive_event)
    M5.Lcd.setFont(Widgets.FONTS.DejaVu12)
    M5.Lcd.setTextColor(0xFFFFFF, 0x000000)
    M5.Lcd.setCursor(0, 0)
    M5.Lcd.setTextScroll(True)
    cap_lora1262.start_recv()


def loop():
    global cap_lora1262, lora_data, cur_time, time_buf, rx_text
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
