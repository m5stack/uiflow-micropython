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
lable_title = None
label_tx = None
label_time = None
btn_ctrl = None
module_cc1101_0 = None
send_flag = None
last_time = None
count = None
tx = None


def btn_ctrl_clicked_event(event_struct):
    global \
        page0, \
        lable_title, \
        label_tx, \
        label_time, \
        btn_ctrl, \
        module_cc1101_0, \
        send_flag, \
        last_time, \
        count, \
        tx
    send_flag = not send_flag
    if send_flag:
        btn_ctrl.set_btn_text(str("Stop"))
    else:
        btn_ctrl.set_btn_text(str("Start"))
    Speaker.tone(666, 100)


def btn_ctrl_event_handler(event_struct):
    global \
        page0, \
        lable_title, \
        label_tx, \
        label_time, \
        btn_ctrl, \
        module_cc1101_0, \
        send_flag, \
        last_time, \
        count, \
        tx
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_ctrl_clicked_event(event_struct)
    return


def setup():
    global \
        page0, \
        lable_title, \
        label_tx, \
        label_time, \
        btn_ctrl, \
        module_cc1101_0, \
        send_flag, \
        last_time, \
        count, \
        tx

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    lable_title = m5ui.M5Label(
        "ModuleCC1101 Tx",
        x=58,
        y=2,
        text_c=0x0000FF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_tx = m5ui.M5Label(
        "Tx:",
        x=5,
        y=64,
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
    btn_ctrl = m5ui.M5Button(
        text="Stop",
        x=127,
        y=130,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    btn_ctrl.add_event_cb(btn_ctrl_event_handler, lv.EVENT.ALL, None)

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
    count = 0
    send_flag = True
    btn_ctrl.set_size(100, 60)
    btn_ctrl.align_to(page0, lv.ALIGN.CENTER, 0, 30)
    Speaker.begin()
    Speaker.setVolumePercentage(0.8)
    Speaker.tone(666, 100)


def loop():
    global \
        page0, \
        lable_title, \
        label_tx, \
        label_time, \
        btn_ctrl, \
        module_cc1101_0, \
        send_flag, \
        last_time, \
        count, \
        tx
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
        last_time = time.ticks_ms()
        label_time.set_text(str((str("Timestamp: ") + str((time.ticks_ms())))))
        if send_flag:
            tx = str("Hello M5 - ") + str(count)
            count = (count if isinstance(count, (int, float)) else 0) + 1
            print(tx)
            if module_cc1101_0.send(tx):
                label_tx.set_text(str((str("Tx: ") + str(tx))))
            else:
                label_tx.set_text(str("Send failed!"))


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
