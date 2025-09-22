# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv


class M5LED(lv.led):
    """Create a LED object.

    :param int x: The x position of the LED.
    :param int y: The y position of the LED.
    :param int size: The size (width and height) of the LED.
    :param int color: The color of the LED in RGB888 format.
    :param bool on: Initial state of the LED (True for ON, False for OFF).
    :param lv.obj parent: The parent object to attach the LED to. If not specified, the LED will be attached to the default screen.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Led
            import lvgl as lv

            m5ui.init()
            led_0 = M5Led(x=50, y=50, size=50, color=0x00FF00, on=True, parent=page0)
    """

    def __init__(self, x=0, y=0, size=50, color=0x00FF00, on=True, parent=None):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_size(size, size)
        self.set_color(color)
        if on:
            self.on()
        else:
            self.off()

    def set_color(self, color: int):
        super().set_color(lv.color_hex(color))

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
