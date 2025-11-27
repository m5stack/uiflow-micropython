# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from unit import Cat1Unit


page0 = None
button0 = None
cat1cn_0 = None


import random


def cat1cn_0_subscription_event(_topic, _msg):
    global page0, button0, cat1cn_0
    print(_topic)
    print(_msg)


def button0_clicked_event(event_struct):
    global page0, button0, cat1cn_0
    cat1cn_0.mqtt_publish_topic(
        "Subscription", (str("Random num:") + str((str((random.randint(1, 100)))))), 0
    )


def button0_event_handler(event_struct):
    global page0, button0, cat1cn_0
    event = event_struct.code
    if event == lv.EVENT.CLICKED and True:
        button0_clicked_event(event_struct)
    return


def setup():
    global page0, button0, cat1cn_0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    button0 = m5ui.M5Button(
        text="Send Msg",
        x=107,
        y=100,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)

    cat1cn_0 = Cat1Unit(2, port=(33, 32))
    page0.screen_load()
    cat1cn_0.mqtt_server_connect("broker-cn.emqx.io", 1883, "mqttx_b899ee59", "", "", 120)
    cat1cn_0.mqtt_subscribe_topic("Subscription", cat1cn_0_subscription_event, 0)


def loop():
    global page0, button0, cat1cn_0
    M5.update()
    cat1cn_0.mqtt_polling_loop()


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
