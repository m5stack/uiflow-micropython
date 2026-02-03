# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from umqtt import MQTTClient


page0 = None
label0 = None
button0 = None
textarea0 = None
label1 = None
textarea1 = None
label2 = None
keyboard0 = None
mqtt_client = None


def button0_short_clicked_event(event_struct):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    mqtt_client.publish("testtopic/test", textarea0.get_text(), qos=0)


def mqtt_testtopic_test_event(data):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    textarea1.set_text(str(data[1]))


def textarea0_focused_event(event_struct):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, False)


def textarea0_defocused_event(event_struct):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, True)


def button0_event_handler(event_struct):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button0_short_clicked_event(event_struct)
    return


def textarea0_event_handler(event_struct):
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    event = event_struct.code
    if event == lv.EVENT.FOCUSED and True:
        textarea0_focused_event(event_struct)
    if event == lv.EVENT.DEFOCUSED and True:
        textarea0_defocused_event(event_struct)
    return


def setup():
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="textarea0",
        placeholder="Placeholder...",
        x=52,
        y=32,
        w=150,
        h=70,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    textarea1 = m5ui.M5TextArea(
        text="textarea1",
        placeholder="Placeholder...",
        x=10,
        y=132,
        w=150,
        h=70,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "pubish topic: testtopic/test",
        x=10,
        y=10,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    button0 = m5ui.M5Button(
        text="publish",
        x=217,
        y=32,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "subscribe topic: testtopic/test",
        x=11,
        y=110,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label2 = m5ui.M5Label(
        "msg:",
        x=10,
        y=32,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    keyboard0 = m5ui.M5Keyboard(
        x=0,
        y=120,
        w=320,
        h=120,
        mode=lv.keyboard.MODE.TEXT_LOWER,
        target_textarea=textarea0,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)
    textarea0.add_event_cb(textarea0_event_handler, lv.EVENT.ALL, None)

    page0.set_flag(lv.obj.FLAG.SCROLLABLE, True)
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, True)
    page0.screen_load()
    mqtt_client = MQTTClient(
        "uiflow",
        "y90166f4.ala.cn-hangzhou.emqxsl.cn",
        port=8883,
        user="test",
        password="test",
        keepalive=0,
        ssl=True,
        ssl_params={
            "cafile": "/flash/certificate/emqxsl-ca.crt",
            "server_hostname": "y90166f4.ala.cn-hangzhou.emqxsl.cn",
        },
    )
    mqtt_client.connect(clean_session=True)
    mqtt_client.subscribe("testtopic/test", mqtt_testtopic_test_event, qos=0)


def loop():
    global page0, label0, button0, textarea0, label1, textarea1, label2, keyboard0, mqtt_client
    M5.update()
    mqtt_client.check_msg()


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
