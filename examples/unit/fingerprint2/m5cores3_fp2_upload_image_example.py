# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from unit import Fingerprint2Unit
import time


page0 = None
canvas0 = None
btn_upload = None
label0 = None
fingerprint2_0 = None
upload = None
fpimg = None


# Describe this function...
def upload_image():
    global upload, fpimg, page0, canvas0, btn_upload, label0, fingerprint2_0
    Speaker.tone(666, 100)
    label0.set_text(str("Please press finger"))
    while not (fingerprint2_0.get_enroll_image()):
        print(".")
        time.sleep_ms(1000)
    label0.set_text(str("Uploading..."))
    fpimg = fingerprint2_0.upload_image(to_rgb565=True, byte_order=True)
    if fpimg:
        Speaker.tone(666, 100)
        label0.set_text(str("Upload image finished!"))
        canvas0.set_buffer(fpimg, 80, 208, lv.COLOR_FORMAT.RGB565)
        upload = False
    else:
        Speaker.tone(888, 200)
        label0.set_text(str("Upload image failed!"))
    upload = False


def btn_upload_clicked_event(event_struct):
    global page0, canvas0, btn_upload, label0, fingerprint2_0, upload, fpimg
    upload = True


def btn_upload_event_handler(event_struct):
    global page0, canvas0, btn_upload, label0, fingerprint2_0, upload, fpimg
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        btn_upload_clicked_event(event_struct)
    return


def setup():
    global page0, canvas0, btn_upload, label0, fingerprint2_0, upload, fpimg
    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    canvas0 = m5ui.M5Canvas(
        x=115,
        y=25,
        w=80,
        h=208,
        color_format=lv.COLOR_FORMAT.ARGB8888,
        bg_c=0xC9C9C9,
        bg_opa=255,
        parent=page0,
    )
    btn_upload = m5ui.M5Button(
        text="upload",
        x=216,
        y=144,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "tip",
        x=6,
        y=3,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    btn_upload.add_event_cb(btn_upload_event_handler, lv.EVENT.ALL, None)
    fingerprint2_0 = Fingerprint2Unit(2, port=(1, 2))
    page0.screen_load()
    Speaker.begin()
    Speaker.setVolumePercentage(0.8)
    btn_upload.set_size(80, 60)
    upload = True
    upload_image()


def loop():
    global page0, canvas0, btn_upload, label0, fingerprint2_0, upload, fpimg
    M5.update()
    if upload:
        upload_image()


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
