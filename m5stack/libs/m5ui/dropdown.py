# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv
import warnings


class M5Dropdown(lv.dropdown):
    """Create a dropdown object.

    :param x: The x position of the dropdown.
    :param y: The y position of the dropdown.
    :param w: The width of the dropdown.
    :param h: The height of the dropdown, default is `lv.SIZE_CONTENT`.
    :param options: A list of options to display in the dropdown.
    :param direction: The direction of the dropdown, can be `lv.DIR.LEFT`, `lv.DIR.RIGHT`, `lv.DIR.TOP`, or `lv.DIR.BOTTOM`.
    :param show_selected: Whether to highlight the selected option, default is `True`.
    :param font: The font used for the text in the dropdown, default is `lv.font_montserrat_14`.
    :param parent: The parent object for this dropdown, default is the active screen.
    """

    def __init__(
        self,
        x=0,
        y=0,
        w=100,
        h=lv.SIZE_CONTENT,
        options: list = [],
        direction: int = lv.DIR.RIGHT,
        show_selected: bool = True,
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
            self.set_options(options)

        self.set_dir(direction)
        self.set_selected_highlight(show_selected)
        self.set_style_text_font(font, lv.PART.MAIN)

    def set_options(self, options: list):
        """Set the options for the dropdown.

        :param options: A list of options to display in the dropdown.

        UiFlow2 Code Block:

            |set_options.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.set_options(["option1", "option2", "option3"])
        """
        if isinstance(options, list):
            self.options = options
            options = "\n".join(options)
            super().set_options(options)
        else:
            warnings.warn("Options must be a list.")

    def get_options(self) -> list:
        """Get the list of options in the dropdown.

        :return: The list of options.
        :rtype: list
        """
        return self.options

    def add_option(self, option: str, pos: int) -> None:
        """Add an option to the dropdown at a specific position.

        :param option: The option to add.
        :param pos: The position to insert the option at.

        UiFlow2 Code Block:

            |add_option.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.add_option("New Option", 1)
        """
        if pos < 0 or pos > len(self.options):
            warnings.warn("Position out of range, appending to the end.")
            pos = len(self.options)
        self.options.insert(pos, option)
        super().add_option(option, pos)

    def clear_options(self) -> None:
        """Clear all options in the dropdown.

        UiFlow2 Code Block:

            |clear_options.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.clear_options()
        """
        self.options = []
        super().set_options("")

    def get_selected_str(self) -> str:
        """Get the currently selected option as a string.

        :return: The selected option as a string.

        UiFlow2 Code Block:

            |get_selected_str.png|

        MicroPython Code Block:

            .. code-block:: python

                selected_option = dropdown_0.get_selected_str()
        """
        sel = bytearray(32)
        super().get_selected_str(sel, len(sel))
        return sel.decode("utf-8").rstrip("\x00")

    def set_dir(self, direction: int) -> None:
        """Set the direction of the dropdown.

        :param direction: The direction of the dropdown, can be `lv.DIR.LEFT`, `lv.DIR.RIGHT`, `lv.DIR.TOP`, or `lv.DIR.BOTTOM`.

        UiFlow2 Code Block:

            |set_dir.png|

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.set_dir(lv.DIR.LEFT)
        """
        super().set_dir(direction)
        if direction == lv.DIR.LEFT:
            self.set_symbol(lv.SYMBOL.LEFT)
        elif direction == lv.DIR.RIGHT:
            self.set_symbol(lv.SYMBOL.RIGHT)
        elif direction == lv.DIR.TOP:
            self.set_symbol(lv.SYMBOL.UP)
        elif direction == lv.DIR.BOTTOM:
            self.set_symbol(lv.SYMBOL.DOWN)

    def set_style_radius(self, radius: int, part: int) -> None:
        """Set the radius of the dropdown's corners.

        :param radius: The radius of the corners in pixels.
        :param part: The part of the dropdown to apply the radius to, e.g., `lv.PART.MAIN`.

        UiFlow2 Code Block:

            None

        MicroPython Code Block:

            .. code-block:: python

                dropdown_0.set_style_radius(10, lv.PART.MAIN | lv.STATE.DEFAULT)
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
