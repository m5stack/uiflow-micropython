# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import startup
import M5
import lvgl as lv
import lv_utils
from .launcher import Launcher, set_hal
from .hal_tab5 import HALTab5
import m5ui


class Tab5_Startup:
    def __init__(self) -> None:
        self._wlan = startup.Startup()

    def startup(self, ssid: str, pswd: str, timeout: int = 60) -> None:
        self._wlan.connect_network(ssid, pswd)

        self._init_lvgl()

        set_hal(HALTab5(self._wlan))

        self.launcher = Launcher()

    def _init_lvgl(self):
        M5.Lcd.setRotation(0)
        M5.Lcd.lvgl_init()

        disp_buf0 = lv.draw_buf_create(
            M5.getDisplay(0).width(), M5.getDisplay(0).height(), lv.COLOR_FORMAT.RGB565, 0
        )
        disp_buf1 = lv.draw_buf_create(
            M5.getDisplay(0).width(), M5.getDisplay(0).height(), lv.COLOR_FORMAT.RGB565, 0
        )

        disp_drv = lv.display_create(M5.getDisplay(0).width(), M5.getDisplay(0).height())
        disp_drv.set_color_format(lv.COLOR_FORMAT.RGB565)

        disp_drv.set_draw_buffers(disp_buf0, disp_buf1)
        disp_drv.set_flush_cb(M5.Lcd.lvgl_flush)
        disp_drv.set_user_data({"display": M5.Lcd})
        disp_drv.set_render_mode(lv.DISPLAY_RENDER_MODE.PARTIAL)
        disp_drv.set_rotation(lv.DISPLAY_ROTATION._90)

        indev_drv = lv.indev_create()
        indev_drv.set_type(lv.INDEV_TYPE.POINTER)
        indev_drv.set_display(disp_drv)
        indev_drv.set_read_cb(M5.Lcd.lvgl_read)

        fs_drv = lv.fs_drv_t()
        lv_utils.fs_register(fs_drv, "S", 500)

        m5ui.event_loop()  # start event loop
