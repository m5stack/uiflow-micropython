# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv


class M5Dropdown(lv.dropdown):
    def __init__(
        self,
        x=0,
        y=0,
        w=100,
        h=lv.SIZE_CONTENT,
        options: list = [],
        direction: int = lv.DIR.RIGHT,
        show_selected: bool = True,
        font: lv.font_t = lv.font_montserrat_14,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_size(w, h)

        if options:
            self.set_options(options)

        self.set_dir(direction)
        self.set_selected_highlight(show_selected)
        self.set_style_text_font(font, lv.PART.MAIN)

    def set_options(self, options: list):
        if isinstance(options, list):
            options = "\n".join(options)
        super().set_options(options)

    def get_selected_str(self) -> str:
        sel = bytearray(32)
        super().get_selected_str(sel, len(sel))
        # 找到第一个空字节的位置，截断字符串
        null_index = sel.find(0)
        if null_index != -1:
            sel = sel[:null_index]
        return sel.decode("utf-8")

    def set_dir(self, direction: int):
        super().set_dir(direction)
        if direction == lv.DIR.LEFT:
            self.set_symbol(lv.SYMBOL.LEFT)
        elif direction == lv.DIR.RIGHT:
            self.set_symbol(lv.SYMBOL.RIGHT)
        elif direction == lv.DIR.UP:
            self.set_symbol(lv.SYMBOL.UP)
        elif direction == lv.DIR.DOWN:
            self.set_symbol(lv.SYMBOL.DOWN)

    def set_style_radius(self, radius: int, part: int) -> None:
        if radius < 0:
            raise ValueError("Radius must be a non-negative integer.")
        super().set_style_radius(radius, part)

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
