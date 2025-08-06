# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv


class M5Page(lv.obj):
    """Create a page object.

    :param int bg_c: The background color of the page in hexadecimal format. Default is 0xFFFFFF (white).

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Page
            import lvgl as lv

            m5ui.init()
            page_0 = M5Page(bg_c=0xFFFFFF)
    """

    def __init__(self, bg_c=0xFFFFFF):
        super().__init__()
        self.set_bg_color(bg_c, lv.OPA.COVER, lv.PART.MAIN | lv.STATE.DEFAULT)

    def screen_load(self):
        """Load the page as the active screen.

        UiFlow2 Code Block:

            |screen_load.png|

        MicroPython Code Block:

            .. code-block:: python

                page_0.screen_load()
        """
        lv.screen_load(self)

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
