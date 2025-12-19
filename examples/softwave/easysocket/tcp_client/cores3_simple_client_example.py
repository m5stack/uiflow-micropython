# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from easysocket import EasyTCPClient
import network


page0 = None
button0 = None
button1 = None
label0 = None
button2 = None
textarea0 = None
keyboard0 = None
label1 = None
textarea1 = None
textarea2 = None
label3 = None
wlan_sta = None
tcpc_0 = None


state = None


def button0_short_clicked_event(event_struct):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    state = not state
    if state:
        tcpc_0.connect()
        button0.set_btn_text(str("connecting"))
        button0.set_bg_color(0xFFCC66, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    else:
        tcpc_0.close()
        button0.set_btn_text(str("connect"))
        button0.set_bg_color(0x3366FF, 255, lv.PART.MAIN | lv.STATE.DEFAULT)


def tcpc_0_connect_event(client_sock):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    button0.set_btn_text(str("connected"))
    button0.set_bg_color(0xFF0000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)


def tcpc_0_disconnect_event(client_sock):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    button0.set_btn_text(str("connect"))
    button0.set_bg_color(0x3366FF, 255, lv.PART.MAIN | lv.STATE.DEFAULT)


def textarea0_focused_event(event_struct):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, False)
    keyboard0.set_textarea(textarea0)


def textarea0_defocused_event(event_struct):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, True)


def textarea1_focused_event(event_struct):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, False)
    keyboard0.set_textarea(textarea1)


def textarea1_defocused_event(event_struct):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, True)


def textarea2_focused_event(event_struct):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, False)
    keyboard0.set_textarea(textarea2)


def textarea2_defocused_event(event_struct):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, True)


def button2_short_clicked_event(event_struct):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    textarea2.set_text("")


def button1_short_clicked_event(event_struct):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    tcpc_0.send(textarea2.get_text())


def button0_event_handler(event_struct):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button0_short_clicked_event(event_struct)
    return


def textarea0_event_handler(event_struct):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    event = event_struct.code
    if event == lv.EVENT.FOCUSED and True:
        textarea0_focused_event(event_struct)
    if event == lv.EVENT.DEFOCUSED and True:
        textarea0_defocused_event(event_struct)
    return


def textarea1_event_handler(event_struct):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    event = event_struct.code
    if event == lv.EVENT.FOCUSED and True:
        textarea1_focused_event(event_struct)
    if event == lv.EVENT.DEFOCUSED and True:
        textarea1_defocused_event(event_struct)
    return


def textarea2_event_handler(event_struct):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    event = event_struct.code
    if event == lv.EVENT.FOCUSED and True:
        textarea2_focused_event(event_struct)
    if event == lv.EVENT.DEFOCUSED and True:
        textarea2_defocused_event(event_struct)
    return


def button2_event_handler(event_struct):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button2_short_clicked_event(event_struct)
    return


def button1_event_handler(event_struct):
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button1_short_clicked_event(event_struct)
    return


def setup():
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
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
        text="",
        placeholder="Placeholder...",
        x=6,
        y=76,
        w=232,
        h=158,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )
    button0 = m5ui.M5Button(
        text="connect",
        x=239,
        y=6,
        bg_c=0x214FF3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    button1 = m5ui.M5Button(
        text="send",
        x=248,
        y=76,
        bg_c=0x214FF3,
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
    button2 = m5ui.M5Button(
        text="clear",
        x=248,
        y=201,
        bg_c=0x214FF3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    keyboard0 = m5ui.M5Keyboard(
        x=0,
        y=119,
        w=320,
        h=120,
        mode=lv.keyboard.MODE.TEXT_LOWER,
        target_textarea=None,
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
        "Data:",
        x=6,
        y=50,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)
    textarea0.add_event_cb(textarea0_event_handler, lv.EVENT.ALL, None)
    textarea1.add_event_cb(textarea1_event_handler, lv.EVENT.ALL, None)
    textarea2.add_event_cb(textarea2_event_handler, lv.EVENT.ALL, None)
    button2.add_event_cb(button2_event_handler, lv.EVENT.ALL, None)
    button1.add_event_cb(button1_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    wlan_sta = network.WLAN(network.STA_IF)
    wlan_sta.active(True)
    button0.set_size(74, 36)
    textarea0.set_one_line(True)
    textarea1.set_one_line(True)
    textarea0.set_text(str(wlan_sta.ifconfig()[0]))
    textarea1.set_text(str("8000"))
    state = True
    tcpc_0 = EasyTCPClient("192.168.8.196", 8000)
    tcpc_0.on_connect(tcpc_0_connect_event)
    tcpc_0.on_disconnect(tcpc_0_disconnect_event)
    button0.set_btn_text(str("connecting"))
    keyboard0.set_flag(lv.obj.FLAG.HIDDEN, True)


def loop():
    global \
        page0, \
        button0, \
        button1, \
        label0, \
        button2, \
        textarea0, \
        keyboard0, \
        label1, \
        textarea1, \
        textarea2, \
        label3, \
        wlan_sta, \
        tcpc_0, \
        state
    M5.update()
    tcpc_0.check_event(timeout=-1)


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
