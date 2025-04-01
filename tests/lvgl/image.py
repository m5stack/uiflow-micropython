# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import sys
import M5
import lvgl as lv
import fs_driver

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

# fs driver init
fs_drv = lv.fs_drv_t()
fs_driver.fs_register(fs_drv, "S")


scr = lv.obj()
img0 = lv.image(scr)
img0.set_src("S:/flash/res/img/uiflow.jpg")
img0.set_pos(0, 0)

img1 = lv.image(scr)
img1.set_src("S:/flash/res/img/uiflow.png")
img1.set_pos(0, 80)

img2 = lv.image(scr)
img2.set_src("S:/flash/res/img/uiflow.bmp")
img2.set_pos(0, 160)

lv.screen_load(scr)
