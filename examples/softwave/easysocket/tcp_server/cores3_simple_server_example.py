# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from easysocket import EasyTCPServer
import network


page0 = None
button0 = None
label0 = None
textarea0 = None
label1 = None
textarea1 = None
textarea2 = None
label3 = None
wlan_sta = None
tcps_0 = None


client = None
received_data = None
state = None


def tcps_0_connect_event(client_sock):
    global \
        page0, \
        button0, \
        label0, \
        textarea0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcps_0, \
        client, \
        received_data, \
        state
    client = client_sock
    textarea2.add_text(str("new clinet: "))
    textarea2.add_text(str(client.getpeername()[0]))
    textarea2.add_text(str("\n"))


def tcps_0_received_event(args):
    global \
        page0, \
        button0, \
        label0, \
        textarea0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcps_0, \
        client, \
        received_data, \
        state
    client, received_data = args
    textarea2.add_text(str(client.getpeername()[0]))
    textarea2.add_text(str(":"))
    textarea2.add_text(str(received_data))
    textarea2.add_text(str("\n"))


def tcps_0_disconnect_event(client_sock):
    global \
        page0, \
        button0, \
        label0, \
        textarea0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcps_0, \
        client, \
        received_data, \
        state
    client = client_sock
    textarea2.add_text(str(client.getpeername()[0]))
    textarea2.add_text(str(" disconnected\n"))


def button0_short_clicked_event(event_struct):
    global \
        page0, \
        button0, \
        label0, \
        textarea0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcps_0, \
        client, \
        received_data, \
        state
    state = not state
    if state:
        textarea2.set_text("")
        tcps_0.start()
        button0.set_btn_text(str("stop"))
        button0.set_bg_color(0xFF0000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    else:
        tcps_0.stop()
        button0.set_btn_text(str("start"))
        button0.set_bg_color(0x3366FF, 255, lv.PART.MAIN | lv.STATE.DEFAULT)


def button0_event_handler(event_struct):
    global \
        page0, \
        button0, \
        label0, \
        textarea0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcps_0, \
        client, \
        received_data, \
        state
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button0_short_clicked_event(event_struct)
    return


def setup():
    global \
        page0, \
        button0, \
        label0, \
        textarea0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcps_0, \
        client, \
        received_data, \
        state

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="textarea0",
        placeholder="Placeholder...",
        x=40,
        y=6,
        w=70,
        h=36,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    textarea1 = m5ui.M5TextArea(
        text="textarea0",
        placeholder="Placeholder...",
        x=178,
        y=6,
        w=56,
        h=36,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    textarea2 = m5ui.M5TextArea(
        text="Text",
        placeholder="Placeholder...",
        x=6,
        y=76,
        w=308,
        h=158,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    button0 = m5ui.M5Button(
        text="stop",
        x=239,
        y=6,
        bg_c=0xF32121,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "IP:",
        x=6,
        y=10,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "Port:",
        x=116,
        y=10,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label3 = m5ui.M5Label(
        "Log:",
        x=6,
        y=50,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(True)
    tcps_0 = EasyTCPServer(host="0.0.0.0", port=8000, listen=0, verbose=True)
    tcps_0.on_client_connect(tcps_0_connect_event)
    tcps_0.on_data_received(tcps_0_received_event)
    tcps_0.on_client_disconnect(tcps_0_disconnect_event)
    button0.set_size(74, 36)
    textarea0.set_one_line(True)
    textarea1.set_one_line(True)
    textarea0.set_text(str(wlan_sta.ifconfig()[0]))
    textarea1.set_text(str("8000"))
    state = True


def loop():
    global \
        page0, \
        button0, \
        label0, \
        textarea0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcps_0, \
        client, \
        received_data, \
        state
    M5.update()
    tcps_0.check_event(timeout=10)


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
