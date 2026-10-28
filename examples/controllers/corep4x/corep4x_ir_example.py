# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time

import lvgl as lv
import M5
from M5 import *
import m5ui
from unit import IRUnit


BACKGROUND = 0x080808
PANEL = 0x222224
TEXT = 0xF4F4F5
MUTED = 0x9A9A9F
GOOD = 0x8EDA91

BUTTON_X = 24
BUTTON_Y = 388
BUTTON_W = 432
BUTTON_H = 64
TX_TONE_HZ = 1800
RX_TONE_HZ = 900
TONE_DURATION_MS = 55
TONE_GAP_MS = 25

ir = None
page = None
label_tx = None
label_rx = None
label_count = None
tx_data = 0
rx_count = 0
rx_pending = False
rx_data = 0
rx_addr = 0
tx_pending = False
speaker_ready = False
tone_queue = []
tone_ready_ms = 0


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


def ir_rx_event(data, addr, ctrl):
    global rx_count, rx_pending, rx_data, rx_addr

    rx_count += 1
    rx_data = data
    rx_addr = addr
    rx_pending = True


def queue_tone(frequency):
    if speaker_ready and len(tone_queue) < 4:
        tone_queue.append(frequency)


def update_tone():
    global tone_ready_ms

    if not speaker_ready or not tone_queue:
        return
    now = time.ticks_ms()
    if time.ticks_diff(now, tone_ready_ms) >= 0:
        Speaker.tone(tone_queue.pop(0), TONE_DURATION_MS)
        tone_ready_ms = time.ticks_add(now, TONE_DURATION_MS + TONE_GAP_MS)


def send_button_event(event_struct):
    global tx_pending

    if event_struct.code == lv.EVENT.CLICKED:
        tx_pending = True


def setup():
    global ir, page, label_tx, label_rx, label_count
    global speaker_ready, tone_ready_ms

    M5.begin()
    m5ui.init()
    page = make_page("Infrared")
    panel = make_panel(page, 24, 84, 432, 260)
    make_label(
        panel, "Addr / Data", 140, 20, 272, lv.font_montserrat_18, MUTED, lv.TEXT_ALIGN.RIGHT
    )
    values = []
    for index, name in enumerate(("TX", "RX", "Received")):
        y = 64 + index * 68
        make_label(panel, name, 20, y + 4, 112, lv.font_montserrat_18, MUTED)
        values.append(
            make_label(panel, "--", 140, y, 272, lv.font_montserrat_24, TEXT, lv.TEXT_ALIGN.RIGHT)
        )
    label_tx, label_rx, label_count = values
    label_tx.set_text("Ready")
    label_rx.set_text("Waiting")
    label_count.set_text("0")
    send_button = make_button(page, "SEND NEC", BUTTON_X, BUTTON_Y, BUTTON_W, BUTTON_H)
    send_button.add_event_cb(send_button_event, lv.EVENT.ALL, None)
    page.screen_load()
    # Use the same explicit board IR pins as the graphical IR Unit example.
    ir = IRUnit((13, 49))
    ir.rx_cb(ir_rx_event)
    speaker_ready = Speaker.begin()
    if speaker_ready:
        Speaker.setVolume(128)
    tone_ready_ms = time.ticks_ms()


def loop():
    global tx_data, rx_pending, tx_pending

    M5.update()
    if tx_pending:
        tx_pending = False
        tx_data = (tx_data + 1) & 0xFF
        ir.tx(0x08, tx_data)
        queue_tone(TX_TONE_HZ)
        label_tx.set_text("08 / %02X" % tx_data)
    if rx_pending:
        rx_pending = False
        label_rx.set_text("%02X / %02X" % (rx_addr, rx_data))
        label_count.set_text("%d" % rx_count)
        queue_tone(RX_TONE_HZ)
    update_tone()
    time.sleep_ms(10)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt):
        Speaker.stop()
        Speaker.end()
        m5ui.deinit()
        raise
