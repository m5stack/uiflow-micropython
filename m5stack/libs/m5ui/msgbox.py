# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from m5ui.base import M5Base
import lvgl as lv
import m5ui


class M5Msgbox(lv.msgbox):
    def __init__(
        self,
        title="",
        x=0,
        y=0,
        w=0,
        h=0,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.set_align(lv.ALIGN.DEFAULT)
        self.add_title(title)
        self.set_pos(x, y)
        self.set_size(w, h)

    def add_text(
        self,
        text,
        text_c=0x212121,
        text_opa=255,
        bg_c=0xFFFFFF,
        bg_opa=255,
        font=lv.font_montserrat_14,
    ):
        _label = m5ui.M5Label(
            text=text,
            text_c=text_c,
            bg_c=bg_c,
            bg_opa=bg_opa,
            font=font,
            parent=self.get_content(),
        )
        _label.set_width(lv.pct(100))
        _label.set_style_text_opa(text_opa, lv.PART.MAIN | lv.STATE.DEFAULT)
        return _label

    def add_button(
        self,
        icon=None,
        text="",
        bg_c=0x2196F3,
        bg_opa=255,
        text_c=0xFFFFFF,
        text_opa=255,
        font=lv.font_montserrat_14,
        option="footer",
    ):
        _parent = None
        _w = 0
        _h = 0
        if option == "header":
            _parent = self.get_header()
            if _parent is None:
                self.add_title("")
                _parent = self.get_header()
            _w = lv.DPI_DEF // 3
            _h = lv.pct(100)
        elif option == "footer":
            _parent = self.get_footer()
            if _parent is None:
                _tmp_btn = self.add_footer_button("")
                _parent = self.get_footer()
                _tmp_btn.delete()
            _w = lv.SIZE_CONTENT
            _h = lv.pct(100)
        _button = m5ui.M5Button(
            text=text, w=_w, h=_h, bg_c=bg_c, text_c=text_c, font=font, parent=_parent
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
