# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import ATOMSocketBase
from hardware import *


atomsocket = None


as_voltage = None
as_current = None
as_power = None
as_kwh = None
onoff = None


def atom_socket_receive_event(voltage, current, power, kwh):
    global atomsocket, as_voltage, as_current, as_power, as_kwh, onoff
    as_voltage = voltage
    as_current = current
    as_power = power
    as_kwh = kwh
    print("hello M5")
    print("hello M5")


def btnA_wasClicked_event(state):  # noqa: N802
    global atomsocket, as_voltage, as_current, as_power, as_kwh, onoff
    onoff = not onoff
    if onoff:
        atomsocket.set_relay(True)
    else:
        atomsocket.set_relay(False)


def setup():
    global atomsocket, as_voltage, as_current, as_power, as_kwh, onoff

    M5.begin()
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)

    atomsocket = ATOMSocketBase(1, port=(22, 33), relay=23)
    onoff = False
    atomsocket.set_relay(False)
    atomsocket.receive_none_block(atom_socket_receive_event)


def loop():
    global atomsocket, as_voltage, as_current, as_power, as_kwh, onoff
    M5.update()


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
