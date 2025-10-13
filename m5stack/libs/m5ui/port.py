# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import lvgl as lv
import sys
import lv_utils
import micropython
import time

_event_loop_instance = None


class event_loop:
    _instance = None
    _initialized = False

    def __new__(cls, freq=33, max_scheduled=2):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, freq=33, max_scheduled=2):
        # 防止重复初始化
        if self._initialized:
            return

        self._initialized = True
        self.delay = 1000 // freq
        import m5utils

        self.timer = m5utils.Timer(
            0, mode=m5utils.Timer.PERIODIC, period=self.delay, callback=self.timer_cb
        )
        self.max_scheduled = max_scheduled
        self.scheduled = 0

    def timer_cb(self, t):
        lv.tick_inc(self.delay)
        if self.scheduled < self.max_scheduled:
            micropython.schedule(self.task_handler, 0)
            self.scheduled += 1

    def task_handler(self, _):
        if lv._nesting.value == 0:
            lv.task_handler()
        self.scheduled -= 1

    def deinit(self):
        if hasattr(self, "timer"):
            self.timer.deinit()
        while self.scheduled > 0:
            time.sleep_ms(20)
        event_loop._initialized = False
        event_loop._instance = None

    @classmethod
    def get_instance(cls):
        """获取单例实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def is_initialized(cls):
        """检查是否已经初始化"""
        return cls._instance is not None and cls._initialized


def _sdl_init(width=320, height=240):
    global _event_loop_instance

    lv.init()

    # Create an event loop and Register SDL display/mouse/keyboard drivers.
    if _event_loop_instance is None:
        from lv_utils import event_loop

        _event_loop_instance = event_loop()

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

    else:
        print("Event loop already running, skip creating new one")


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

    event_loop()


def init():
    if sys.platform == "esp32":
        _m5_init()
    elif sys.platform in ["linux", "darwin"]:
        _sdl_init()


def deinit():
    if sys.platform == "esp32":
        import M5

        event_loop().deinit()
        M5.Lcd.lvgl_deinit()
        lv.mp_lv_deinit_gc()
    else:
        pass
