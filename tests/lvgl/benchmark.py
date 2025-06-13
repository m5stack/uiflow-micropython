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
disp_drv.set_rotation(lv.DISPLAY_ROTATION._270)

# touch driver init
indev_drv = lv.indev_create()
indev_drv.set_type(lv.INDEV_TYPE.POINTER)
# indev_drv.set_display(lv.display_get_default())
indev_drv.set_display(disp_drv)
indev_drv.set_read_cb(M5.Lcd.lvgl_read)

M5.Lcd.lv_demo_benchmark()
