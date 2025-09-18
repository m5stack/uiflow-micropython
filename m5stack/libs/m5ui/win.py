# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from m5ui.base import M5Base
import lvgl as lv
import m5ui

try:
    DPI = int(lv.DPI_DEF / 3)
except Exception:
    DPI = 80


class M5Win(lv.win):
    """Create a window object.

    :param int x: The x position of the window.
    :param int y: The y position of the window.
    :param int w: The width of the window.
    :param int h: The height of the window.
    :param lv.obj parent: The parent object to attach the window to. If not specified, the window will be attached to the default screen.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Win
            import lvgl as lv

            m5ui.init()
            win0 = M5Win(x=120, y=80, w=60, h=30, parent=page0)
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=0,
        h=0,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_size(w, h)

    def add_title(
        self,
        text,
        text_c=0x212121,
        text_opa=255,
        bg_c=0xE0E0E0,
        bg_opa=255,
        font=lv.font_montserrat_14,
    ):
        """Add a title label to the window.

        :param str text: The text to display on the window.
        :param int text_c: The text color of the label in hexadecimal format.
        :param int text_opa: The text opacity of the label (0-255).
        :param int bg_c: The background color of the label in hexadecimal format.
        :param int bg_opa: The background opacity of the label (0-255).
        :param lv.font font: The font to use for the label.
        :return: The created label object :ref:`m5ui.M5Label <m5ui.M5Label>`.
        :rtype: lv.obj

        UiFlow2 Code Block:

            |add_title.png|

            |add_title2.png|

        MicroPython Code Block:

            .. code-block:: python

                win0.add_title("A title", text_c=0x212121, text_opa=255, bg_c=0xE0E0E0, bg_opa=255, font=lv.font_montserrat_14)
        """
        _label = m5ui.M5Label(
            text=text,
            text_c=text_c,
            bg_c=bg_c,
            bg_opa=bg_opa,
            font=font,
            parent=self.get_header(),
        )
        _label.set_long_mode(lv.label.LONG_MODE.DOTS)
        _label.set_flex_grow(1)
        _label.set_style_text_opa(text_opa, lv.PART.MAIN | lv.STATE.DEFAULT)
        return _label

    def add_text(
        self,
        text,
        x=0,
        y=0,
        text_c=0x212121,
        text_opa=255,
        bg_c=0xF6F6F6,
        bg_opa=255,
        font=lv.font_montserrat_14,
    ):
        """Add a text label to the window.

        :param str text: The text to display on the window.
        :param int x: The x position of the label.
        :param int y: The y position of the label.
        :param int text_c: The text color of the label in hexadecimal format.
        :param int text_opa: The text opacity of the label (0-255).
        :param int bg_c: The background color of the label in hexadecimal format.
        :param int bg_opa: The background opacity of the label (0-255).
        :param lv.font font: The font to use for the label.
        :return: The created label object :ref:`m5ui.M5Label <m5ui.M5Label>`.
        :rtype: lv.obj

        UiFlow2 Code Block:

            |add_text.png|

            |add_text2.png|

        MicroPython Code Block:

            .. code-block:: python

                win0.add_text("A title", text_c=0x212121, text_opa=255, bg_c=0xF6F6F6, bg_opa=255, font=lv.font_montserrat_14)
        """
        _label = m5ui.M5Label(
            text=text,
            x=x,
            y=y,
            text_c=text_c,
            bg_c=bg_c,
            bg_opa=bg_opa,
            font=font,
            parent=self.get_content(),
        )
        _label.set_style_text_opa(text_opa, lv.PART.MAIN | lv.STATE.DEFAULT)
        return _label

    def add_button(
        self,
        icon=None,
        text="",
        w=DPI,
        bg_c=0x2196F3,
        bg_opa=255,
        text_c=0xFFFFFF,
        text_opa=255,
        font=lv.font_montserrat_14,
    ):
        """Add a button to the window.

        :param int icon: The icon to display on the button.
        :param str text: The text to display on the button.
        :param int h: The height of the button.
        :param int bg_c: The background color of the button in hexadecimal format.
        :param int bg_opa: The background opacity of the button (0-255).
        :param int text_c: The text color of the button in hexadecimal format.
        :param int text_opa: The text opacity of the button (0-255).
        :param lv.font font: The font to use for the button text.
        :return: The created button object :ref:`m5ui.M5Button <m5ui.M5Button>`.
        :rtype: lv.obj

        UiFlow2 Code Block:

            |add_button.png|

            |add_button2.png|

        MicroPython Code Block:

            .. code-block:: python

                win0.add_button(icon=lv.SYMBOL.BULLET, text_c=0xffffff, text_opa=255, bg_c=0x2196f3, bg_opa=255, font=lv.font_montserrat_14)

                win0.add_button(text='M5', text_c=0xffffff, text_opa=255, bg_c=0x2196f3, bg_opa=255, font=lv.font_montserrat_14)
        """
        _h = lv.pct(100)
        _button = m5ui.M5Button(
            text=text,
            w=w,
            h=_h,
            bg_c=bg_c,
            text_c=text_c,
            font=font,
            parent=self.get_header(),
        )
        _button.set_style_bg_opa(bg_opa, lv.PART.MAIN | lv.STATE.DEFAULT)
        _button.set_style_text_opa(text_opa, lv.PART.MAIN | lv.STATE.DEFAULT)

        if icon is not None:
            _icon = lv.image(_button)
            _icon.set_src(icon)
            _icon.set_align(lv.ALIGN.CENTER)
        return _button

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
