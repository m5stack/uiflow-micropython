# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time
from unit import Fingerprint2Unit


page0 = None
btn_enroll = None
btn_recognize = None
btn_delete = None
label0 = None
label_tip = None
label_res = None
fingerprint2_0 = None
id2 = None
count = None
operation = None
i = None
g_id = None
res = None


def wait_for_finger_press():
    global \
        id2, \
        count, \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_tip.set_text(str("Please place your finger"))
    while not (fingerprint2_0.get_enroll_image()):
        time.sleep_ms(100)
    Speaker.tone(888, 100)


def wait_for_finger_left():
    global \
        id2, \
        count, \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_tip.set_text(str("Please remove your finger"))
    while fingerprint2_0.get_enroll_image():
        time.sleep_ms(100)


def enroll(id2, count):
    global \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_res.set_text(str(""))
    i = 0
    while i < count:
        wait_for_finger_press()
        if fingerprint2_0.gen_feature():
            i = (i if isinstance(i, (int, float)) else 0) + 1
            print(i)
        wait_for_finger_left()
    if fingerprint2_0.gen_template():
        if fingerprint2_0.store_template(g_id):
            label_res.set_text(str((str((str("Enroll ID: ") + str(g_id))) + str(" success!"))))
            operation = 0
            label_tip.set_text(str(""))
            if g_id < 98:
                g_id = (g_id if isinstance(g_id, (int, float)) else 0) + 1
            Speaker.tone(666, 100)


def recognize():
    global \
        id2, \
        count, \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_res.set_text(str(""))
    label_tip.set_text(str("Please place your finger"))
    while not (fingerprint2_0.get_verify_image()):
        time.sleep_ms(100)
    label_tip.set_text(str(""))
    if fingerprint2_0.gen_feature():
        res = fingerprint2_0.find_match()
        if res:
            id2 = res[0]
            label_res.set_text(str((str("Recognize ID: ") + str(id2))))
            Speaker.tone(666, 100)
            operation = 0
    if operation != 0:
        operation = 0
        label_res.set_text(str("Recognize failed! "))
        Speaker.tone(999, 200)


def delete(id2):
    global \
        count, \
        operation, \
        i, \
        g_id, \
        res, \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0
    label_res.set_text(str(""))
    if g_id > 0:
        g_id = (g_id if isinstance(g_id, (int, float)) else 0) + -1
    if fingerprint2_0.delete_template(g_id):
        label_res.set_text(str((str("Delete ID: ") + str(g_id))))
    else:
        label_res.set_text(str("Delete failed!"))
        Speaker.tone(999, 200)
    operation = 0


def btn_enroll_clicked_event(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    operation = 1
    Speaker.tone(888, 100)


def btn_recognize_clicked_event(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    operation = 2
    Speaker.tone(888, 100)


def btn_delete_clicked_event(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    Speaker.tone(888, 100)
    operation = 3


def btn_enroll_event_handler(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_enroll_clicked_event(event_struct)
    return


def btn_recognize_event_handler(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_recognize_clicked_event(event_struct)
    return


def btn_delete_event_handler(event_struct):
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_delete_clicked_event(event_struct)
    return


def setup():
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    btn_enroll = m5ui.M5Button(
        text="enroll",
        x=14,
        y=165,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    btn_recognize = m5ui.M5Button(
        text="recognize",
        x=109,
        y=165,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    btn_delete = m5ui.M5Button(
        text="delete",
        x=229,
        y=165,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "Fingerprint enroll, recognize, delete",
        x=14,
        y=9,
        text_c=0x0F6DD1,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_tip = m5ui.M5Label(
        "Tip:",
        x=46,
        y=61,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_res = m5ui.M5Label(
        "Result:",
        x=20,
        y=95,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )

    btn_enroll.add_event_cb(btn_enroll_event_handler, lv.EVENT.ALL, None)
    btn_recognize.add_event_cb(btn_recognize_event_handler, lv.EVENT.ALL, None)
    btn_delete.add_event_cb(btn_delete_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    Speaker.begin()
    Speaker.setVolumePercentage(0.5)
    fingerprint2_0 = Fingerprint2Unit(2, port=(1, 2))
    fingerprint2_0.activate_module()
    fingerprint2_0.set_work_mode(1, save=False)
    btn_enroll.set_size(80, 60)
    btn_enroll.align_to(page0, lv.ALIGN.CENTER, -105, 60)
    btn_recognize.set_size(100, 60)
    btn_recognize.align_to(page0, lv.ALIGN.CENTER, 0, 60)
    btn_delete.set_size(80, 60)
    btn_delete.align_to(page0, lv.ALIGN.CENTER, 105, 60)
    operation = 0
    g_id = 0


def loop():
    global \
        page0, \
        btn_enroll, \
        btn_recognize, \
        btn_delete, \
        label0, \
        label_tip, \
        label_res, \
        fingerprint2_0, \
        operation, \
        i, \
        g_id, \
        count, \
        res, \
        id2
    M5.update()
    if operation == 1:
        enroll(1, 5)
    elif operation == 2:
        recognize()
    elif operation == 3:
        delete(1)
    else:
        pass


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
