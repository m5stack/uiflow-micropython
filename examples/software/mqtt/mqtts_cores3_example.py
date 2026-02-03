# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from umqtt import *


label0 = None
mqtt_client = None


def mqtt_testtopic_event(data):
    global label0, mqtt_client
    label0.setText(str(data[1]))


def setup():
    global label0, mqtt_client

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Text", 25, 20, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    mqtt_client = MQTTClient(
        "umqtt-client",
        "emqxsl.cn",
        port=8883,
        user="test",
        password="test",
        keepalive=60,
        ssl=True,
        ssl_params={"server_hostname": "emqxsl.cn"},
    )
    mqtt_client.connect(clean_session=True)
    mqtt_client.subscribe("testtopic", mqtt_testtopic_event, qos=0)


def loop():
    global label0, mqtt_client
    M5.update()
    mqtt_client.check_msg()


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
