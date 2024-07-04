# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from m5ble import *


_labelRecv = None
labelRecv = None
_labelStatus = None
labelStatus = None
ble = None


client = None
conn_handle = None
addr_type = None
addr = None


def ble_client_on_connected_event(args):
    _client = args
    global \
        _labelRecv, \
        labelRecv, \
        _labelStatus, \
        labelStatus, \
        ble, \
        client, \
        conn_handle, \
        addr_type, \
        addr
    client = _client
    _labelRecv.setColor(0x33FF33, 0x000000)
    labelStatus.setText(str("connected"))


def ble_client_on_disconnected_event(args):
    _client, _conn_handle, _addr_type, _addr = args
    global \
        _labelRecv, \
        labelRecv, \
        _labelStatus, \
        labelStatus, \
        ble, \
        client, \
        conn_handle, \
        addr_type, \
        addr
    client = _client
    conn_handle = _conn_handle
    addr_type = _addr_type
    addr = _addr
    _labelRecv.setColor(0xFF0000, 0x000000)
    labelStatus.setText(str("disconnected"))


def ble_client_on_notify_event(args):
    _client = args
    global \
        _labelRecv, \
        labelRecv, \
        _labelStatus, \
        labelStatus, \
        ble, \
        client, \
        conn_handle, \
        addr_type, \
        addr
    client = _client
    labelRecv.setText(
        str(
            ble.client.read(
                "F49F0000-398A-1980-B25F-2059B7B57637", "F49F0000-398A-1980-B25F-2059B7B57637", 0
            )
        )
    )


def setup():
    global \
        _labelRecv, \
        labelRecv, \
        _labelStatus, \
        labelStatus, \
        ble, \
        client, \
        conn_handle, \
        addr_type, \
        addr

    M5.begin()
    Widgets.fillScreen(0x222222)
    _labelRecv = Widgets.Label("Recv: ", 9, 11, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    labelRecv = Widgets.Label("--", 68, 11, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    _labelStatus = Widgets.Label(
        "Status:", 10, 48, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    labelStatus = Widgets.Label("--", 82, 48, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    ble = M5BLE.Device()
    ble.client.on_connected(ble_client_on_connected_event)
    ble.client.on_disconnected(ble_client_on_disconnected_event)
    ble.client.on_notify(ble_client_on_notify_event)
    ble.client.scan(5000, True, "M5BLETest", None)


def loop():
    global \
        _labelRecv, \
        labelRecv, \
        _labelStatus, \
        labelStatus, \
        ble, \
        client, \
        conn_handle, \
        addr_type, \
        addr
    M5.update()


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            ble.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
