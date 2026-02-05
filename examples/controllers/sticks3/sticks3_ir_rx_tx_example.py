# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import IR


label_title = None
label_tx_addr = None
label_rx_addr = None
label_tx_data = None
label_rx_data = None
label_rx_cnt = None
label_tip = None
ir = None
rx_data = None
rx_addr = None
rx_cnt = None
tx_data = None
tx_addr = None


def ir_rx_event(_data, _addr, _ctrl):
    global \
        label_title, \
        label_tx_addr, \
        label_rx_addr, \
        label_tx_data, \
        label_rx_data, \
        label_rx_cnt, \
        label_tip, \
        ir, \
        rx_data, \
        rx_addr, \
        rx_cnt, \
        tx_data, \
        tx_addr
    rx_data = _data
    rx_addr = _addr
    rx_cnt = (rx_cnt if isinstance(rx_cnt, (int, float)) else 0) + 1
    label_rx_cnt.setText(str((str("rx count: ") + str(rx_cnt))))
    label_rx_addr.setText(str((str("rx addr: ") + str(rx_addr))))
    label_rx_data.setText(str((str("rx data: ") + str(rx_data))))


def btna_click_event_cb(state):
    global \
        label_title, \
        label_tx_addr, \
        label_rx_addr, \
        label_tx_data, \
        label_rx_data, \
        label_rx_cnt, \
        label_tip, \
        ir, \
        rx_data, \
        rx_addr, \
        rx_cnt, \
        tx_data, \
        tx_addr
    tx_data = (tx_data if isinstance(tx_data, (int, float)) else 0) + 1
    ir.tx(tx_addr, tx_data)
    print((str("IR: Send addr: ") + str((str(tx_addr) + str((str("data: ") + str(tx_data)))))))
    label_tx_data.setText(str((str("tx data: ") + str(tx_data))))


def setup():
    global \
        label_title, \
        label_tx_addr, \
        label_rx_addr, \
        label_tx_data, \
        label_rx_data, \
        label_rx_cnt, \
        label_tip, \
        ir, \
        rx_data, \
        rx_addr, \
        rx_cnt, \
        tx_data, \
        tx_addr

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "IR TX & RX", 15, 5, 1.0, 0x1AEAEB, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_tx_addr = Widgets.Label(
        "tx addr:", 5, 135, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_rx_addr = Widgets.Label(
        "rx addr:", 5, 70, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_tx_data = Widgets.Label(
        "tx data:", 5, 160, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_rx_data = Widgets.Label(
        "rx data:", 5, 95, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_rx_cnt = Widgets.Label(
        "rx count:", 5, 45, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )
    label_tip = Widgets.Label(
        "BtnA Send", 18, 200, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_click_event_cb)

    ir = IR()
    ir.rx_cb(ir_rx_event)
    rx_addr = 0
    rx_data = 0
    tx_addr = 8
    tx_data = 0
    Power.setExtOutput(True)
    Speaker.setPA(False)
    label_tx_addr.setText(str((str("tx addr: ") + str(tx_addr))))
    rx_cnt = 0


def loop():
    global \
        label_title, \
        label_tx_addr, \
        label_rx_addr, \
        label_tx_data, \
        label_rx_data, \
        label_rx_cnt, \
        label_tip, \
        ir, \
        rx_data, \
        rx_addr, \
        rx_cnt, \
        tx_data, \
        tx_addr
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
