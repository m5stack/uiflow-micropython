# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv


class M5Slider(lv.slider):

    """Create a slider widget.

    :param x: The x position of the slider.
    :param y: The y position of the slider.
    :param w: The width of the slider.
    :param h: The height of the slider.
    :param mode: only `lv.slider.MODE.NORMAL` is supported.
    :param min_value: The minimum value of the slider.
    :param max_value: The maximum value of the slider.
    :param value: The initial value of the slider.
    :param bg_c: The background color of the slider.
    :param color: The color of the slider indicator.
    :param parent: The parent object of the slider. If not specified, it will be set to the active screen.
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=100,
        h=20,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=25,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)

        self.set_size(w, h)
        self.set_pos(x, y)
        self.set_mode(mode)
        self.set_range(min_value, max_value)
        self.set_value(value, False)
        self.set_bg_color(bg_c, 51, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_bg_color(color, lv.OPA.COVER, lv.PART.INDICATOR | lv.STATE.DEFAULT)

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
