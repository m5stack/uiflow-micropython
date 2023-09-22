from ..app import AppBase
from widgets.image import Image
from widgets.label import Label
import M5
from M5 import Widgets
import os
import sys
from ..res import (
    APPLIST_UNSELECTED_IMG,
    APPLIST_SELECTED_IMG,
    APPLIST_IMG,
    BAR5_IMG,
    APPLIST_LEFT_IMG,
    APPLIST_RIGHT_IMG,
)


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

    def set_x(self, x):
        self._x = x
        self._parent.fillRect(self._x, self._y, self._w, self._h, self._fill_c)
        self._parent.drawRect(self._x, self._y, self._w, self._h, self._color)

    def get_y(self):
        return self._y

    def set_y(self, y):
        self._y = y
        self._parent.fillRect(self._x, self._y, self._w, self._h, self._fill_c)
        self._parent.drawRect(self._x, self._y, self._w, self._h, self._color)

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

    def __iter__(self):
        return iter(self.files)

    def __next__(self):
        if self.file_pos < self.files_len:
            val = self.files[self.file_pos]
            self.file_pos += 1
            return val
        else:
            raise StopIteration()

    def __len__(self):
        return self.files_len


class ListApp(AppBase):
    def __init__(self, icos: dict, data=None) -> None:
        pass

    def on_install(self):
        M5.Lcd.drawImage(APPLIST_UNSELECTED_IMG, 5 + 62 * 3, 0)

    def on_launch(self):
        self._files = FileList("apps")
        self._max_file_num = 4 if len(self._files) > 4 else len(self._files)
        self._cursor_pos = 0
        self._file_pos = 0

    def on_view(self):
        M5.Lcd.drawImage(APPLIST_SELECTED_IMG, 5 + 62 * 3, 0)

        self._origin_x = 0
        self._origin_y = 56

        self._bg_img = Image(use_sprite=False)
        self._bg_img.set_pos(self._origin_x + 4, self._origin_y + 4)
        self._bg_img.set_size(312, 156)
        self._bg_img.set_src(APPLIST_IMG)

        M5.Lcd.drawImage(BAR5_IMG, 0, 220)

        self._line_spacing = 36 + 2 + 2
        self._left_cursor_x = self._origin_x + 4
        self._left_cursor_y = self._origin_y + 4 + 2

        self._rect0 = Rectangle(
            self._left_cursor_x, self._left_cursor_y, 10, 36, 0xFEFEFE, 0xFEFEFE
        )

        self._left_img = Image(use_sprite=False)
        self._left_img.set_pos(self._left_cursor_x, self._left_cursor_y)
        self._left_img.set_size(10, 36)
        self._left_img.set_src(APPLIST_LEFT_IMG)

        self._right_cursor_x = 320 - 4 - 60 - 10
        self._right_cursor_y = self._origin_y + 4 + 2

        self._rect1 = Rectangle(
            self._right_cursor_x, self._right_cursor_y, 10, 36, 0xFEFEFE, 0xFEFEFE, parent=M5.Lcd
        )

        self._right_img = Image(use_sprite=False)
        self._right_img.set_pos(self._right_cursor_x, self._right_cursor_y)
        self._right_img.set_size(10, 36)
        self._right_img.set_src(APPLIST_RIGHT_IMG)

        self._label0 = Label(
            "",
            self._left_cursor_x + 10,
            self._left_cursor_y + 8,
            w=200,
            h=36,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=Widgets.FONTS.DejaVu18,
        )

        self._label1 = Label(
            "",
            self._left_cursor_x + 10,
            self._left_cursor_y + 8 + self._line_spacing,
            w=200,
            h=36,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=Widgets.FONTS.DejaVu18,
        )

        self._label2 = Label(
            "",
            self._left_cursor_x + 10,
            self._left_cursor_y + 8 + self._line_spacing + self._line_spacing,
            w=200,
            h=36,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=Widgets.FONTS.DejaVu18,
        )

        self._label3 = Label(
            "",
            self._left_cursor_x + 10,
            self._left_cursor_y + 8 + self._line_spacing + self._line_spacing + self._line_spacing,
            w=200,
            h=36,
            fg_color=0x000000,
            bg_color=0xFEFEFE,
            font=Widgets.FONTS.DejaVu18,
        )
        self._labels = []
        self._labels.append(self._label0)
        self._labels.append(self._label1)
        self._labels.append(self._label2)
        self._labels.append(self._label3)

        for label, file in zip(self._labels, self._files):
            file and label and label.setText(file)

    def on_exit(self):
        M5.Lcd.drawImage(APPLIST_UNSELECTED_IMG, 5 + 62 * 3, 0)
        del self._bg_img, self._left_img, self._right_img
        del self._label0, self._label1, self._label2, self._label3, self._labels
        del self._rect0
        del self._files, self._max_file_num, self._cursor_pos, self._file_pos

    async def _btna_event_handler(self, fw):
        pass

    async def _btnb_event_handler(self, fw):
        self._rect0.set_pos(
            self._left_cursor_x, self._left_cursor_y + self._cursor_pos * self._line_spacing
        )
        self._rect1.set_pos(
            self._right_cursor_x, self._right_cursor_y + self._cursor_pos * self._line_spacing
        )
        # M5.Lcd.fillRect(self._left_cursor_x, self._left_cursor_y + self._cursor_pos * self._line_spacing, 10, 36, 0xfefefe)
        # M5.Lcd.fillRect(self._right_cursor_x, self._right_cursor_y + self._cursor_pos * self._line_spacing, 10, 36, 0xfefefe)
        if self._file_pos + 1 == len(self._files):
            self._cursor_pos = 0
        else:
            self._cursor_pos = (self._cursor_pos + 1) % self._max_file_num
        self._file_pos = (self._file_pos + 1) % len(self._files)
        # self._bg_img._draw(False)
        self._left_img.set_pos(
            self._left_cursor_x, self._left_cursor_y + self._cursor_pos * self._line_spacing
        )
        self._right_img.set_pos(
            self._right_cursor_x, self._right_cursor_y + self._cursor_pos * self._line_spacing
        )

        if self._file_pos < 4:
            for label, file in zip(self._labels, self._files):
                file and label and label.setText(file)
        else:
            for label, file in zip(
                self._labels,
                self._files[
                    self._file_pos - self._cursor_pos : self._file_pos + (4 - self._cursor_pos)
                ],
            ):
                file and label and label.setText(file)

    async def _btnc_event_handler(self, fw):
        execfile("apps/" + self._files[self._file_pos])
        sys.exit(0)
