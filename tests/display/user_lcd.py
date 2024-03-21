# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
# User display example
from M5 import UserDisplay, Widgets

user_lcd = UserDisplay(
    # LCD type
    panel=UserDisplay.PANEL.GC9A01,
    # resolution
    w=240,
    h=240,
    ox=0,
    oy=0,
    # color order
    invert=True,
    rgb=False,
    # SPI bus
    spi_host=2,
    spi_freq=40,
    sclk=6,
    mosi=5,
    miso=-1,
    dc=4,
    cs=7,
    rst=8,
    busy=-1,
    # backlight
    bl=9,
    bl_invert=False,
    bl_pwm_freq=44100,
    bl_pwm_chn=7,
)

Widgets.fillScreen(0xFF, parent=user_lcd)

label0 = Widgets.Label(
    "Hello World", 50, 57, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18, parent=user_lcd
)

label0.setCursor(60, 100)
