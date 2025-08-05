# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from m5ui.base import M5Base
import lvgl as lv
import m5ui


class M5List(lv.list):
    """Create a list object.

    :param int x: The x position of the list.
    :param int y: The y position of the list.
    :param int w: The width of the list.
    :param int h: The height of the list.
    :param lv.obj parent: The parent object to attach the list to. If not specified, the list will be attached to the default screen.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5List
            import lvgl as lv

            m5ui.init()
            list_0 = M5List(x=120, y=80, w=60, h=30, parent=page0)
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

    def add_text(
        self,
        text,
        text_c=0x212121,
        text_opa=255,
        bg_c=0xE6E2E6,
        bg_opa=255,
        font=lv.font_montserrat_14,
    ):
        """Add a text label to the list.

        :param str text: The text to display on the label.
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

                list_0.add_text("Item 1", text_c=0x000000, text_opa=255, bg_c=0xFFFFFF, bg_opa=255, font=lv.font_montserrat_14)
        """
        _label = m5ui.M5Label(
            text=text, text_c=text_c, bg_c=bg_c, bg_opa=bg_opa, font=font, parent=self
        )
        _label.set_style_text_opa(text_opa, lv.PART.MAIN | lv.STATE.DEFAULT)
        _label.set_width(lv.pct(100))
        _label.set_style_margin_left(-14, lv.PART.MAIN | lv.STATE.DEFAULT)
        _label.set_style_margin_right(-14, lv.PART.MAIN | lv.STATE.DEFAULT)
        _label.set_style_pad_left(14, lv.PART.MAIN | lv.STATE.DEFAULT)
        _label.set_style_pad_right(14, lv.PART.MAIN | lv.STATE.DEFAULT)
        return _label

    def add_button(
        self,
        icon,
        text="button0",
        h=0,
        bg_c=0xFFFFFF,
        bg_opa=255,
        text_c=0x000000,
        text_opa=255,
        font=lv.font_montserrat_14,
    ):
        """Add a button to the list.

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

                list_0.add_button(lv.SYMBOL.BULLET, text="Home", h=40, bg_c=0xFFFFFF, text_c=0x000000, font=lv.font_montserrat_14)
        """
        _button = m5ui.M5Button(
            text=text, w=1, h=h, bg_c=bg_c, text_c=text_c, font=font, parent=self
        )
        if icon:
            _icon = lv.image(_button)
            _icon.set_src(icon)
            _icon.move_to_index(0)

        _button.set_width(lv.pct(100))
        _button.set_flex_flow(lv.FLEX_FLOW.ROW)
        _button.set_style_margin_left(-14, lv.PART.MAIN)
        _button.set_style_margin_right(-14, lv.PART.MAIN)
        _button.set_style_pad_left(14, lv.PART.MAIN)
        _button.set_style_pad_right(14, lv.PART.MAIN)
        _button.set_style_radius(0, lv.PART.MAIN | lv.STATE.DEFAULT)
        _button.set_style_border_side(lv.BORDER_SIDE.BOTTOM, 0)
        _button.set_style_border_width(1, 0)
        _button.set_style_border_color(lv.color_hex(0xECE9EC), 0)
        _button.set_style_bg_opa(bg_opa, lv.PART.MAIN | lv.STATE.DEFAULT)
        _button.set_style_text_opa(text_opa, lv.PART.MAIN | lv.STATE.DEFAULT)
        return _button

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
