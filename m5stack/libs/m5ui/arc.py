# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from m5ui.base import M5Base
import lvgl as lv


class M5Arc(lv.arc):
    """Create a arc object.

    :param int x: The x position of the arc.
    :param int y: The y position of the arc.
    :param int w: The width of the arc.
    :param int h: The height of the arc.
    :param int value: The initial value of the arc.
    :param int min_value: The minimum value of the arc.
    :param int max_value: The maximum value of the arc.
    :param int rotation: The rotation of the arc in degrees.
    :param int bg_c: The color of the arc in the off state in hexadecimal format.
    :param int bg_c_indicator: The color of the arc in the on state in hexadecimal format.
    :param int bg_c_knob: The color of the knob on the arc in hexadecimal format.
    :param lv.obj parent: The parent object to attach the arc to. If not specified, the arc will be attached to the default screen.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Arc
            import lvgl as lv

            m5ui.init()
            arc_0 = M5Arc(
                x=0,
                y=0,
                w=100,
                h=100,
                value=10,
                min_value=0,
                max_value=100,
                rotation=0,
                mode=lv.arc.MODE.REVERSE,
                bg_c=0xE7E3E7,
                bg_c_indicator=0x0288FB,
                bg_c_knob=0xE7E3E7,
                parent=page0,
            )
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=0,
        h=0,
        value=0,
        min_value=0,
        max_value=100,
        rotation=0,
        mode=lv.arc.MODE.NORMAL,
        bg_c=0xE7E3E7,
        bg_c_indicator=0x0288FB,
        bg_c_knob=0xE7E3E7,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_size(w, h)
        self.set_value(value)
        self.set_range(min_value, max_value)
        self.set_rotation(rotation)
        self.set_mode(mode)
        self.set_arc_color(bg_c, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_arc_color(bg_c_indicator, 255, lv.PART.INDICATOR | lv.STATE.DEFAULT)
        self.set_arc_color(bg_c_knob, 255, lv.PART.KNOB | lv.STATE.DEFAULT)

    def set_arc_color(self, color, opa: int, part: int):
        """Set the color of the arc.

        :param int color: The color of the arc in hexadecimal format.
        :param int opa: The opacity level (0-255).
        :param int part: The part of the arc to apply the style to (e.g., lv.PART.MAIN | lv.STATE.DEFAULT).

        UiFlow2 Code Block:

            |set_arc_color.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_arc_color(0x2196F3, lv.PART.MAIN | lv.STATE.DEFAULT)
        """
        if isinstance(color, int):
            color = lv.color_hex(color)
        if part == lv.PART.KNOB | lv.STATE.DEFAULT:
            self.set_bg_color(color, opa, lv.PART.KNOB | lv.STATE.DEFAULT)
        else:
            self.set_style_arc_color(color, part)
            self.set_style_arc_opa(opa, part)

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
