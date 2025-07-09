# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv


class M5TextArea(lv.textarea):
    """Create a text area widget.

    :param str text: Initial text content of the text area.
    :param str placeholder: Placeholder text when the text area is empty.
    :param int x: X position of the text area.
    :param int y: Y position of the text area.
    :param int w: Width of the text area.
    :param int h: Height of the text area.
    :param lv.font_t font: Font used for the text.
    :param int bg_c: Background color of the text area.
    :param int border_c: Border color of the text area.
    :param int text_c: Text color of the text area.
    :param lv.obj parent: Parent object of the text area. If not specified, it will be set to the active screen.
    """

    def __init__(
        self,
        text="",
        placeholder="",
        x=0,
        y=0,
        w=200,
        h=100,
        font=lv.font_montserrat_14,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)

        self.set_size(w, h)
        self.set_pos(x, y)
        self.set_text(text)
        self.set_placeholder_text(placeholder)
        self.set_style_text_font(font, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_bg_color(bg_c, lv.OPA.COVER, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_border_color(border_c, lv.OPA.COVER, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_text_color(text_c, lv.OPA.COVER, lv.PART.MAIN | lv.STATE.DEFAULT)

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
