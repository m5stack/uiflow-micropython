# -*- encoding: utf-8 -*-
# User display example
from M5 import UserDisplay, Widgets

user_lcd = UserDisplay(
    # LCD type
    panel_type=UserDisplay.PANEL.GC9A01,
    # resolution
    width=240,
    height=240,
    offset_x=0,
    offset_y=0,
    # color order
    invert=True,
    rgb_order=False,
    # SPI bus
    spi_host=2,
    spi_freq=40,
    pin_sclk=6,
    pin_mosi=5,
    pin_miso=-1,
    pin_dc=4,
    pin_cs=7,
    pin_rst=8,
    pin_busy=-1,
    # backlight
    pin_bl=9,
    bl_invert=False,
    bl_pwm_freq=44100,
    bl_pwm_chn=7,
)

Widgets.fillScreen(0xFF, parent=user_lcd)

label0 = Widgets.Label(
    "Hello World", 50, 57, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18, parent=user_lcd
)

label0.setCursor(60, 100)
