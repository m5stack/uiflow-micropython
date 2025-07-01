# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import lvgl as lv
import sys
import lv_utils


def _sdl_init(width=320, height=240):
    lv.init()

    # Create an event loop and Register SDL display/mouse/keyboard drivers.
    from lv_utils import event_loop

    event_loop = event_loop()

    disp_drv = lv.sdl_window_create(width, height)
    disp_drv.set_default()
    display = lv.display_get_default()

    group = lv.group_create()
    group.set_default()

    mouse = lv.sdl_mouse_create()
    mouse.set_display(display)
    mouse.set_group(group)

    keyboard = lv.sdl_keyboard_create()
    keyboard.set_display(display)
    keyboard.set_group(group)
    print("SDL initialized with display size:", width, "x", height)


def _m5_init():
    import M5

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
    lv_utils.fs_register(fs_drv, "S", 500)


def init():
    if sys.platform == "esp32":
        _m5_init()
    elif sys.platform in ["linux", "darwin"]:
        _sdl_init()


def deinit():
    if sys.platform == "esp32":
        import M5

        M5.Lcd.lvgl_deinit()
    else:
        pass
