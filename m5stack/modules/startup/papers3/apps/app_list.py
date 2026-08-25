# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .. import app_base
from .. import layout
import widgets
import M5
import os
import sys


class TextButton(widgets.Button):
    def __init__(
        self,
        text: str,
        x: int,
        y: int,
        w: int = 0,
        h: int = 0,
        size: float = 1.0,
        font_align: int = widgets.Label.LEFT_ALIGNED,
        fg_color: int = 0xFFFFFF,
        bg_color: int = 0x000000,
        font=M5.Lcd.FONTS.Montserrat14,
        parent=M5.Lcd,
        _id=0,
    ) -> None:
        super().__init__(parent)
        self._label = widgets.Label(
            text, x, y, w, h, size, font_align, fg_color, bg_color, font, parent
        )
        self.set_pos(x, y)
        self.set_size(w, h)
        self.id = _id

    def handle(self, x, y):
        if self._is_select(x, y) and self._event_handler:
            self._event_handler(self)
            return True
        return False

    def set_pos(self, x, y):
        self._x = x
        self._y = y
        self._label.set_pos(x, y)


class ImageButton(widgets.Button):
    def __init__(
        self,
        x: int,
        y: int,
        w: int = 0,
        h: int = 0,
        parent=M5.Lcd,
        _id=0,
    ) -> None:
        super().__init__(parent)
        self._image = widgets.Image(use_sprite=False)
        self._image.set_pos(x, y)
        self._image.set_size(w, h)
        self.set_pos(x, y)
        self.set_size(w, h)
        self.id = _id

    def handle(self, x, y):
        if self._is_select(x, y) and self._event_handler:
            self._event_handler(self)
            return True
        return False

    def set_pos(self, x, y):
        self._x = x
        self._y = y
        self._image.clear(0xFFFFFF)
        self._image.set_pos(x, y)


class Rectangle:
    def __init__(self, x, y, w, h, fg, bg, parent=M5.Lcd) -> None:
        self._x = x
        self._y = y
        self._w = w
        self._h = h
        self._fg = fg
        self._bg = bg
        self._parent = parent
        self.set_pos(self._x, self._y)

    def set_pos(self, x, y):
        self._parent.fillRect(self._x, self._y, self._w, self._h, self._bg)
        self._x = x
        self._y = y
        self._parent.fillRect(self._x, self._y, self._w, self._h, self._fg)


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


class ListApp(app_base.AppBase):
    BACKGROUND = "applist.png"

    def __init__(self, icos: dict, data=None) -> None:
        super().__init__()

    def on_install(self):
        tab_x = 470 if layout.IS_PAPERMONO else 493
        tab_w = 100 if layout.IS_PAPERMONO else 48
        self.descriptor = app_base.Descriptor(
            x=layout.x(tab_x),
            y=layout.y(321),
            w=layout.size(tab_w),
            h=layout.size(181),
        )

    def on_launch(self):
        self._files = FileList("apps")
        self._max_file_num = 9 if len(self._files) > 9 else len(self._files)
        self._file_pos = 0

    def on_view(self):
        layout.draw_background(layout.resource_path(self.BACKGROUND))

        self._run_btn = ImageButton(
            layout.x(400),
            layout.y(435),
            layout.size(46),
            layout.size(46),
            parent=M5.Lcd,
            _id=0,
        )
        self._run_btn._image.set_scale(layout.SCALE_X, layout.SCALE_Y)
        self._run_btn._image.set_src(layout.image_source(layout.resource_path("run.png")))
        self._run_btn.add_event(self._btn_run_event_handler)

        self._rect = Rectangle(
            layout.x(65),
            layout.y(438),
            layout.size(10),
            layout.size(42),
            0,
            0xFFFFFF,
            parent=M5.Lcd,
        )

        self._btns = []
        for i in range(9):
            btn = TextButton(
                text="",
                x=layout.x(80),
                y=layout.y(440 + 48 * i),
                w=layout.size(324),
                h=layout.size(32),
                size=1.0,
                font_align=widgets.Label.LEFT_ALIGNED,
                fg_color=0x000000,
                bg_color=0xFFFFFF,
                font=layout.app_list_font(),
                parent=M5.Lcd,
                _id=i,
            )
            btn.add_event(self._btn_files_event_handler)
            self._btns.append(btn)

        for btn, file in zip(self._btns, self._files):
            file and btn and btn._label.set_text(file)

    def on_exit(self):
        del self._btns, self._run_btn, self._rect

    def _btn_files_event_handler(self, btn):
        print("%d pressed" % btn.id)
        if len(btn._label._text) == 0:
            return
        self._file_pos = btn.id
        self._rect.set_pos(layout.x(65), layout.y(438 + 48 * btn.id))
        self._run_btn.set_pos(layout.x(400), layout.y(435 + 48 * btn.id))

    def _btn_run_event_handler(self, btn):
        if self._max_file_num == 0:
            return
        print("run %d, %s" % (self._file_pos, self._files[self._file_pos]))
        execfile("/".join(["apps/", self._files[self._file_pos]]), {"__name__": "__main__"})  # noqa: F821
        raise KeyboardInterrupt

    async def _click_event_handler(self, x, y, fw):
        # print("_click_event_handler")
        for button in self._btns:
            button.handle(x, y)
        self._run_btn.handle(x, y)
