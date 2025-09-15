# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv
import warnings


class M5Bar(lv.bar):
    """Initialize a new M5Bar widget.

    :param int x: The x-coordinate of the bar.
    :param int y: The y-coordinate of the bar.
    :param int w: The width of the bar.
    :param int h: The height of the bar.
    :param int min_value: The minimum value of the bar range.
    :param int max_value: The maximum value of the bar range.
    :param int value: The initial value of the bar.
    :param bool is_show_value: Whether to display the current value as text.
    :param int bg_c: The background color of the bar.
    :param int color: The indicator color of the bar.
    :param lv.obj parent: The parent object. If None, uses the active screen.
    :return: None

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            bar = M5Bar(x=50, y=50, w=200, h=30, min_value=0, max_value=100, value=50)
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=100,
        h=20,
        min_value=0,
        max_value=100,
        value=25,
        is_show_value=False,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)

        self.set_pos(x, y)
        self.set_size(w, h)
        super().set_range(min_value, max_value)
        self.set_bg_color(
            bg_c, 51, lv.PART.MAIN | lv.STATE.DEFAULT
        )  # default opacity is 51 (20% opacity)
        self.set_bg_color(color, lv.OPA.COVER, lv.PART.INDICATOR | lv.STATE.DEFAULT)
        super().set_value(value, True)

        if is_show_value:
            self.add_event_cb(self._draw_cb, lv.EVENT.DRAW_MAIN_END, None)

    def set_value(self, value: int, anim: bool = False) -> None:
        """Set the current value of the bar.

        :param int value: The value to set.
        :param bool anim_enable: Whether to enable animation when changing the value.
        :return: None

        UiFlow2 Code Block:

            |set_value.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.set_value(75, True)
        """
        if not isinstance(value, int):
            raise ValueError("Value must be an integer.")
        if value < self.get_min_value():
            warnings.warn(f"Value is less than min_value, setting to {self.get_min_value()}.")
            value = self.get_min_value()
        if value > self.get_max_value():
            warnings.warn(f"Value is greater than max_value, setting to {self.get_max_value()}.")
            value = self.get_max_value()
        super().set_value(value, anim)

    def set_range(self, min_value: int, max_value: int) -> None:
        """Set the value range of the bar.

        :param int min_value: The minimum value.
        :param int max_value: The maximum value.
        :return: None

        UiFlow2 Code Block:

            |set_range.png|

        MicroPython Code Block:

            .. code-block:: python

                bar.set_range(0, 200)
        """
        if not isinstance(min_value, int) or not isinstance(max_value, int):
            raise ValueError("min_value and max_value must be integers.")
        super().set_range(min_value, max_value)
        self.set_value(self.get_value(), False)

    def _draw_cb(self, event_struct):
        label_dsc = lv.draw_label_dsc_t()
        label_dsc.init()
        label_dsc.font = lv.font_get_default()

        txt_size = lv.point_t()
        lv.text_get_size(
            txt_size,
            f"{self.get_value()}",
            label_dsc.font,
            label_dsc.letter_space,
            label_dsc.line_space,
            lv.COORD.MAX,
            label_dsc.flag,
        )

        txt_area = lv.area_t()
        txt_area.x1 = 0
        txt_area.x2 = txt_size.x - 1
        txt_area.y1 = 0
        txt_area.y2 = txt_size.y - 1

        indic_area = lv.area_t()
        self.get_coords(indic_area)
        indic_area.set_width(indic_area.get_width() * self.get_value() // self.get_max_value())

        if indic_area.get_width() > (txt_size.x + 20):
            print("Indicator area is large enough to display text")
            indic_area.align(txt_area, lv.ALIGN.RIGHT_MID, -10, 0)
            label_dsc.color = lv.color_hex(0xFFFFFF)
        else:
            print("Indicator area is too small to display text")
            indic_area.align(txt_area, lv.ALIGN.OUT_RIGHT_MID, 10, 0)
            label_dsc.color = lv.color_hex(0x000000)

        label_dsc.text = f"{self.get_value()}"
        label_dsc.text_local = True
        lv.draw_label(event_struct.get_layer(), label_dsc, txt_area)

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
