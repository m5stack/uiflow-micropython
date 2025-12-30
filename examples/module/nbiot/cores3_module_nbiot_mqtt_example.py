# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from module import NBIOTModule


page0 = None
label0 = None
nbiotmodule_0 = None
nbiotmodule_0_mqtt = None


def nbiotmodule_0__testtopic_a_event(data):
    global page0, label0, nbiotmodule_0, nbiotmodule_0_mqtt
    label0.set_text(str(data[1]))


def setup():
    global page0, label0, nbiotmodule_0, nbiotmodule_0_mqtt

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label0 = m5ui.M5Label(
        "label0",
        x=130,
        y=105,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    page0.screen_load()
    nbiotmodule_0 = NBIOTModule(2, 17, 18)
    nbiotmodule_0.connect(apn="cmnbiot")
    while not (nbiotmodule_0.isconnected()):
        pass
    nbiotmodule_0_mqtt = nbiotmodule_0.MQTTClient(
        "uiflow2-client", "mqtt.m5stack.com", port=1883, user="", password="", keepalive=0
    )
    nbiotmodule_0_mqtt.connect(clean_session=False)
    nbiotmodule_0_mqtt.subscribe("testtopic/a", nbiotmodule_0__testtopic_a_event, qos=0)


def loop():
    global page0, label0, nbiotmodule_0, nbiotmodule_0_mqtt
    M5.update()
    nbiotmodule_0_mqtt.check_msg()


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
