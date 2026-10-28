# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import IR
from hardware.stackchan import StackChan


label_title = None
label_tx_addr = None
label_tx_data = None
label_rx_addr = None
label_rx_data = None
ir = None
stackchan = None
ir_data = None
ir_addr = None
tx_data = None
ir_tx = None
tx_addr = None


def ir_rx_event(_data, _addr, _ctrl):
    global \
        label_title, \
        label_tx_addr, \
        label_tx_data, \
        label_rx_addr, \
        label_rx_data, \
        ir, \
        stackchan, \
        ir_data, \
        ir_addr, \
        tx_data, \
        ir_tx, \
        tx_addr
    ir_data = _data
    ir_addr = _addr
    label_rx_addr.setText(str((str("RX Addr: ") + str(ir_addr))))
    label_rx_data.setText(str((str("RX Data: ") + str(ir_data))))
    Speaker.tone(700, 100)


def btn_pwr_was_clicked_event(state):
    global \
        label_title, \
        label_tx_addr, \
        label_tx_data, \
        label_rx_addr, \
        label_rx_data, \
        ir, \
        stackchan, \
        ir_data, \
        ir_addr, \
        tx_data, \
        ir_tx, \
        tx_addr
    tx_data = (tx_data if isinstance(tx_data, (int, float)) else 0) + 1
    if tx_data > 255:
        tx_data = 0
    ir.tx(tx_addr, tx_data)
    label_tx_addr.setText(str((str("TX Addr: ") + str(tx_addr))))
    label_tx_data.setText(str((str("TX Data: ") + str(tx_data))))


def setup():
    global \
        label_title, \
        label_tx_addr, \
        label_tx_data, \
        label_rx_addr, \
        label_rx_data, \
        ir, \
        stackchan, \
        ir_data, \
        ir_addr, \
        tx_data, \
        ir_tx, \
        tx_addr

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "IR TX & RX Example", 41, 5, 1.0, 0x0DC9F4, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_tx_addr = Widgets.Label(
        "TX Addr:", 9, 59, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_tx_data = Widgets.Label(
        "TX Data:", 170, 59, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_rx_addr = Widgets.Label(
        "RX Addr:", 10, 100, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_rx_data = Widgets.Label(
        "RX Data:", 170, 100, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btn_pwr_was_clicked_event)

    stackchan = StackChan(i2c=1, uart=1)
    ir = IR()
    ir.rx_cb(ir_rx_event)
    tx_addr = 1
    tx_data = 0
    Speaker.begin()
    Speaker.setVolumePercentage(0.5)
    label_tx_addr.setText(str((str("TX Addr: ") + str(tx_addr))))


def loop():
    global \
        label_title, \
        label_tx_addr, \
        label_tx_data, \
        label_rx_addr, \
        label_rx_data, \
        ir, \
        stackchan, \
        ir_data, \
        ir_addr, \
        tx_data, \
        ir_tx, \
        tx_addr
    M5.update()
    if ir_tx:
        ir_tx = False


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
