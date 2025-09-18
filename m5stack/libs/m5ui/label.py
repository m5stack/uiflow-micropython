# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from m5ui.base import M5Base
import lvgl as lv


class M5Label(lv.label):
    """Create a label object.

    :param str text: The text to display on the label.
    :param int x: The x position of the label.
    :param int y: The y position of the label.
    :param int text_c: The text color of the label in hexadecimal format.
    :param int bg_c: The background color of the label in hexadecimal format.
    :param int bg_opa: The background opacity of the label (0-255).
    :param lv.lv_font_t font: The font to use for the button text.
    :param lv.obj parent: The parent object to attach the button to. If not specified, the button will be attached to the default screen.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Label
            import lvgl as lv

            m5ui.init()
            label_0 = M5Label(text="Hello, World!", x=10, y=10, text_c=0x212121, bg_c=0xFFFFFF, bg_opa=0, font=lv.font_montserrat_14, parent=page0)
    """

    def __init__(
        self,
        text,
        x=0,
        y=0,
        text_c=0x212121,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.set_text(text)
        self.set_pos(x, y)
        self.set_text_color(text_c, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_bg_color(bg_c, bg_opa, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_style_text_font(font, lv.PART.MAIN | lv.STATE.DEFAULT)
        self._shadow_label = lv.label(self)
        self.unset_shadow()

    def set_shadow(self, color: int, opa: int, align: int, offset_x: int, offset_y: int) -> None:
        """Set a shadow for the label.

        :param int color: The color of the shadow in hexadecimal format or an integer.
        :param int opa: The opacity of the shadow (0-255).
        :param int align: The alignment of the shadow relative to the label.
        :param int offset_x: The horizontal offset of the shadow.
        :param int offset_y: The vertical offset of the shadow.
        :return: None

        UiFlow2 Code Block:

            |set_shadow.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.set_shadow(color=0x000000, opa=128, align=lv.ALIGN.BOTTOM_RIGHT, offset_x=5, offset_y=5)
        """
        if isinstance(color, int):
            color = lv.color_hex(color)

        self._shadow_label.remove_flag(lv.obj.FLAG.HIDDEN)

        self._shadow_label.set_text(self.get_text())
        self._shadow_label.set_style_text_color(color, lv.PART.MAIN | lv.STATE.DEFAULT)
        self._shadow_label.set_style_text_opa(opa, lv.PART.MAIN | lv.STATE.DEFAULT)
        self._shadow_label.set_style_text_font(
            self.get_style_text_font(lv.PART.MAIN), lv.PART.MAIN
        )
        self._shadow_label.set_width(self.get_width())

        for part in (lv.PART.MAIN,):
            self._shadow_label.set_style_pad_left(self.get_style_pad_left(part), part)
            self._shadow_label.set_style_pad_right(self.get_style_pad_right(part), part)
            self._shadow_label.set_style_pad_top(self.get_style_pad_top(part), part)
            self._shadow_label.set_style_pad_bottom(self.get_style_pad_bottom(part), part)

        if isinstance(self.get_parent(), lv.list):
            offset_x -= self.get_style_pad_left(part)
        self._shadow_label.align_to(self, align, offset_x, offset_y)

    def unset_shadow(self) -> None:
        """Remove the shadow from the label.

        UiFlow2 Code Block:

            |unset_shadow.png|

        MicroPython Code Block:

            .. code-block:: python

                label_0.unset_shadow()
        """
        self._shadow_label.add_flag(lv.obj.FLAG.HIDDEN)

    def set_style_radius(self, radius: int, part: int) -> None:
        if radius < 0:
            raise ValueError("Radius must be a non-negative integer.")
        super().set_style_radius(radius, part)

    def __del__(self):
        self._shadow_label.delete()
        super().__delete__()

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
