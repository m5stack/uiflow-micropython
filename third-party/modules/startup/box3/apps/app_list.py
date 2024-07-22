# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from ..app import AppBase, Descriptor
from widgets.image import Image
from widgets.label import Label
from widgets.button import Button
import M5
import os
import sys
import time
import machine
import esp32


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
    def __init__(self, icos: dict, data=None) -> None:
        super().__init__()

    def on_install(self):
        M5.Lcd.drawImage("/system/box3/Selection/appList_unselected.png", 5 + 62 * 3, 20 + 4)
        self.descriptor = Descriptor(x=5 + 62 + 62 + 62, y=20 + 4, w=62, h=56)

    def on_launch(self):
        self._files = FileList("apps")
        self._max_file_num = 4 if len(self._files) > 4 else len(self._files)
        self._cursor_pos = 0
        self._file_pos = 0

    def on_view(self):
        M5.Lcd.drawImage("/system/box3/Selection/appList_selected.png", 5 + 62 * 3, 20 + 4)

        self._bg_img = Image(use_sprite=False)
        self._bg_img.set_pos(4, 20 + 4 + 56 + 4)
        self._bg_img.set_size(312, 156)
        self._bg_img.set_src("/system/box3/List/main.png")

        self._line_spacing = 36 + 2 + 2
        self._left_cursor_x = 4 + 2 + 30
        self._left_cursor_y = (20 + 4 + 56 + 4) + 2

        self._rect0 = Rectangle(
            self._left_cursor_x, self._left_cursor_y, 10, 36, 0xFEFEFE, 0xFEFEFE
        )

        self._left_img = Image(use_sprite=False)
        self._left_img.set_pos(self._left_cursor_x, self._left_cursor_y)
        self._left_img.set_size(10, 36)
        self._left_img.set_src("/system/box3/List/left_cursor.png")

        self._right_cursor_x = 320 - 4 - 60 - 10
        self._right_cursor_y = (20 + 4 + 56 + 4) + 2

        self._rect1 = Rectangle(
            self._right_cursor_x, self._right_cursor_y, 10, 36, 0xFEFEFE, 0xFEFEFE, parent=M5.Lcd
        )

        self._right_img = Image(use_sprite=False)
        self._right_img.set_pos(self._right_cursor_x, self._right_cursor_y)
        self._right_img.set_size(10, 36)
        self._right_img.set_src("/system/box3/List/right_cursor.png")

        self._label0 = Label(
            "",
            self._left_cursor_x + 10,
            self._left_cursor_y + 8,
            w=200,
            h=36,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font="/system/common/font/Montserrat-Medium-18.vlw",
        )

        self._label1 = Label(
            "",
            self._left_cursor_x + 10,
            self._left_cursor_y + 8 + self._line_spacing,
            w=200,
            h=36,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font="/system/common/font/Montserrat-Medium-18.vlw",
        )

        self._label2 = Label(
            "",
            self._left_cursor_x + 10,
            self._left_cursor_y + 8 + self._line_spacing + self._line_spacing,
            w=200,
            h=36,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font="/system/common/font/Montserrat-Medium-18.vlw",
        )

        self._label3 = Label(
            "",
            self._left_cursor_x + 10,
            self._left_cursor_y + 8 + self._line_spacing + self._line_spacing + self._line_spacing,
            w=200,
            h=36,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font="/system/common/font/Montserrat-Medium-18.vlw",
        )
        self._labels = []
        self._labels.append(self._label0)
        self._labels.append(self._label1)
        self._labels.append(self._label2)
        self._labels.append(self._label3)

        for label, file in zip(self._labels, self._files):
            file and label and label.set_text(file)

        self._btn_up = Button(None)
        self._btn_up.set_pos(4 + 2, (20 + 4 + 56 + 4) + 2)
        self._btn_up.set_size(60, 75)
        self._btn_up.add_event(self._btn_up_event_handler)

        self._btn_down = Button(None)
        self._btn_down.set_pos(4 + 2, (20 + 4 + 56 + 4) + 2 + 75 + 2)
        self._btn_down.set_size(60, 75)
        self._btn_down.add_event(self._btn_down_event_handler)

        self._btn_once = Button(None)
        self._btn_once.set_pos(4 + (312 - 100), (20 + 4 + 56 + 4) + 30)
        self._btn_once.set_size(100, 63)
        self._btn_once.add_event(self._btn_once_event_handler)

        self._btn_always = Button(None)
        self._btn_always.set_pos(4 + (312 - 100), (20 + 4 + 56 + 4) + 30 + 63)
        self._btn_always.set_size(100, 63)
        self._btn_always.add_event(self._btn_always_event_handler)

        self._buttons = (self._btn_up, self._btn_down, self._btn_once, self._btn_always)

    def on_exit(self):
        M5.Lcd.drawImage("/system/box3/Selection/appList_unselected.png", 5 + 62 * 3, 20 + 4)
        del self._bg_img, self._left_img, self._right_img
        del self._label0, self._label1, self._label2, self._label3, self._labels
        del self._files

    async def _click_event_handler(self, x, y, fw):
        # print("_click_event_handler")
        for button in self._buttons:
            button.handle(x, y)

    def _btn_up_event_handler(self, event):
        # print("_btn_up_event_handler")
        if self._file_pos == 0 and self._cursor_pos == 0:
            return

        # Clear selection cursor
        self._rect0.set_pos(
            self._left_cursor_x, self._left_cursor_y + self._cursor_pos * self._line_spacing
        )
        self._rect1.set_pos(
            self._right_cursor_x, self._right_cursor_y + self._cursor_pos * self._line_spacing
        )

        # Calculate cursor and file positions
        self._file_pos -= 1
        if self._file_pos < 0:
            self._file_pos = 0

        self._cursor_pos -= 1
        if self._cursor_pos < 0:
            self._cursor_pos = 0

        if self._file_pos < self._cursor_pos:
            for label, file in zip(self._labels, self._files):
                label.set_text(file)
        else:
            for label, file in zip(
                self._labels,
                self._files[
                    self._file_pos - self._cursor_pos : self._file_pos + (4 - self._cursor_pos)
                ],
            ):
                label.set_text(file)

        self._left_img.set_pos(
            self._left_cursor_x, self._left_cursor_y + self._line_spacing * self._cursor_pos
        )
        self._right_img.set_pos(
            self._right_cursor_x, self._right_cursor_y + self._line_spacing * self._cursor_pos
        )

    def _btn_down_event_handler(self, fw):
        # Clear selection cursor
        self._rect0.set_pos(
            self._left_cursor_x, self._left_cursor_y + self._cursor_pos * self._line_spacing
        )
        self._rect1.set_pos(
            self._right_cursor_x, self._right_cursor_y + self._cursor_pos * self._line_spacing
        )

        # Calculate cursor and file positions
        self._file_pos += 1
        self._cursor_pos += 1

        max_cursor_pos = len(self._files) - 1 if len(self._files) < 4 else 3
        if self._cursor_pos > max_cursor_pos:
            self._cursor_pos = max_cursor_pos

        # cursor img
        self._left_img.set_pos(
            self._left_cursor_x, self._left_cursor_y + self._cursor_pos * self._line_spacing
        )
        self._right_img.set_pos(
            self._right_cursor_x, self._right_cursor_y + self._cursor_pos * self._line_spacing
        )

        if self._file_pos >= len(self._files):
            self._file_pos = len(self._files) - 1
            return

        # Show File
        if self._file_pos < 4:
            for label, file in zip(self._labels, self._files):
                if file is None or label is None:
                    break
                label.set_text(file)
        else:
            for label, file in zip(
                self._labels, self._files[self._file_pos - 3 : self._file_pos + 1]
            ):
                if file is None or label is None:
                    break
                label.set_text(file)

    def _btn_once_event_handler(self, event):
        execfile("apps/" + self._files[self._file_pos])  # noqa: F821
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
        time.sleep(0.1)
        machine.reset()
