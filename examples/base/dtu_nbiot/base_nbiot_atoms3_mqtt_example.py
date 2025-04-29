# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomDTUNBIoT
from hardware import UART


title0 = None
base_nbiot = None
uart2 = None


def base_nbiot_SubTopic_event(_topic, _msg):  # noqa: N802
    global title0, base_nbiot, uart2
    print(_topic)
    print(_msg)


def setup():
    global title0, base_nbiot, uart2

    M5.begin()
    title0 = Widgets.Title("NBIoT MQTT", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    uart2 = UART(2, baudrate=115200, bits=8, parity=None, stop=1, tx=5, rx=6)
    base_nbiot = AtomDTUNBIoT(uart2)
    base_nbiot.mqtt_server_connect("mqtt.m5stack.com", 1883, "m5-mqtt-2024", "", "", 120)
    base_nbiot.mqtt_subscribe_topic("SubTopic", base_nbiot_SubTopic_event, 0)


def loop():
    global title0, base_nbiot, uart2
    M5.update()
    base_nbiot.mqtt_polling_loop()


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
