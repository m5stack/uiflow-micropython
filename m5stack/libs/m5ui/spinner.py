# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from m5ui.base import M5Base
import lvgl as lv


class M5Spinner(lv.spinner):
    """Create a spinner object.

    :param int x: The x position of the spinner.
    :param int y: The y position of the spinner.
    :param int w: The width of the spinner.
    :param int h: The height of the spinner.
    :param int anim_t: The animation time in milliseconds.
    :param int angle: The angle of the spinner in degrees.
    :param lv.obj parent: The parent object to attach the spinner to. If not specified, the spinner will be attached to the default screen.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Spinner
            import lvgl as lv

            m5ui.init()
            spinner_0 = M5Spinner(x=120, y=80, w=60, h=30, anim_t=1000, angle=180, parent=page0)
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=0,
        h=0,
        anim_t=10000,
        angle=180,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_size(w, h)
        self.set_anim_params(anim_t, angle)

    def set_spinner_color(self, color, opa: int, part: int):
        """Set the color of the spinner.

        :param int color: The color of the spinner in hexadecimal format.

        UiFlow2 Code Block:

            |set_spinner_color.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_spinner_color(0x2196F3, lv.PART.MAIN | lv.STATE.DEFAULT)
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
