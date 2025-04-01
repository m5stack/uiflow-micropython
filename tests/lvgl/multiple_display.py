# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# multipl display example
import sys
import M5
import lvgl as lv
import fs_driver
from hardware import I2C
from hardware import Pin
from unit import LCDUnit
from unit import OLEDUnit

M5.begin()

i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
lcd_0 = LCDUnit(i2c0, 0x3E)
# oled_0 = OLEDUnit(i2c0, 0x3c)

# lvgl init
M5.Lcd.lvgl_init()

# built-in display
disp_buf0 = lv.draw_buf_create(M5.Lcd.width(), 10, lv.COLOR_FORMAT.RGB565, 0)
disp_buf1 = lv.draw_buf_create(M5.Lcd.width(), 10, lv.COLOR_FORMAT.RGB565, 0)

disp_drv = lv.display_create(M5.Lcd.width(), M5.Lcd.height())
disp_drv.set_color_format(lv.COLOR_FORMAT.RGB565)

disp_drv.set_draw_buffers(disp_buf0, disp_buf1)
disp_drv.set_flush_cb(M5.Lcd.lvgl_flush)
disp_drv.set_user_data({"display": M5.Lcd})
disp_drv.set_render_mode(lv.DISPLAY_RENDER_MODE.PARTIAL)

# create a display 1
disp_buf0 = lv.draw_buf_create(lcd_0.width(), 10, lv.COLOR_FORMAT.RGB565, 0)
disp_buf1 = lv.draw_buf_create(lcd_0.width(), 10, lv.COLOR_FORMAT.RGB565, 0)

disp_drv1 = lv.display_create(lcd_0.width(), lcd_0.height())
disp_drv1.set_color_format(lv.COLOR_FORMAT.RGB565)

disp_drv1.set_draw_buffers(disp_buf0, disp_buf1)
disp_drv1.set_flush_cb(M5.Lcd.lvgl_flush)
disp_drv1.set_user_data({"display": lcd_0})
disp_drv1.set_render_mode(lv.DISPLAY_RENDER_MODE.PARTIAL)

# create a display 2
# disp_buf0 = lv.draw_buf_create(oled_0.width(), 10, lv.COLOR_FORMAT.RGB565, 0)
# disp_buf1 = lv.draw_buf_create(oled_0.width(), 10, lv.COLOR_FORMAT.RGB565, 0)

# disp_drv2 = lv.display_create(oled_0.width(), oled_0.height())
# disp_drv2.set_color_format(lv.COLOR_FORMAT.RGB565)

# disp_drv2.set_draw_buffers(disp_buf0, disp_buf1)
# disp_drv2.set_flush_cb(M5.Lcd.lvgl_flush)
# disp_drv2.set_user_data({"display": oled_0})
# disp_drv2.set_render_mode(lv.DISPLAY_RENDER_MODE.PARTIAL)

# touch driver init
indev_drv = lv.indev_create()
indev_drv.set_type(lv.INDEV_TYPE.POINTER)
# indev_drv.set_display(lv.display_get_default())
indev_drv.set_display(disp_drv)
indev_drv.set_read_cb(M5.Lcd.lvgl_read)

# fs driver init
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, "S")

# display 0
disp_drv.set_default()
scr = lv.screen_active()
scr.clean()

img0 = lv.image(scr)
img0.set_src("S:/flash/res/img/uiflow.jpg")
img0.set_pos(0, 0)

# display 1
disp_drv1.set_default()
scr = lv.screen_active()
scr.clean()

img0 = lv.image(scr)
img0.set_src("S:/flash/res/img/uiflow.jpg")
img0.set_pos(0, 0)

# display 2
# disp_drv2.set_default()
# scr = lv.screen_active()
# scr.clean()

# img0 = lv.image(scr)
# img0.set_src("S:/flash/res/img/uiflow.jpg")
# img0.set_pos(0, 0)
