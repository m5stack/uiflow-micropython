# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from ..app import AppBase
from ..res import (
    APPLIST_ICO,
    APPRUN_ICO,
    DEVELOP_ICO,
    EZDATA_ICO,
    SETTING_ICO,
    RIGHT_ICO,
    LEFT_ICO,
    MontserratMedium10_VLW,
    MontserratMedium12_VLW,
)
from widgets.image import Image
from widgets.label import Label
import M5
from collections import namedtuple

Icon = namedtuple("Icon", ["name", "src"])


class LauncherApp(AppBase):
    def __init__(self) -> None:
        super().__init__()
        self._icos = (
            Icon("SETTING", SETTING_ICO),
            Icon("DEVELOP", DEVELOP_ICO),
            Icon("APP.RUN", APPRUN_ICO),
            Icon("APP.LIST", APPLIST_ICO),
            Icon("EZDATA", EZDATA_ICO),
        )
        self._id = 1

    def on_view(self):
        M5.Lcd.fillRect(0, 16, 240, 119, 0xEEEEEF)

        left = (len(self._icos) - 1) if self._id - 1 < 0 else self._id - 1
        self._left_img = Image(use_sprite=False)
        self._left_img.set_pos(23, 42)
        self._left_img.set_size(48, 48)
        self._left_img.set_scale(0.75, 0.75)
        self._left_img.set_src(self._icos[left].src)

        self._left_label = Label(
            "SETTING",
            47,
            92,
            w=48 + 4,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font=MontserratMedium10_VLW,
        )
        self._left_label.set_text(self._icos[left].name)

        self._center_img = Image(use_sprite=False)
        self._center_img.set_pos(88, 36)
        self._center_img.set_size(64, 64)
        self._center_img.set_src(self._icos[self._id].src)

        self._center_label = Label(
            "DEVELOP",
            120,
            101,
            w=64,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font=MontserratMedium12_VLW,
        )
        self._center_label.set_text(self._icos[self._id].name)

        right = 0 if self._id + 1 > (len(self._icos) - 1) else self._id + 1
        self._right_img = Image(use_sprite=False)
        self._right_img.set_pos(169, 42)
        self._right_img.set_size(48, 48)
        self._right_img.set_scale(0.75, 0.75)
        self._right_img.set_src(self._icos[right].src)

        self._right_label = Label(
            "APP.RUN",
            193,
            92,
            w=48 + 4,
            font_align=Label.CENTER_ALIGNED,
            fg_color=0x000000,
            bg_color=0xEEEEEF,
            font=MontserratMedium10_VLW,
        )
        self._right_label.set_text(self._icos[right].name)

        M5.Lcd.drawImage(LEFT_ICO, 3, 56)
        M5.Lcd.drawImage(RIGHT_ICO, 227, 56)

    def on_ready(self):
        pass

    def on_hide(self):
        pass

    def on_exit(self):
        pass

    def on_uninstall(self):
        pass

    async def _keycode_enter_event_handler(self, fw):
        app = fw._app_selector.index(self._id + 1)
        app.start()

    async def _keycode_back_event_handler(self, fw):
        pass

    async def _keycode_dpad_down_event_handler(self, fw):
        left = 0
        right = 0
        self._id = self._id + 1 if self._id + 1 < len(self._icos) else 0
        left = (len(self._icos) - 1) if self._id - 1 < 0 else self._id - 1
        right = 0 if self._id + 1 > (len(self._icos) - 1) else self._id + 1
        refresh = True
        if refresh:
            self._left_img.set_src(self._icos[left].src)
            self._left_label.set_text(self._icos[left].name)
            self._center_img.set_src(self._icos[self._id].src)
            self._center_label.set_text(self._icos[self._id].name)
            self._right_img.set_src(self._icos[right].src)
            self._right_label.set_text(self._icos[right].name)

    async def _keycode_dpad_up_event_handler(self, fw):
        left = 0
        right = 0
        refresh = False
        self._id = self._id - 1 if self._id - 1 >= 0 else (len(self._icos) - 1)
        left = (len(self._icos) - 1) if self._id - 1 < 0 else self._id - 1
        right = 0 if self._id + 1 > (len(self._icos) - 1) else self._id + 1
        refresh = True

        if refresh:
            self._left_img.set_src(self._icos[left].src)
            self._left_label.set_text(self._icos[left].name)
            self._center_img.set_src(self._icos[self._id].src)
            self._center_label.set_text(self._icos[self._id].name)
            self._right_img.set_src(self._icos[right].src)
            self._right_label.set_text(self._icos[right].name)

    async def _kb_event_handler(self, event, fw):
        left = 0
        right = 0
        refresh = False
        if event.key == 183:  # right key
            self._id = self._id + 1 if self._id + 1 < len(self._icos) else 0
            left = (len(self._icos) - 1) if self._id - 1 < 0 else self._id - 1
            right = 0 if self._id + 1 > (len(self._icos) - 1) else self._id + 1
            refresh = True

        if event.key == 180:  #  left key
            self._id = self._id - 1 if self._id - 1 >= 0 else (len(self._icos) - 1)
            left = (len(self._icos) - 1) if self._id - 1 < 0 else self._id - 1
            right = 0 if self._id + 1 > (len(self._icos) - 1) else self._id + 1
            refresh = True

        if refresh:
            self._left_img.set_src(self._icos[left].src)
            self._left_label.set_text(self._icos[left].name)
            self._center_img.set_src(self._icos[self._id].src)
            self._center_label.set_text(self._icos[self._id].name)
            self._right_img.set_src(self._icos[right].src)
            self._right_label.set_text(self._icos[right].name)

        if event.key == 0x0D:
            app = fw._app_selector.index(self._id + 1)
            app.start()
