# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


import os, sys, io
import M5
from M5 import *
from unit import NBIOT2Unit
import time


nbiot2_0 = None


def nbiot2_0_SubTopic_event(_topic, _msg):  # noqa: N802
    global nbiot2_0
    print(_topic)
    print(_msg)


def setup():
    global nbiot2_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    nbiot2_0 = NBIOT2Unit(2, port=(18, 17))
    while not (nbiot2_0.get_gprs_network_status()):
        time.sleep(2)
    nbiot2_0.mqtt_server_configure("mqtt.m5stack.com", 1883, "m5-mqtt-2024", "", "", 120)
    nbiot2_0.mqtt_subscribe_topic("SubTopic", nbiot2_0_SubTopic_event, 0)


def loop():
    global nbiot2_0
    M5.update()
    nbiot2_0.mqtt_polling_loop()


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
