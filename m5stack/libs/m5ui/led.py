# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv
import warnings


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

    def set_brightness(self, brightness: int):
        """Set the brightness of the LED.

        :param int brightness: Brightness level (0-100). Will be mapped to 80-255 internally.

        UiFlow2 Code Block:

            |set_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                led_0.set_brightness(50)  # Set brightness to 50%
        """
        # Clamp input to [0, 100]
        if brightness < 0:
            brightness = 0
            warnings.warn("Brightness below 0, clamped to 0")
        elif brightness > 100:
            brightness = 100
            warnings.warn("Brightness above 100, clamped to 100")

        # Map 0..100 -> 80..255 linearly
        # 0 -> 80, 100 -> 255
        mapped = 80 + (175 * brightness + 50) // 100  # integer rounding
        super().set_brightness(int(mapped))

    def get_brightness(self) -> int:
        """Get the brightness of the LED.

        :return: Brightness level (0-100).
        :rtype: int

        UiFlow2 Code Block:

            |get_brightness.png|

        MicroPython Code Block:

            .. code-block:: python

                brightness = led_0.get_brightness()
        """
        raw_brightness = super().get_brightness()
        # Map 80..255 -> 0..100 linearly with rounding to match set_brightness mapping
        if raw_brightness <= 80:
            return 0
        if raw_brightness >= 255:
            return 100
        # round to nearest: add half of denominator (175//2 == 87)
        mapped = ((raw_brightness - 80) * 100 + 87) // 175
        return int(mapped)

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
