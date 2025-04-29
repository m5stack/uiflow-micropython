# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import sys
import M5
import lvgl as lv
import lv_utils

M5.begin()

# lvgl init
M5.Lcd.lvgl_init()

# built-in display
disp_buf0 = lv.draw_buf_create(M5.getDisplay(0).width(), 10, lv.COLOR_FORMAT.RGB565, 0)
disp_buf1 = lv.draw_buf_create(M5.getDisplay(0).width(), 10, lv.COLOR_FORMAT.RGB565, 0)

disp_drv = lv.display_create(M5.getDisplay(0).width(), M5.getDisplay(0).height())
disp_drv.set_color_format(lv.COLOR_FORMAT.RGB565)

disp_drv.set_draw_buffers(disp_buf0, disp_buf1)
disp_drv.set_flush_cb(M5.Lcd.lvgl_flush)
disp_drv.set_user_data({"display": M5.Lcd})
disp_drv.set_render_mode(lv.DISPLAY_RENDER_MODE.PARTIAL)

# touch driver init
indev_drv = lv.indev_create()
indev_drv.set_type(lv.INDEV_TYPE.POINTER)
# indev_drv.set_display(lv.display_get_default())
indev_drv.set_display(disp_drv)
indev_drv.set_read_cb(M5.Lcd.lvgl_read)

# sd card driver init
from hardware import sdcard

sdcard.SDCard(slot=2, width=1, sck=18, miso=38, mosi=23, cs=4, freq=20000000)

# fs driver init
fs_drv = lv.fs_drv_t()
lv_utils.fs_register(fs_drv, "S", 500)

scr = lv.screen_active()
scr.clean()

myfont_cn = lv.binfont_create("S:/sd/font-PHT-cn-20.bin")

label1 = lv.label(scr)
label1.set_style_text_font(myfont_cn, 0)  # set the font
label1.set_text("上中下乎")
label1.align(lv.ALIGN.CENTER, 0, -25)

myfont_en = lv.binfont_create("S:/sd/font-PHT-en-20.bin")

label2 = lv.label(scr)
label2.set_style_text_font(myfont_en, 0)  # set the font
label2.set_text("Hello LVGL!")
label2.align(lv.ALIGN.CENTER, 0, 25)


myfont_jp = lv.binfont_create("S:/sd/font-PHT-jp-20.bin")

label3 = lv.label(scr)
label3.set_style_text_font(myfont_jp, 0)  # set the font
label3.set_text("こんにちはありがとう")
label3.align(lv.ALIGN.CENTER, 0, 0)

img0 = lv.image(scr)
img0.set_src("S:/flash/res/img/uiflow.jpg")
img0.set_pos(0, 0)

img1 = lv.image(scr)
img1.set_src("S:/flash/res/img/uiflow.png")
img1.set_pos(0, 80)
