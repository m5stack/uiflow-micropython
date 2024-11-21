# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import PuzzleUnit
import time


title0 = None
label0 = None
label1 = None
puzzle_0 = None


def setup():
    global title0, label0, label1, puzzle_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "UnitPuzzle M5Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "Pls see the Puzzle", 76, 102, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "Program will run automatically", 10, 134, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    puzzle_0 = PuzzleUnit((33, 32), 1)
    puzzle_0.set_brightness(10)


def loop():
    global title0, label0, label1, puzzle_0
    M5.update()
    puzzle_0.set_color(1, 1, 0xFFFFFF)
    puzzle_0.set_color(1, 64, 0x66FFFF)
    time.sleep(1)
    puzzle_0.fill_color(0x6600CC)
    time.sleep(1)
    puzzle_0.set_color_from(1, 1, 64, 0x6600CC, 0)
    puzzle_0.set_color_from(1, 64, 1, 0x33FF33, 30)
    time.sleep(1)
    puzzle_0.set_color_running_from(1, 1, 64, 0x6600CC, 30)
    puzzle_0.set_color_running_from(1, 64, 1, 0x33FF33, 30)
    time.sleep(1)
    puzzle_0.set_color_saturation_from(1, 1, 64, 0x6600CC, 30)
    puzzle_0.set_color_saturation_from(1, 64, 1, 0x33FF33, 30)
    time.sleep(1)
    puzzle_0.set_random_color_random_led_from(1, 1, 64)
    time.sleep(1)
    puzzle_0.set_screen(
        1,
        [
            0xFFFFFF,
            0xFFFFFF,
            0,
            0,
            0,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0,
            0,
            0,
            0,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0,
            0,
            0,
            0,
            0,
            0xFFFFFF,
            0xFFFFFF,
            0,
            0,
            0,
            0,
            0,
            0,
            0xFFFFFF,
        ],
    )
    time.sleep(1)


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
