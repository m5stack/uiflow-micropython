# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv


class M5Keyboard(lv.keyboard):
    """Create a keyboard widget.

    :param int x: The x position of the keyboard.
    :param int y: The y position of the keyboard.
    :param int w: The width of the keyboard.
    :param int h: The height of the keyboard.
    :param int mode: The keyboard mode, default is `lv.keyboard.MODE.TEXT_LOWER`.
    :param lv.obj target_textarea: The target textarea to link with the keyboard.
    :param lv.obj parent: The parent object, default is the active screen.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            import m5ui
            import lvgl as lv

            m5ui.init()
            keyboard = m5ui.M5Keyboard(x=0, y=120, w=320, h=100, target_textarea=None, parent=page0)
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=200,
        h=100,
        mode=lv.keyboard.MODE.TEXT_LOWER,
        target_textarea=None,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)

        self.set_size(w, h)
        self.set_pos(x, y)
        self.set_align(lv.ALIGN.TOP_LEFT)
        self.set_mode(mode)
        self.set_textarea(target_textarea)

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
