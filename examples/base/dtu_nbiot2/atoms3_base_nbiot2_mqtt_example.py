# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import UART
from base import AtomRS485
from base import AtomDTUNBIoT2


label0 = None
base_nbiot2 = None
uart2 = None
base_rs485 = None
base_nbiot2_mqtt = None


def base_nbiot2_testtopic_a_event(data):
    global label0, base_nbiot2, uart2, base_rs485, base_nbiot2_mqtt
    label0.setText(str(data[1]))


def setup():
    global label0, base_nbiot2, uart2, base_rs485, base_nbiot2_mqtt

    M5.begin()
    Widgets.fillScreen(0x000000)
    label0 = Widgets.Label("label0", 8, 7, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    uart2 = UART(2, baudrate=115200, bits=8, parity=None, stop=1, tx=5, rx=6)
    base_rs485 = AtomRS485(
        1,
        baudrate=115200,
        bits=8,
        parity=None,
        stop=1,
        tx=7,
        rx=8,
        txbuf=256,
        rxbuf=256,
        timeout=0,
        timeout_char=0,
        invert=0,
        flow=0,
    )
    base_nbiot2 = AtomDTUNBIoT2(uart2, verbose=False)
    base_nbiot2.connect(apn="cmnbiot")
    while not (base_nbiot2.isconnected()):
        pass
    base_nbiot2_mqtt = base_nbiot2.MQTTClient(
        "uiflow2-client", "mqtt.m5stack.com", port=1883, user="", password="", keepalive=0
    )
    base_nbiot2_mqtt.connect(clean_session=False)
    base_nbiot2_mqtt.subscribe("testtopic/a", base_nbiot2_testtopic_a_event, qos=0)


def loop():
    global label0, base_nbiot2, uart2, base_rs485, base_nbiot2_mqtt
    M5.update()
    base_nbiot2_mqtt.check_msg()


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
