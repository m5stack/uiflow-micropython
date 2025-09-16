# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv
import warnings


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

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Slider
            import lvgl as lv

            slider_0 = M5Slider(x=50, y=50, w=200, h=20, min_value=0, max_value=100, value=25)
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
        super().set_range(min_value, max_value)
        super().set_value(value, False)
        self.set_bg_color(bg_c, 51, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_bg_color(color, lv.OPA.COVER, lv.PART.INDICATOR | lv.STATE.DEFAULT)

    def set_value(self, value: int, anim: bool = False) -> None:
        """Set the value of the slider.

        :param int value: The value to set.
        :param bool anim: Whether to animate the change.
        :return: None

        UiFlow2 Code Block:

            |set_value.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.set_value(50, True)
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
        """Set the range of the slider.

        :param int min_value: The minimum value of the range.
        :param int max_value: The maximum value of the range.
        :return: None

        UiFlow2 Code Block:

            |set_range.png|

        MicroPython Code Block:

            .. code-block:: python

                slider_0.set_range(0, 200)
        """
        if not isinstance(min_value, int) or not isinstance(max_value, int):
            raise ValueError("min_value and max_value must be integers.")
        super().set_range(min_value, max_value)
        self.set_value(self.get_value(), False)

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
