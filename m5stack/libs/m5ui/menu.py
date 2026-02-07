# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from m5ui.base import M5Base
import lvgl as lv
import m5ui


class M5Menu(lv.menu):
    """Create a list object.

    :param int x: The x position of the menu.
    :param int y: The y position of the menu.
    :param int w: The width of the menu.
    :param int h: The height of the menu.
    :param str page_name: The name of the main page of the menu.
    :param lv.obj parent: The parent object to attach the menu to. If not specified, the menu will be attached to the default screen.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Menu
            import lvgl as lv

            m5ui.init()
            menu0 = M5Menu(x=120, y=80, w=60, h=30, parent=page0)
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=0,
        h=0,
        page_name=None,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_size(w, h)
        self.main_page = lv.menu_page(self, page_name)  # Create a main page

    def add_label(
        self,
        text,
        text_c=0x212121,
        text_opa=255,
        bg_c=0xFFFFFF,
        bg_opa=255,
        font=lv.font_montserrat_14,
        parent=None,
    ):
        """Add a label to the menu.

        :param str text: The text to display on the label.
        :param int text_c: The text color of the label.
        :param int bg_c: The background color of the label.
        :param int bg_opa: The background opacity of the label.
        :param lv.font_t font: The font of the label.
        :param lv.obj parent: The parent object to attach the label to. If not specified, the label will be attached to the main page of the menu.
        :return: The created label object.
        :rtype: :ref:`m5ui.M5Label <m5ui.M5Label>`

         UiFlow2 Code Block:

            |add_label.png|

            |add_label2.png|

        MicroPython Code Block:

            .. code-block:: python

                label0 = menu0.add_label("Hello, World!", text_c=0x212121, bg_c=0xFFFFFF, bg_opa=255, font=lv.font_montserrat_14, parent=menu0.main_page)
        """
        if parent is None:
            parent = self.main_page
        _cont = lv.menu_cont(parent)
        _label = m5ui.M5Label(
            text=text, text_c=text_c, bg_c=bg_c, bg_opa=bg_opa, font=font, parent=_cont
        )
        _label.cont = _cont
        _label.set_style_text_opa(text_opa, lv.PART.MAIN | lv.STATE.DEFAULT)
        return _label

    def add_switch(
        self,
        text,
        w=50,
        h=20,
        bg_c=0xE7E3E7,
        bg_opa=255,
        bg_c_checked=0x0288FB,
        bg_c_checked_opa=255,
        circle_c=0xFFFFFF,
        circle_opa=255,
        parent=None,
    ):
        """Add a switch to the menu.

        :param str text: The text to display next to the switch.
        :param int w: The width of the switch.
        :param int h: The height of the switch.
        :param int bg_c: The background color of the switch when unchecked.
        :param int bg_c_checked: The background color of the switch when checked.
        :param int circle_c: The color of the switch circle.
        :param lv.obj parent: The parent object to attach the switch to. If not specified, the switch will be attached to the main page of the menu.
        :return: The created switch object.
        :rtype: :ref:`m5ui.M5Switch <m5ui.M5Switch>`

        UiFlow2 Code Block:

            |add_switch.png|

            |add_switch2.png|

        MicroPython Code Block:

            .. code-block:: python

                switch_0 = menu0.add_switch("Switch 1", w=50, h=20, bg_c=0xE7E3E7, bg_c_checked=0x0288FB, circle_c=0xFFFFFF, parent=menu0.main_page)
        """

        if parent is None:
            parent = self.main_page
        _cont = lv.menu_cont(parent)
        _label = lv.label(_cont)
        _label.set_text(text)
        _label.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
        _switch = m5ui.M5Switch(
            w=w,
            h=h,
            bg_c=bg_c,
            bg_c_checked=bg_c_checked,
            circle_c=circle_c,
            parent=_cont,
        )
        _switch.set_style_bg_opa(bg_opa, lv.PART.MAIN | lv.STATE.DEFAULT)
        _switch.set_style_bg_opa(bg_c_checked_opa, lv.PART.INDICATOR | lv.STATE.CHECKED)
        _switch.set_style_bg_opa(circle_opa, lv.PART.KNOB | lv.STATE.DEFAULT)

        return _switch

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
