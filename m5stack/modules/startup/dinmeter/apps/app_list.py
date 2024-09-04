# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from ..app import AppBase
from ..res import (
    CARD_228x32_SELECT_IMG,
    CARD_228x32_UNSELECT_IMG,
    MontserratMedium18_VLW,
)
from widgets.image import Image
from widgets.label import Label
import M5
import esp32
import machine
import os
import sys


class Rectangle:
    def __init__(self, x, y, w, h, color, fill_c, parent=M5.Lcd) -> None:
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._color = color
        self._fill_c = fill_c
        self._parent = parent
        self.set_pos(self._x, self._y)

    def set_pos(self, x, y):
        self._x = x
        self._y = y
        self._parent.fillRect(self._x, self._y, self._w, self._h, self._fill_c)
        self._parent.drawRect(self._x, self._y, self._w, self._h, self._color)

    def set_color(self, color, fill_c):
        self._color = color
        self._fill_c = fill_c
        self._parent.fillRect(self._x, self._y, self._w, self._h, self._fill_c)
        self._parent.drawRect(self._x, self._y, self._w, self._h, self._color)


class FileList:
    def __init__(self, dir, suffix=".py") -> None:
        self.files = []
        for file in os.listdir(dir):
            if file.endswith(suffix):
                self.files.append(file)
        self.files_len = len(self.files)
        self.file_pos = 0

    def __contains__(self, item):
        return item in self.files

    def __getitem__(self, item):
        return self.files[item]

    # def __iter__(self):
    #     return iter(self.files)

    # def __next__(self):
    #     if self.file_pos < self.files_len:
    #         val = self.files[self.file_pos]
    #         self.file_pos += 1
    #         return val
    #     else:
    #         raise StopIteration()

    def __len__(self):
        return self.files_len


class ListApp(AppBase):
    # log control
    DEBUG = False

    def __init__(self, icos: dict, data=None) -> None:
        self._wlan = data
        super().__init__()

    def on_install(self):
        pass

    def on_launch(self):
        self._files = FileList("apps")
        self._imgs = []
        self._icos = []
        self._labels = []
        self._max_file_num = 3 if len(self._files) > 3 else len(self._files)
        self._cursor_pos = 0
        self._file_pos = 0

    def on_view(self):
        M5.Lcd.fillRect(0, 16, 240, 119, 0xEEEEEF)

        if self._max_file_num > 0:
            self._img0 = Image(use_sprite=False)
            self._img0.set_pos(6, 22)
            self._img0.set_size(228, 32)
            self._img0.set_src(CARD_228x32_SELECT_IMG)
            self._imgs.append(self._img0)

            self._ico0 = Image(use_sprite=False)
            self._ico0.set_pos(9, 25)
            self._ico0.set_size(26, 26)
            self._icos.append(self._ico0)

            self._label0 = Label(
                "",
                40,
                27,
                w=182,
                h=22,
                fg_color=0x000000,
                bg_color=0xFFFFFF,
                font=MontserratMedium18_VLW,
            )
            self._labels.append(self._label0)

        if self._max_file_num > 1:
            self._img1 = Image(use_sprite=False)
            self._img1.set_pos(6, 60)
            self._img1.set_size(228, 32)
            self._img1.set_src(CARD_228x32_UNSELECT_IMG)
            self._imgs.append(self._img1)

            self._ico1 = Image(use_sprite=False)
            self._ico1.set_pos(9, 63)
            self._ico1.set_size(26, 26)
            self._icos.append(self._ico1)

            self._label1 = Label(
                "",
                40,
                65,
                w=182,
                h=22,
                fg_color=0x000000,
                bg_color=0xFFFFFF,
                font=MontserratMedium18_VLW,
            )
            self._labels.append(self._label1)

        if self._max_file_num > 2:
            self._img2 = Image(use_sprite=False)
            self._img2.set_pos(6, 98)
            self._img2.set_size(228, 32)
            self._img2.set_src(CARD_228x32_UNSELECT_IMG)
            self._imgs.append(self._img2)

            self._ico2 = Image(use_sprite=False)
            self._ico2.set_pos(9, 101)
            self._ico2.set_size(26, 26)
            self._icos.append(self._ico2)

            self._label2 = Label(
                "",
                40,
                103,
                w=182,
                h=22,
                fg_color=0x000000,
                bg_color=0xFFFFFF,
                font=MontserratMedium18_VLW,
            )
            self._labels.append(self._label2)

        for label, icos, file in zip(self._labels, self._icos, self._files):
            ico_name = file[0].lower()
            icos.set_src(f"/system/dinmeter/ico/{ico_name}.jpeg")
            label.set_text(file)

    def on_ready(self):
        pass

    def on_hide(self):
        M5.Lcd.fillRect(32, 26, 206, 103, 0x333333)

    def on_exit(self):
        del (
            self._imgs,
            self._icos,
            self._labels,
            self._files,
        )

    def _btn_up_event_handler(self, event):
        self.DEBUG and print("_btn_up_event_handler")
        if self._file_pos == 0 and self._cursor_pos == 0:
            M5.Speaker.tone(4500, 60)
            return

        # Clear selection cursor
        self._imgs[self._cursor_pos].set_src(CARD_228x32_UNSELECT_IMG)

        # Calculate cursor and file positions
        self._file_pos -= 1
        if self._file_pos < 0:
            self._file_pos = 0

        self._cursor_pos -= 1
        if self._cursor_pos < 0:
            self._cursor_pos = 0

        # cursor img
        self._imgs[self._cursor_pos].set_src(CARD_228x32_SELECT_IMG)

        if self._file_pos < self._cursor_pos:
            for label, icos, file in zip(self._labels, self._icos, self._files):
                ico_name = file[0].lower()
                icos.set_src(f"/system/dinmeter/ico/{ico_name}.jpeg")
                label.set_text(file)
        else:
            for label, icos, file in zip(
                self._labels,
                self._icos,
                self._files[
                    self._file_pos - self._cursor_pos : self._file_pos + (3 - self._cursor_pos)
                ],
            ):
                ico_name = file[0].lower()
                icos.set_src(f"/system/dinmeter/ico/{ico_name}.jpeg")
                label.set_text(file)

    def _btn_down_event_handler(self, fw):
        # Clear selection cursor
        self.DEBUG and print("_btn_down_event_handler")
        self.DEBUG and print("_cursor_pos:", self._cursor_pos)
        self._imgs[self._cursor_pos].set_src(CARD_228x32_UNSELECT_IMG)

        # Calculate cursor and file positions
        self._file_pos += 1
        self._cursor_pos += 1

        max_cursor_pos = len(self._files) - 1 if len(self._files) < 3 else 2
        if self._cursor_pos > max_cursor_pos:
            self._cursor_pos = max_cursor_pos

        # cursor img
        self.DEBUG and print("_cursor_pos:", self._cursor_pos)
        self._imgs[self._cursor_pos].set_src(CARD_228x32_SELECT_IMG)

        if self._file_pos >= len(self._files):
            self._file_pos = len(self._files) - 1
            M5.Speaker.tone(4500, 60)

        # Show File
        if self._file_pos < 3:
            for label, icos, file in zip(self._labels, self._icos, self._files):
                ico_name = file[0].lower()
                icos.set_src(f"/system/dinmeter/ico/{ico_name}.jpeg")
                label.set_text(file)
        else:
            for label, icos, file in zip(
                self._labels, self._icos, self._files[self._file_pos - 2 : self._file_pos + 1]
            ):
                ico_name = file[0].lower()
                icos.set_src(f"/system/dinmeter/ico/{ico_name}.jpeg")
                label.set_text(file)

    def _btn_once_event_handler(self, event):
        execfile("/".join(["apps/", self._files[self._file_pos]]), {"__name__": "__main__"})  # noqa: F821
        sys.exit(0)

    def _btn_always_event_handler(self, event):
        nvs = esp32.NVS("uiflow")
        nvs.set_u8("boot_option", 2)
        nvs.commit()
        with open("apps/" + self._files[self._file_pos], "rb") as f_src, open(
            "main.py", "wb"
        ) as f_dst:
            while True:
                chunk = f_src.read(1024)
                if not chunk:
                    break
                f_dst.write(chunk)
        machine.reset()

    async def _keycode_enter_event_handler(self, fw):
        self._btn_once_event_handler(None)

    async def _keycode_ctrl_event_handler(self, fw):
        self._btn_always_event_handler(None)

    async def _keycode_back_event_handler(self, fw):
        pass

    async def _keycode_dpad_down_event_handler(self, fw):
        self._btn_down_event_handler(None)

    async def _keycode_dpad_up_event_handler(self, fw):
        self._btn_up_event_handler(None)

    async def _kb_event_handler(self, event, fw):
        if event.key == 182:  # down key
            self._btn_down_event_handler(None)
        if event.key == 181:  # up key
            self._btn_up_event_handler(None)

        if event.key == 0x0D:  # Enter key
            self._btn_once_event_handler(event)
        elif event.key in (ord("a"), ord("A")):
            self._btn_always_event_handler(event)
