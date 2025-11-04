# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from m5ui.base import M5Base
from m5ui.button import M5Button
import lvgl as lv


class M5TabView(lv.tabview):
    """Create a TabView object.

    :param int x: The x position of the tab view.
    :param int y: The y position of the tab view.
    :param int w: The width of the tab view.
    :param int h: The height of the tab view.
    :param int bar_size: The size of the tab bar.
    :param int bar_pos: The position of the tab bar.
    :param lv.obj parent: The parent object to attach the tab view to. If not specified, the tab view will be attached to the default screen.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Label
            import lvgl as lv

            m5ui.init()
            tabview0 = m5ui.M5TabView(x=0, y=-2, w=320, h=240, bar_size=60, bar_pos=lv.DIR.TOP, parent=page0)
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=0,
        h=0,
        bar_size=60,
        bar_pos=lv.DIR.TOP,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_size(w, h)
        self.set_tab_bar_position(bar_pos)
        self.set_tab_bar_size(bar_size)
        self.tab_num = 0

    @staticmethod
    def _button_clicked_event_cb(event_struct):
        _button = event_struct.get_current_target()

        if not hasattr(_button, "get_parent"):
            _button = lv.obj.__cast__(_button)

        tv = _button.get_parent().get_parent()
        idx = _button.get_index()
        lv.tabview.set_active(tv, idx, False)

    def add_tab(self, text):
        """Add a tab to the tab view.

        :param str text: The text to display on the tab.
        :rtype: lv.obj

        UiFlow2 Code Block:

            |add_tab.png|

        MicroPython Code Block:

            .. code-block:: python

                Tab1 = tabview0.add_tab("Tab1")
                Tab2 = tabview0.add_tab("Tab2")
        """
        _button = M5Button(
            text=text,
            w=lv.pct(100),
            h=lv.pct(100),
            bg_c=0xFFFFFF,
            text_c=0x0,
            parent=self.get_tab_bar(),
        )
        _button.set_flex_grow(1)
        _button.add_event_cb(self._button_clicked_event_cb, lv.EVENT.CLICKED, None)

        _cont = self.get_content()
        _page = lv.obj(_cont)
        _page.set_size(lv.pct(100), lv.pct(100))
        self.tab_num += 1
        return _page

    def rename_tab(self, pos: int, txt: str) -> None:
        """Rename a tab in the tab view.

        :param int pos: The position of the tab to rename.
        :param str txt: The new text for the tab.

        UiFlow2 Code Block:

            |rename_tab.png|

        MicroPython Code Block:

            .. code-block:: python

                tabview0.rename_tab(0, 'hello M5')
        """
        if pos < self.tab_num:
            super().rename_tab(pos, txt)

    def get_tab_active(self) -> int:
        return super().get_tab_active() + 1

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
