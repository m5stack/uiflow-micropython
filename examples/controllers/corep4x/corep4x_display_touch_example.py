# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import time

import lvgl as lv
import M5
from M5 import *
import m5ui


COLORS = (0xFF0000, 0x00FF00, 0x0000FF, 0xFFFFFF, 0x000000)
COLOR_NAMES = ("RED", "GREEN", "BLUE", "WHITE", "BLACK")
CORNER_COLORS = (0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00)

page = None
labels = []
label_color = None
label_touch = None
label_last_touch = None
color_index = 0
touch_count = 0


def foreground(background):
    return 0x000000 if background in (0xFFFFFF, 0x00FF00, 0xFFFF00) else 0xFFFFFF


def make_corner(x, y, color, name, text_color):
    corner = lv.obj(page)
    corner.remove_style_all()
    corner.set_pos(x, y)
    corner.set_size(64, 64)
    corner.set_style_bg_color(lv.color_hex(color), lv.PART.MAIN)
    corner.set_style_bg_opa(255, lv.PART.MAIN)
    corner.remove_flag(lv.obj.FLAG.SCROLLABLE)
    corner.remove_flag(lv.obj.FLAG.CLICKABLE)
    label = m5ui.M5Label(name, 0, 0, text_color, color, 0, lv.font_montserrat_18, corner)
    label.center()
    label.remove_flag(lv.obj.FLAG.CLICKABLE)


def update_screen():
    background = COLORS[color_index]
    text_color = foreground(background)
    page.set_bg_color(background, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
    label_color.set_text("%s" % COLOR_NAMES[color_index])
    label_touch.set_text("Taps: %d" % touch_count)
    for label in labels:
        label.set_text_color(text_color, 255, lv.PART.MAIN | lv.STATE.DEFAULT)


def page_touch_event(event_struct):
    global color_index, touch_count

    if event_struct.code == lv.EVENT.PRESSED:
        x = Touch.getX()
        y = Touch.getY()
        touch_count += 1
        label_last_touch.set_text("%d, %d" % (x, y))
        color_index = (color_index + 1) % len(COLORS)
        update_screen()


def setup():
    global page, labels, label_color, label_touch, label_last_touch

    M5.begin()
    m5ui.init()
    page = m5ui.M5Page(bg_c=COLORS[color_index])
    page.set_style_pad_all(0, lv.PART.MAIN)
    page.set_style_border_width(0, lv.PART.MAIN)
    page.remove_flag(lv.obj.FLAG.SCROLLABLE)
    page.add_flag(lv.obj.FLAG.CLICKABLE)
    make_corner(0, 0, CORNER_COLORS[0], "TL", 0x000000)
    make_corner(416, 0, CORNER_COLORS[1], "TR", 0x000000)
    make_corner(0, 416, CORNER_COLORS[2], "BL", 0xFFFFFF)
    make_corner(416, 416, CORNER_COLORS[3], "BR", 0x000000)
    text_color = foreground(COLORS[color_index])
    labels = []
    for text, y, font in (
        ("TOP", 24, lv.font_montserrat_18),
        ("Display + Touch", 104, lv.font_montserrat_24),
        ("RED", 170, lv.font_montserrat_48),
        ("Taps: 0", 256, lv.font_montserrat_24),
        ("--, --", 300, lv.font_montserrat_24),
        ("Tap to change color", 370, lv.font_montserrat_18),
    ):
        label = m5ui.M5Label(text, 72, y, text_color, COLORS[color_index], 0, font, page)
        label.set_width(336)
        label.set_style_text_align(lv.TEXT_ALIGN.CENTER, lv.PART.MAIN)
        label.remove_flag(lv.obj.FLAG.CLICKABLE)
        labels.append(label)
    label_color, label_touch, label_last_touch = labels[2:5]
    page.add_event_cb(page_touch_event, lv.EVENT.ALL, None)
    page.screen_load()


def loop():
    M5.update()
    time.sleep_ms(10)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt):
        m5ui.deinit()
        raise
