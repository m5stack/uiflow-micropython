# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from module import CC1101Module
import time


page0 = None
label_title = None
label_rssi = None
label_rx = None
label_time = None
module_cc1101_0 = None
cc1101_data = None
last_time = None


def module_cc1101_0_receive_event(received_data):
    global \
        page0, \
        label_title, \
        label_rssi, \
        label_rx, \
        label_time, \
        module_cc1101_0, \
        cc1101_data, \
        last_time
    cc1101_data = received_data
    if cc1101_data.crc_ok:
        label_rx.set_text(str((str("Rx: ") + str((cc1101_data.decode())))))
    else:
        print("CRC error")
    label_rssi.set_text(str((str("RSSI: ") + str((str((cc1101_data.rssi)) + str(" dBm"))))))


def setup():
    global \
        page0, \
        label_title, \
        label_rssi, \
        label_rx, \
        label_time, \
        module_cc1101_0, \
        cc1101_data, \
        last_time

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label_title = m5ui.M5Label(
        "ModuleCC1101 Rx",
        x=56,
        y=2,
        text_c=0x0000FF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_rssi = m5ui.M5Label(
        "RSSI:",
        x=5,
        y=95,
        text_c=0x0000FF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_rx = m5ui.M5Label(
        "Rx:",
        x=5,
        y=65,
        text_c=0x0000FF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_time = m5ui.M5Label(
        "Timestamp:",
        x=5,
        y=210,
        text_c=0x0000FF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )

    page0.screen_load()
    module_cc1101_0 = CC1101Module(
        pin_cs=5,
        pin_gdo0=7,
        pin_gdo2=10,
        freq_khz=868000,
        bitrate_kbps=3,
        freq_dev_khz=25.4,
        rx_bw_khz=58,
        output_power=10,
        preamble_length=16,
        sync_word_h=0x12,
        sync_word_l=0xAD,
    )
    module_cc1101_0.set_rx_irq_callback(module_cc1101_0_receive_event)
    module_cc1101_0.start_recv()


def loop():
    global \
        page0, \
        label_title, \
        label_rssi, \
        label_rx, \
        label_time, \
        module_cc1101_0, \
        cc1101_data, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
        last_time = time.ticks_ms()
        label_time.set_text(str((str("Timestamp: ") + str((time.ticks_ms())))))


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
