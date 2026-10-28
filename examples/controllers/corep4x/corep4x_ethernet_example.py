# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import socket
import struct
import time

import lvgl as lv
import machine
import network
import M5
from M5 import *
import m5ui
from hardware import RTC


BACKGROUND = 0x080808
PANEL = 0x222224
TEXT = 0xF4F4F5
MUTED = 0x9A9A9F
GOOD = 0x8EDA91
WARNING = 0xFFB84D

NTP_HOST = "ntp.aliyun.com"
NTP_DELTA = 2208988800
UTC_OFFSET = 8 * 60 * 60

ethernet = None
rtc = None
page = None
label_link = None
label_ip = None
label_date = None
label_hour = None
label_minute = None
label_second = None
label_ntp = None
sync_button = None
last_connected = None
last_update_ms = 0
ntp_epoch = None
ntp_ticks_ms = 0
sync_pending = False


def make_label(parent, text, x, y, width, font, color=TEXT, align=lv.TEXT_ALIGN.LEFT):
    label = m5ui.M5Label(text, x, y, color, BACKGROUND, 0, font, parent)
    label.set_width(width)
    label.set_style_text_align(align, lv.PART.MAIN)
    label.remove_flag(lv.obj.FLAG.CLICKABLE)
    return label


def make_page(title):
    screen = m5ui.M5Page(bg_c=BACKGROUND)
    screen.set_style_pad_all(0, lv.PART.MAIN)
    screen.set_style_border_width(0, lv.PART.MAIN)
    screen.set_style_shadow_width(0, lv.PART.MAIN)
    screen.remove_flag(lv.obj.FLAG.SCROLLABLE)
    make_label(screen, title, 24, 24, 432, lv.font_montserrat_24)
    return screen


def make_panel(parent, x, y, width, height, color=PANEL):
    panel = lv.obj(parent)
    panel.remove_style_all()
    panel.set_pos(x, y)
    panel.set_size(width, height)
    panel.set_style_radius(24, lv.PART.MAIN)
    panel.set_style_pad_all(0, lv.PART.MAIN)
    panel.set_style_bg_color(lv.color_hex(color), lv.PART.MAIN)
    panel.set_style_bg_opa(255, lv.PART.MAIN)
    panel.remove_flag(lv.obj.FLAG.SCROLLABLE)
    panel.remove_flag(lv.obj.FLAG.CLICKABLE)
    return panel


def make_button(parent, text, x, y, width, height, color=0x303034):
    button = m5ui.M5Button(text, x, y, width, height, color, TEXT, lv.font_montserrat_18, parent)
    button.set_style_radius(18, lv.PART.MAIN)
    button.set_style_pad_all(0, lv.PART.MAIN)
    button.set_style_shadow_width(0, lv.PART.MAIN)
    button.set_style_shadow_width(0, lv.PART.MAIN | lv.STATE.PRESSED)
    button.label.set_width(width - 16)
    button.label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)
    button.label.center()
    return button


def query_ntp(host):
    query = bytearray(48)
    query[0] = 0x1B
    address = socket.getaddrinfo(host, 123, 0, socket.SOCK_DGRAM)[0][-1]
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(3)
    try:
        sock.sendto(query, address)
        response = sock.recv(48)
    finally:
        sock.close()
    return struct.unpack("!I", response[40:44])[0] - NTP_DELTA


def format_datetime(epoch):
    value = time.gmtime(epoch + UTC_OFFSET)
    date_text = "%04d-%02d-%02d" % value[:3]
    time_text = "%02d:%02d:%02d" % value[3:6]
    return date_text, time_text


def set_label_color(label, color):
    label.set_text_color(color, 255, lv.PART.MAIN | lv.STATE.DEFAULT)


def set_clock(epoch):
    date_text, time_text = format_datetime(epoch)
    label_date.set_text(date_text)
    label_hour.set_text(time_text[0:2])
    label_minute.set_text(time_text[3:5])
    label_second.set_text(time_text[6:8])
    set_label_color(label_hour, GOOD)
    set_label_color(label_minute, GOOD)
    set_label_color(label_second, GOOD)


def sync_time():
    global ntp_epoch, ntp_ticks_ms

    label_ntp.set_text("Syncing...")
    set_label_color(label_ntp, WARNING)
    for attempt in range(1, 4):
        try:
            ntp_epoch = query_ntp(NTP_HOST)
            ntp_ticks_ms = time.ticks_ms()
            utc = time.gmtime(ntp_epoch)
            rtc.init((utc[0], utc[1], utc[2], utc[3], utc[4], utc[5], utc[6], 0))
            set_clock(ntp_epoch)
            label_ntp.set_text("Synced / UTC+8")
            set_label_color(label_ntp, GOOD)
            return True
        except OSError:
            time.sleep(1)
    label_ntp.set_text("Sync failed")
    set_label_color(label_ntp, WARNING)
    return False


def refresh_status():
    global last_connected

    connected = ethernet.isconnected()
    ip = ethernet.ifconfig()[0] if connected else "0.0.0.0"
    label_link.set_text("Connected" if connected else "No link")
    set_label_color(label_link, GOOD if connected else WARNING)
    label_ip.set_text(ip)
    last_connected = connected


def sync_button_event(event_struct):
    global sync_pending

    if event_struct.code == lv.EVENT.CLICKED:
        sync_pending = True


def setup():
    global ethernet, rtc, page, label_link, label_ip, label_date
    global label_hour, label_minute, label_second, label_ntp, sync_button
    global last_update_ms

    M5.begin()
    rtc = RTC()
    m5ui.init()
    page = make_page("Ethernet")
    panel = make_panel(page, 24, 84, 432, 280)
    make_label(panel, "Link", 20, 24, 100, lv.font_montserrat_18, MUTED)
    label_link = make_label(
        panel, "Starting", 140, 24, 272, lv.font_montserrat_18, WARNING, lv.TEXT_ALIGN.RIGHT
    )
    make_label(panel, "IP", 20, 64, 100, lv.font_montserrat_18, MUTED)
    label_ip = make_label(
        panel, "--", 140, 64, 272, lv.font_montserrat_18, TEXT, lv.TEXT_ALIGN.RIGHT
    )
    label_date = make_label(
        panel, "---- -- --", 24, 116, 384, lv.font_montserrat_24, TEXT, lv.TEXT_ALIGN.CENTER
    )
    digits = []
    for x in (52, 168, 284):
        digits.append(
            make_label(panel, "--", x, 158, 96, lv.font_montserrat_48, GOOD, lv.TEXT_ALIGN.CENTER)
        )
    label_hour, label_minute, label_second = digits
    for x in (155, 271):
        for y in (171, 189):
            dot = make_panel(panel, x, y, 6, 6, GOOD)
            dot.set_style_radius(3, lv.PART.MAIN)
    label_ntp = make_label(
        panel, "Waiting", 24, 236, 384, lv.font_montserrat_18, MUTED, lv.TEXT_ALIGN.CENTER
    )
    sync_button = make_button(page, "SYNC NTP", 24, 388, 432, 64)
    sync_button.add_event_cb(sync_button_event, lv.EVENT.ALL, None)
    page.screen_load()

    ethernet = network.LAN(
        0,
        phy_addr=1,
        phy_type=network.PHY_IP101,
        mdc=machine.Pin(31),
        mdio=machine.Pin(36),
        power=machine.Pin(52),
        ref_clk=machine.Pin(32),
        tx_en=machine.Pin(33),
        txd0=machine.Pin(41),
        txd1=machine.Pin(35),
        crs_dv=machine.Pin(28),
        rxd0=machine.Pin(29),
        rxd1=machine.Pin(30),
    )
    ethernet.active(True)
    ethernet.set_default_netif()

    deadline = time.ticks_add(time.ticks_ms(), 30000)
    while not ethernet.isconnected() and time.ticks_diff(deadline, time.ticks_ms()) > 0:
        M5.update()
        refresh_status()
        time.sleep_ms(200)
    refresh_status()
    if ethernet.isconnected():
        sync_time()
    else:
        label_ntp.set_text("No network")
        set_label_color(label_ntp, WARNING)
    last_update_ms = time.ticks_ms()


def loop():
    global last_update_ms, sync_pending, last_connected

    M5.update()
    if sync_pending:
        sync_pending = False
        if ethernet.isconnected():
            sync_time()
        else:
            label_ntp.set_text("No network")
            set_label_color(label_ntp, WARNING)
    now = time.ticks_ms()
    if time.ticks_diff(now, last_update_ms) >= 1000:
        last_update_ms = now
        was_connected = last_connected
        refresh_status()
        if ethernet.isconnected() and was_connected is False:
            sync_time()
        if ntp_epoch is not None:
            elapsed = time.ticks_diff(now, ntp_ticks_ms) // 1000
            set_clock(ntp_epoch + elapsed)
    time.sleep_ms(10)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt):
        m5ui.deinit()
        raise
