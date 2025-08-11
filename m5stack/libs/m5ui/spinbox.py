# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv
import warnings
import time


class M5Spinbox(lv.obj):
    """Create a spinbox widget.

    :param int x: The x position of the spinbox.
    :param int y: The y position of the spinbox.
    :param int w: The width of the spinbox.
    :param int h: The height of the spinbox.
    :param int value: The initial value of the spinbox.
    :param int min_value: The minimum value of the spinbox.
    :param int max_value: The maximum value of the spinbox.
    :param int digit_count: The number of digits to display.
    :param int prec: The number of decimal places.
    :param lv.font_t font: The font to use for the spinbox.
    :param lv.obj parent: The parent object of the spinbox.
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=100,
        h=20,
        value=50,
        min_value=0,
        max_value=100,
        digit_count=5,
        prec=0,
        font=lv.font_montserrat_14,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)

        self.remove_style_all()
        self.set_flex_flow(lv.FLEX_FLOW.ROW)
        self.set_flex_align(lv.FLEX_ALIGN.SPACE_AROUND, lv.FLEX_ALIGN.CENTER, lv.FLEX_ALIGN.CENTER)
        self.set_size(w, h)
        self.set_style_pad_gap(5, 0)
        self.set_pos(x, y)
        self.set_style_text_font(font, lv.PART.MAIN | lv.STATE.DEFAULT)

        self._btn_dec = lv.button(self)
        self._spinbox = lv.spinbox(self)
        self._btn_inc = lv.button(self)

        # left button
        self._btn_dec.set_size(h, h)
        self._btn_dec.set_style_bg_image_src(lv.SYMBOL.MINUS, 0)
        self._btn_dec.add_event_cb(self._decrement_event_cb, lv.EVENT.CLICKED, None)
        self._btn_dec.add_event_cb(self._decrement_event_cb, lv.EVENT.SHORT_CLICKED, None)
        self._btn_dec.add_event_cb(self._decrement_event_cb, lv.EVENT.LONG_PRESSED_REPEAT, None)

        # spinbox
        self._spinbox.set_height(h)
        self._spinbox.set_flex_grow(1)
        self._digit_count = digit_count
        self._sep_pos = digit_count - prec
        self._min_value = min_value
        self._max_value = max_value
        self._check_value(value, min_value, max_value, digit_count, prec)
        self.set_range(min_value, max_value)
        self.set_digit_format(digit_count, self._sep_pos)
        self.set_value(value)

        # right button
        self._btn_inc.set_size(h, h)
        self._btn_inc.set_style_bg_image_src(lv.SYMBOL.PLUS, 0)
        self._btn_inc.add_event_cb(self._increment_event_cb, lv.EVENT.CLICKED, None)
        self._btn_inc.add_event_cb(self._increment_event_cb, lv.EVENT.SHORT_CLICKED, None)
        self._btn_inc.add_event_cb(self._increment_event_cb, lv.EVENT.LONG_PRESSED_REPEAT, None)

    def _check_value(self, value, min_value, max_value, digit_count, prec):
        if value < min_value or value > max_value:
            warnings.warn(f"Value must be between {min_value} and {max_value}.")

        if prec < 0 or prec > digit_count:
            warnings.warn("prec must be between 0 and digit_count.")

        new_max = 10 ** (digit_count - prec) - 1
        new_min = -new_max if min_value < 0 else 0
        if max_value > new_max or min_value < new_min:
            warnings.warn(
                f"max_value must be less than {new_max}, min_value must be greater than {new_min}."
            )

    def add_event_cb(self, event_cb, filters, user_data):
        """Add an event callback to the spinbox.

        :param function handler: The callback function to call.
        :param int event: The event to listen for.
        :param Any user_data: Optional user data to pass to the callback.

        UiFlow2 Code Block:

            |event.png|

        MicroPython Code Block:

            .. code-block:: python

                def spinbox0_value_changed_event(event_struct):
                    global page0, spinbox0
                    print("value changed:", spinbox0.get_value())

                def spinbox0_event_handler(event_struct):
                global page0, spinbox0
                event = event_struct.code
                if event == lv.EVENT.VALUE_CHANGED and True:
                    spinbox0_value_changed_event(event_struct)
                return

                spinbox_0.add_event_cb(spinbox0_event_handler, lv.EVENT.ALL, None)
        """
        self._spinbox.add_event_cb(event_cb, filters, user_data)

    def set_bg_color(self, color: int, opa: int, part: int) -> None:
        """Set the background color and opacity for a given part of the object.

        :param int color: The color to set, can be an integer (hex) or a lv.color object.
        :param int opa: The opacity level (0-255).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_bg_color.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox0.set_bg_color(0xFF0000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        """
        if isinstance(color, int):
            color = lv.color_hex(color)

        self._spinbox.set_style_bg_color(color, part)
        time.sleep(0.01)
        self._spinbox.set_style_bg_opa(opa, part)

    def set_border_color(self, color: int, opa: int, part: int):
        """Set the border color and opacity for a given part of the object.

        :param int color: The color to set, can be an integer (hex) or a lv.color object.
        :param int opa: The opacity level (0-255).
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN).
        :return: None

        UiFlow2 Code Block:

            |set_border_color.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox0.set_border_color(0xFF0000, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        """
        if isinstance(color, int):
            color = lv.color_hex(color)

        self._spinbox.set_style_border_color(color, part)
        time.sleep(0.01)
        self._spinbox.set_style_border_opa(opa, part)

    def set_style_border_width(self, w, part):
        """Set the border width of the spinbox.

        :param int w: The border width in pixels.
        :param int part: The part of the spinbox to apply the border width to, e.g., `lv.PART.MAIN`.
        :return: None

        UiFlow2 Code Block:

            |set_style_border_width.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox0.set_style_border_width(10, lv.PART.MAIN | lv.STATE.DEFAULT)
        """
        self._spinbox.set_style_border_width(w, part)

    def set_style_radius(self, radius: int, part: int) -> None:
        """Set the radius of the spinbox's corners.

        :param radius: The radius of the corners in pixels.
        :param part: The part of the spinbox to apply the radius to, e.g., `lv.PART.MAIN`.

        UiFlow2 Code Block:

            |set_style_radius.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
        """
        if radius < 0:
            warnings.warn("Radius must be a non-negative integer.")
            return
        self._spinbox.set_style_radius(radius, part)

    def _increment_event_cb(self, event_struct):
        event = event_struct.code
        if event in (lv.EVENT.CLICKED, lv.EVENT.SHORT_CLICKED, lv.EVENT.LONG_PRESSED_REPEAT):
            self._spinbox.increment()

    def _decrement_event_cb(self, event_struct):
        event = event_struct.code
        if event in (lv.EVENT.CLICKED, lv.EVENT.SHORT_CLICKED, lv.EVENT.LONG_PRESSED_REPEAT):
            self._spinbox.decrement()

    def set_digit_format(self, digit_count: int, sep_pos: int) -> None:
        """Set the digit format of the spinbox.

        :param digit_count: The total number of digits in the float representation.
        :type digit_count: int
        :param sep_pos: The position of the separator.
        :type sep_pos: int
        """
        if digit_count < 0 or sep_pos < 0 or sep_pos > digit_count:
            raise ValueError(
                "digit_count and sep_pos must be non-negative and sep_pos must be less than or equal to digit_count."
            )

        self._digit_count = digit_count
        self._sep_pos = sep_pos
        self._spinbox.set_digit_format(digit_count, sep_pos)

    def set_range(self, min_value: float | int, max_value: float | int) -> None:
        """Set the range of the spinbox.

        :param min_value: The minimum value of the spinbox.
        :type min_value: float | int
        :param max_value: The maximum value of the spinbox.
        :type max_value: float | int

        UiFlow2 Code Block:

            |set_range.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox0.set_range(0, 100)
        """
        if min_value >= max_value:
            raise ValueError("min_value must be less than max_value.")

        self._min_value = min_value
        self._max_value = max_value
        self._spinbox.set_range(
            self.value2raw(min_value, self._digit_count, self._sep_pos),
            self.value2raw(max_value, self._digit_count, self._sep_pos),
        )

    def set_value(self, value: float | int) -> None:
        """Set the value of the spinbox.

        :param value: The value to set.
        :type value: float | int

        UiFlow2 Code Block:

            |set_value.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox0.set_value(50)
        """
        if value < self._min_value or value > self._max_value:
            raise ValueError(f"Value must be between {self._min_value} and {self._max_value}.")

        self._spinbox.set_value(self.value2raw(value, self._digit_count, self._sep_pos))

    def get_value(self) -> float | int:
        """Get the current value of the spinbox.

        :return: The current value.
        :rtype: float | int

        UiFlow2 Code Block:

            |get_value.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox0.get_value()
        """
        return self.raw2value(self._spinbox.get_value(), self._digit_count, self._sep_pos)

    def set_step(self, step: float | int) -> None:
        """Set the step value for the spinbox.

        :param step: The step value to set.
        :type step: float | int

        UiFlow2 Code Block:

            |set_step.png|

        MicroPython Code Block:

            .. code-block:: python

                spinbox0.set_step(1)
                spinbox0.set_step(0.1)
        """
        self._spinbox.set_step(self.value2raw(step, self._digit_count, self._sep_pos))

    @staticmethod
    def value2raw(value: float | int, digit_count: int, sep_pos: int) -> int:
        """Convert a float to an integer by removing the decimal point.

        :param float value: The float value to convert.
        :return: The converted integer value.
        :rtype: int
        """
        if sep_pos < 0 or sep_pos >= digit_count:
            raise ValueError("sep_pos must be between 0 and digit_count.")

        dec_pos = digit_count - sep_pos
        return int(value * (10**dec_pos))

    @staticmethod
    def raw2value(raw: int, digit_count: int, sep_pos: int) -> float | int:
        """Convert an integer to a float with a specified decimal point position.

        :param int value: The integer value to convert.
        :param int digit_count: The total number of digits in the float representation.
        :param int sep_pos: The position of the decimal point.
        :return: The converted float value.
        :rtype: float
        """
        if sep_pos < 0 or sep_pos >= digit_count:
            raise ValueError("sep_pos must be between 0 and digit_count.")

        if sep_pos == 0:
            return raw

        dot_pos = sep_pos
        s = str(raw)
        if len(s) < digit_count:
            if s.find("-") == 0:
                dot_pos += 1
                s = "-" + "0" * (digit_count - len(s) + 1) + s[1:]
            else:
                s = "0" * (digit_count - len(s)) + s
        return float(".".join([s[:dot_pos], s[dot_pos:]]))

    def __getattr__(self, name):
        # First check if it's a method from M5Base
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method

        # Then check if it's a method from the spinbox widget
        if hasattr(self._spinbox, name):
            attr = getattr(self._spinbox, name)
            if callable(attr):
                # Create a bound method that delegates to the spinbox
                bound_method = lambda *args, **kwargs: attr(*args, **kwargs)
                setattr(self, name, bound_method)
                return bound_method
            else:
                # For non-callable attributes, return them directly
                return attr

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
