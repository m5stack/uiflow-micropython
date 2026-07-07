<!-- .. currentmodule:: m5ui -->

# M5Table

<!-- .. include:: ../refs/m5ui.table.ref -->

M5Table are built from rows, columns, and cells containing text.

## UiFlow2 Example

#### Table Basic Usage Example

Open the |cores3_m5ui_table_example.m5f2| project in UiFlow2.

This example demonstrates how to create a table with student information including names, ages, and scores. The table displays data for three students: Alice (18, 95), Bob (18, 80), and Carol (17, 86).

UiFlow2 Code Block:

Example output:

    None.

## MicroPython Example

#### Table Basic Usage Example

This example demonstrates how to create a table with student information including names, ages, and scores. The table displays data for three students: Alice (18, 95), Bob (18, 80), and Carol (17, 86).

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
table0 = None
table = None
i = None
info = None
row = None
k = None

def setup():
    global page0, table0, table, i, info, row, k

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    table0 = m5ui.M5Table(x=10, y=35, w=300, h=180, row_cnt=3, col_cnt=3, parent=page0)
    table = m5ui.M5Label(
        "M5UI Table Example",
        x=35,
        y=2,
        text_c=0x0000FF,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    page0.screen_load()
    for i in range(3):
        table0.set_column_width(i, 85)

    table0.set_column_count(3)
    table0.set_row_count(4)
    table0.set_width(260)
    table0.align_to(page0, lv.ALIGN.CENTER, 0, 10)
    table0.set_cell_value(0, 0, "name")
    table0.set_cell_value(0, 1, "age")
    table0.set_cell_value(0, 2, "score")
    info = {"name": ["Alice", "Bob", "Carol"], "age": [18, 18, 17], "score": [95, 80, 86]}
    row = 1
    for k in info["name"]:
        table0.set_cell_value(row, 0, k)
        row = row + 1
    row = 1
    for k in info["age"]:
        table0.set_cell_value(row, 1, str(k))
        row = row + 1
    row = 1
    for k in info["score"]:
        table0.set_cell_value(row, 2, str(k))
        row = row + 1

def loop():
    global page0, table0, table, i, info, row, k
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None.

## **API**

#### M5Table

## M5Table
Create a table object.

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

<!-- .. py:method:: set_cell_value(row, col, value) -->

        Set the value of a cell.

        New rows/columns are added automatically if required.

        :param int row: Row index [0 .. row_cnt - 1]
        :param int col: Column index [0 .. col_cnt - 1]
        :param str value: Text to display in the cell

        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                table_0.set_cell_value(row, col, value)

<!-- .. py:method:: get_cell_value(row, col) -->

        Get the value of a cell.

        :param int row: Row index
        :param int col: Column index
        :return: Text in the cell
        :rtype: str

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                table_0.get_cell_value()

<!-- .. py:method:: set_row_count(row_cnt) -->

        Set the number of rows.

        :param int row_cnt: Number of rows.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                table_0.set_row_count(row_cnt)

<!-- .. py:method:: set_column_count(col_cnt) -->

        Set the number of columns.

        :param int col_cnt: Number of columns.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                table_0.set_column_count(col_cnt)

<!-- .. py:method:: get_row_count() -->

        Get the number of rows.

        :return: Number of row.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                row_cnt = table_0.get_row_count()

<!-- .. py:method:: get_column_count() -->

        Get the number of columns.

        :return: Number of columns.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                col_cnt = table_0.get_column_count()

<!-- .. py:method:: set_column_width(col, width) -->

        Set the width of a column.

        :param int col: Column index [0 .. LV_TABLE_COL_MAX - 1].
        :param int width: Column width.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                table_0.set_column_width(col, width)

<!-- .. py:method:: get_column_width(col) -->

        Get the width of a column.

        :param int col: Column index [0 .. LV_TABLE_COL_MAX - 1].
        :return: Column width.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                width = table_0.get_column_width()

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the Table.

        :param int x: The x position of the Table.
        :param int y: The y position of the Table.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                table_0.set_pos(x, y)

<!-- .. py:method:: set_x(x) -->

        Set the x position of the Table.

        :param int x: The x position of the Table.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                table_0.set_x(x)

<!-- .. py:method:: set_y(y) -->

        Set the y position of the Table.

        :param int y: The y position of the Table.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                table_0.set_y(y)

<!-- .. py:method:: get_x() -->

        Get the x position of the Table.

        :return: The x position of the Table.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                x = table_0.get_x()

<!-- .. py:method:: get_y() -->

        Get the y position of the Table.

        :return: The y position of the Table.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                y = table_0.get_y()

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the Table.

        :param int width: The width of the Table.
        :param int height: The height of the Table.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                table_0.set_size(width, height)

<!-- .. py:method:: set_width(width) -->

        Set the width of the Table.

        :param int width: The width of the Table.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                table_0.set_width(width)

<!-- .. py:method:: get_width() -->

        Get the width of the Table.

        :return: The width of the Table.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                width = table_0.get_width()

<!-- .. py:method:: set_height(height) -->

        Set the height of the Table.

        :param int height: The height of the Table.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                table_0.set_height(height)

<!-- .. py:method:: get_height() -->

        Get the height of the Table.

        :return: The height of the Table.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                height = table_0.get_height()

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the Table relative to another object.

        :param obj: The reference object (e.g. page0).
        :param int align: Alignment option (see lv.ALIGN constants below).
        :param int x: X offset after alignment.
        :param int y: Y offset after alignment.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                table_0.align_to(page0, lv.ALIGN.CENTER, 0, 0)

<!-- .. py:data:: lv.ALIGN -->

        Alignment options for positioning objects.

        - lv.ALIGN.DEFAULT
        - lv.ALIGN.TOP_LEFT
        - lv.ALIGN.TOP_MID
        - lv.ALIGN.TOP_RIGHT
        - lv.ALIGN.BOTTOM_LEFT
        - lv.ALIGN.BOTTOM_MID
        - lv.ALIGN.BOTTOM_RIGHT
        - lv.ALIGN.LEFT_MID
        - lv.ALIGN.RIGHT_MID
        - lv.ALIGN.CENTER
        - lv.ALIGN.OUT_TOP_LEFT
        - lv.ALIGN.OUT_TOP_MID
        - lv.ALIGN.OUT_TOP_RIGHT
        - lv.ALIGN.OUT_BOTTOM_LEFT
        - lv.ALIGN.OUT_BOTTOM_MID
        - lv.ALIGN.OUT_BOTTOM_RIGHT
        - lv.ALIGN.OUT_LEFT_TOP
        - lv.ALIGN.OUT_LEFT_MID
        - lv.ALIGN.OUT_LEFT_BOTTOM
        - lv.ALIGN.OUT_RIGHT_TOP
        - lv.ALIGN.OUT_RIGHT_MID
        - lv.ALIGN.OUT_RIGHT_BOTTOM
