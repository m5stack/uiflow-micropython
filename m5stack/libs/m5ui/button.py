# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv


class M5Button(lv.button):
    """Create a button object.

    :param str text: The text to display on the button.
    :param int x: The x position of the button.
    :param int y: The y position of the button.
    :param int w: The width of the button. when set to 0, the button will automatically size to fit the text.
    :param int h: The height of the button. when set to 0, the button will automatically size to fit the text.
    :param int bg_c: The background color of the button in hexadecimal format.
    :param int text_c: The text color of the button in hexadecimal format.
    :param lv.lv_font_t font: The font to use for the button text.
    :param lv.obj parent: The parent object to attach the button to. If not specified, the button will be attached to the default screen.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Button
            import lvgl as lv

            m5ui.init()
            button_0 = M5Button(text="Click Me", x=10, y=10, bg_c=0x2196F3, text_c=0xFFFFFF, parent=page0)
    """

    EFFECT_SIMPLE = 0
    EFFECT_WAVE = 1
    EFFECT_GUMMY = 2

    def __init__(
        self,
        text="button0",
        x=0,
        y=0,
        w=0,
        h=0,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_text_color(text_c, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_bg_color(bg_c, 255, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_style_text_font(font, lv.PART.MAIN | lv.STATE.DEFAULT)
        if w > 0 and h > 0:
            self.set_size(w, h)
        self.label = lv.label(self)
        self.label.set_text(text)
        self.label.set_align(lv.ALIGN.CENTER)

        self.trans_def = self.get_style_transition(lv.PART.MAIN | lv.STATE.DEFAULT)
        self.trans_pr = self.get_style_transition(lv.PART.MAIN | lv.STATE.PRESSED)

    def set_btn_text(self, text: str) -> None:
        """Set the text of the button.

        :param str text: The text to set on the button.

        UiFlow2 Code Block:

            |set_btn_text.png|

        MicroPython Code Block:

            .. code-block:: python

                button_0.set_btn_text("Click Me")
        """
        self.label.set_text(text)

    def set_style_radius(self, radius: int, part: int) -> None:
        if radius < 0:
            raise ValueError("Radius must be a non-negative integer.")
        super().set_style_radius(radius, part)

    def get_btn_text(self) -> str:
        """Get the text of the button.

        :return: The text of the button.
        :rtype: str

        UiFlow2 Code Block:

            |get_btn_text.png|

        MicroPython Code Block:
            .. code-block:: python

                text = button_0.get_btn_text()
        """
        return self.label.get_text()

    def set_shadow(self, color, opa, align, offset_x, offset_y):
        if isinstance(color, int):
            color = lv.color_hex(color)

        self.set_style_text_color(color, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_style_text_opa(opa, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.align_to(self, align, offset_x, offset_y)

    def unset_shadow(self):
        raise NotImplementedError

    def _effect_simple(self):
        self.set_style_transition(self.trans_def, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_style_transition(self.trans_pr, lv.PART.MAIN | lv.STATE.PRESSED)

    def _effect_wave(self):
        pass

    def _effect_gummy(self):
        trans_def = lv.style_transition_dsc_t()
        trans_def.init(
            [
                lv.STYLE.TRANSFORM_WIDTH,
                lv.STYLE.TRANSFORM_HEIGHT,
                lv.STYLE.TEXT_LETTER_SPACE,
                0,
            ],
            lv.anim_t.path_overshoot,
            250,
            100,
            None,
        )

        trans_pr = lv.style_transition_dsc_t()
        trans_pr.init(
            [
                lv.STYLE.TRANSFORM_WIDTH,
                lv.STYLE.TRANSFORM_HEIGHT,
                lv.STYLE.TEXT_LETTER_SPACE,
                0,
            ],
            lv.anim_t.path_overshoot,
            250,
            0,
            None,
        )

        self.set_style_transition(trans_def, lv.PART.MAIN | lv.STATE.DEFAULT)
        self.set_style_transform_width(10, lv.PART.MAIN | lv.STATE.PRESSED)
        self.set_style_transform_height(-10, lv.PART.MAIN | lv.STATE.PRESSED)
        self.set_style_text_letter_space(10, lv.PART.MAIN | lv.STATE.PRESSED)

    def set_pressed_effect(self, effect):
        if effect == self.EFFECT_SIMPLE:
            self._effect_simple()
        elif effect == self.EFFECT_WAVE:
            raise NotImplementedError("Wave effect is not implemented yet.")
        elif effect == self.EFFECT_GUMMY:
            self._effect_gummy()
        else:
            raise ValueError(f"Unknown effect: {effect}")

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
