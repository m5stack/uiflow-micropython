# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv
import warnings


class M5Roller(lv.roller):
    """Create a roller widget.

    :param int x: X position of the widget.
    :param int y: Y position of the widget.
    :param int w: Width of the widget.
    :param int h: Height of the widget.
    :param list options: List of options to display in the roller.
    :param lv.roller.MODE mode: Roller mode (default is NORMAL).
    :param int selected: Index of the initially selected option.
    :param int visible_row_count: Number of visible rows in the roller.
    :param lv.font_t font: Font to use for the text in the roller.
    :param parent: Parent widget to attach this roller to (default is the active screen).
    :type parent: lv.obj or None

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Roller
            import lvgl as lv
            m5ui.init()
            roller_0 = M5Roller(x=10, y=10, w=100, h=100, options=["Option 1", "Option 2"], mode=lv.roller.MODE.NORMAL, selected=0, visible_row_count=2, font=lv.font_montserrat_14, parent=page0)
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=100,
        h=100,
        options=[],
        mode=lv.roller.MODE.NORMAL,
        selected=0,
        visible_row_count=2,
        font: lv.font_t = lv.font_montserrat_14,
        parent=None,
    ):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_size(w, h)

        self.options = []
        if options:
            self.set_options(options, mode)

        self.set_selected(selected, True)
        self.set_visible_row_count(visible_row_count)
        self.set_style_text_font(font, lv.PART.MAIN | lv.STATE.DEFAULT)

    def set_options(self, options: list, mode=lv.roller.MODE.NORMAL):
        """Set the options for the roller.

        :param list options: List of options to display in the roller.
        :param lv.roller.MODE mode: Roller mode (default is NORMAL).

        UiFlow2 Code Block:

            |set_options.png|

        MicroPython Code Block:

            .. code-block:: python

                roller_0.set_options(["Option 1", "Option 2"], mode=lv.roller.MODE.NORMAL)
        """
        if isinstance(options, list):
            self.options = options
            options = "\n".join(options)
            super().set_options(options, mode)
        else:
            warnings.warn("Options must be a list.")

    def get_options(self) -> list:
        """Get the list of options in the dropdown.

        :return: The list of options.
        :rtype: list

        UiFlow2 Code Block:

            |get_options.png|

        MicroPython Code Block:

            .. code-block:: python

                options = roller_0.get_options()
        """
        return self.options

    def get_selected_str(self) -> str:
        """Get the currently selected option as a string.

        :return: The selected option as a string.

        UiFlow2 Code Block:

            |get_selected_str.png|

        MicroPython Code Block:

            .. code-block:: python

                selected_option = roller_0.get_selected_str()
        """
        sel = bytearray(32)
        super().get_selected_str(sel, len(sel))
        return sel.decode("utf-8").rstrip("\x00")

    def set_style_radius(self, radius: int, part: int) -> None:
        """Set the corner radius of the slider components.

        :param int radius: The radius to set.
        :param int part: The part of the object to apply the style to (e.g., lv.PART.MAIN, lv.PART.SELECTED).
        :return: None

        UiFlow2 Code Block:

            |set_style_radius.png|

        MicroPython Code Block:

            .. code-block:: python

                roller_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
                roller_0.set_style_radius(10, lv.PART.SELECTED | lv.STATE.DEFAULT)
        """
        if radius < 0:
            warnings.warn("Radius must be a non-negative integer.")
            return
        super().set_style_radius(radius, part)

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
