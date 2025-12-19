# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .base import M5Base
import lvgl as lv


class M5Table(lv.table):
    """Create a table object.

    :param int x: The x position of the table.
    :param int y: The y position of the table.
    :param int w: The width of the table.
    :param int h: The height of the table.
    :param int row_cnt: Number of rows.
    :param int col_cnt: Number of columns.
    :param lv.obj parent: The parent object to attach the table to. If not specified, the table will be attached to the default screen.

    UiFlow2 Code Block:

        None

    MicroPython Code Block:

        .. code-block:: python

            from m5ui import M5Table
            import lvgl as lv

            m5ui.init()
            table_0 = M5Table(x=30, y=20, w=200, h=150, row_cnt=2, col_cnt=2)
    """

    def __init__(self, x=30, y=20, w=200, h=150, row_cnt=2, col_cnt=2, parent=None):
        if parent is None:
            parent = lv.screen_active()
        super().__init__(parent)
        self.set_pos(x, y)
        self.set_size(w, h)
        self.set_row_count(row_cnt)
        self.set_column_count(col_cnt)
        # Enable column borders (default theme only shows row borders)
        self.set_style_border_side(lv.BORDER_SIDE.FULL, lv.PART.ITEMS)

    def __getattr__(self, name):
        if hasattr(M5Base, name):
            method = getattr(M5Base, name)
            bound_method = lambda *args, **kwargs: method(self, *args, **kwargs)
            setattr(self, name, bound_method)
            return bound_method
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
