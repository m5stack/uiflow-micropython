# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv


class M5Switch(lv.switch):
    """Create a switch object.

    :param int x: The x position of the switch.
    :param int y: The y position of the switch.
    :param int w: The width of the switch.
    :param int h: The height of the switch.
    :param int bg_c: The color of the switch in the off state in hexadecimal format.
    :param int bg_c_checked: The color of the switch in the on state in hexadecimal format.
    :param int circle_c: This color refers to the color of the circle on the switch in hexadecimal format.
    :param lv.obj parent: The parent object to attach the switch to. If not specified, the switch will be attached to the default screen.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Switch
            import lvgl as lv

            m5ui.init()
            switch_0 = M5Switch(x=120, y=80, w=60, h=30, bg_c=0xE7E3E7, color=0x2196F3, parent=page0)
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=0,
        h=0,
        bg_c=0xE7E3E7,
        bg_c_checked=0x0288FB,
        circle_c=0xFFFFFF,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_bg_color(bg_c, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_bg_color(bg_c_checked, 255, lv.PART.INDICATOR | lv.STATE.CHECKED)
        self.set_bg_color(circle_c, 255, lv.PART.KNOB | lv.STATE.DEFAULT)
        self.set_size(w, h)

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
