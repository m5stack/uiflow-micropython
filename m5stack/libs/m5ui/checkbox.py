# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv


class M5Checkbox(lv.checkbox):
    """Create a checkbox object.

    :param str title: The title text of the checkbox.
    :param bool value: The initial checked state of the checkbox.
    :param int x: The x position of the checkbox.
    :param int y: The y position of the checkbox.
    :param int title_c: The color of the title text in hexadecimal format.
    :param lv.lv_font_t title_font: The font to use for the title text.
    :param int bullet_border_c: The border color of the checkbox bullet in hexadecimal format.
    :param int bullet_bg_c: The background color of the checkbox bullet in hexadecimal format.
    :param lv.obj parent: The parent object to attach the checkbox to. If not specified, the checkbox will be attached to the default screen.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Checkbox
            import lvgl as lv
            m5ui.init()
            checkbox_0 = M5Checkbox(title="Check Me", value=True, x=10, y=10, title_c=0x2121, title_font=lv.font_montserrat_14, bullet_border_c=0x2196F3, bullet_bg_c=0xFFFFFF, parent=page0)

    """

    def __init__(
        self,
        title="Checkbox",
        value=False,
        x=0,
        y=0,
        title_c=0x2121,
        title_font=lv.font_montserrat_14,
        bullet_border_c=0x2196F3,
        bullet_bg_c=0xFFFFFF,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)

        self.set_pos(x, y)
        self.set_text(title)
        self.set_state(lv.STATE.CHECKED, value)

        part = lv.STATE.CHECKED if value else lv.STATE.DEFAULT

        self.set_text_color(title_c, lv.OPA.COVER, lv.PART.MAIN | part)
        self.set_style_text_font(title_font, lv.PART.MAIN | lv.STATE.DEFAULT)

        self.set_bg_color(bullet_bg_c, lv.OPA.COVER, lv.PART.INDICATOR | part)
        self.set_border_color(bullet_border_c, lv.OPA.COVER, lv.PART.INDICATOR | part)

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
