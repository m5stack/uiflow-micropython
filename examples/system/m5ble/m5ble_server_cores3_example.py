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


server = None
client_handle = None
service_uuid = None
char_uuid = None
char_uuid_2 = None


def ble_server_on_receive_event(args):
    _server, _connected_client_handle = args
    global \
        _labelRecv, \
        labelRecv, \
        _labelStatus, \
        labelStatus, \
        ble, \
        server, \
        client_handle, \
        service_uuid, \
        char_uuid, \
        char_uuid_2
    server = _server
    client_handle = _connected_client_handle
    labelRecv.setText(str(client_handle.read("F49F3F31-398A-1980-B25F-2059B7B57637", 0)))


def ble_server_on_connected_event(args):
    _server, _connected_client_handle = args
    global \
        _labelRecv, \
        labelRecv, \
        _labelStatus, \
        labelStatus, \
        ble, \
        server, \
        client_handle, \
        service_uuid, \
        char_uuid, \
        char_uuid_2
    server = _server
    client_handle = _connected_client_handle
    labelStatus.setColor(0x00FF00, 0x000000)
    labelStatus.setText(str("connected"))


def ble_server_on_disconnected_event(args):
    _server, _connected_client_handle = args
    global \
        _labelRecv, \
        labelRecv, \
        _labelStatus, \
        labelStatus, \
        ble, \
        server, \
        client_handle, \
        service_uuid, \
        char_uuid, \
        char_uuid_2
    server = _server
    client_handle = _connected_client_handle
    labelStatus.setColor(0xFF0000, 0x000000)
    labelStatus.setText(str("disconnected"))


def setup():
    global \
        _labelRecv, \
        labelRecv, \
        _labelStatus, \
        labelStatus, \
        ble, \
        server, \
        client_handle, \
        service_uuid, \
        char_uuid, \
        char_uuid_2

    M5.begin()
    Widgets.fillScreen(0x222222)
    _labelRecv = Widgets.Label("Recv: ", 9, 11, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    labelRecv = Widgets.Label("--", 68, 11, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    _labelStatus = Widgets.Label(
        "Status:", 10, 48, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    labelStatus = Widgets.Label("--", 82, 48, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    ble = M5BLE.Device()
    ble.server.on_receive(ble_server_on_receive_event)
    ble.server.on_connected(ble_server_on_connected_event)
    ble.server.on_disconnected(ble_server_on_disconnected_event)
    service_uuid = "F49F0000-398A-1980-B25F-2059B7B57637"
    char_uuid = "F49F3F30-398A-1980-B25F-2059B7B57637"
    char_uuid_2 = "F49F3F31-398A-1980-B25F-2059B7B57637"
    ble.server.add_service(
        service_uuid,
        [
            ble.server.create_characteristic(char_uuid, True, False, True),
            ble.server.create_characteristic(char_uuid_2, False, True, False),
        ],
    )
    ble.server.start(500000)


def loop():
    global \
        _labelRecv, \
        labelRecv, \
        _labelStatus, \
        labelStatus, \
        ble, \
        server, \
        client_handle, \
        service_uuid, \
        char_uuid, \
        char_uuid_2
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
