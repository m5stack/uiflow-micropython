
# M5Table

M5Table are built from rows, columns, and cells containing text.

## MicroPython Example

#### Table Basic Usage Example

This example demonstrates how to create a table with student information including names, ages, and scores. The table displays data for three students: Alice (18, 95), Bob (18, 80), and Carol (17, 86).

```python
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

## `M5Table`
Create a table object.

- Parameter `x` (`int`): The x position of the table.
- Parameter `y` (`int`): The y position of the table.
- Parameter `w` (`int`): The width of the table.
- Parameter `h` (`int`): The height of the table.
- Parameter `row_cnt` (`int`): Number of rows.
- Parameter `col_cnt` (`int`): Number of columns.
- Parameter `parent` (`lv.obj`): The parent object to attach the table to. If not specified, the table will be attached to the default screen.

    None

```python
from m5ui import M5Table
import lvgl as lv

m5ui.init()
table_0 = M5Table(x=30, y=20, w=200, h=150, row_cnt=2, col_cnt=2)
```

### `set_cell_value(row, col, value)`

        Set the value of a cell.

        New rows/columns are added automatically if required.

        - Parameter `row` (`int`): Row index [0 .. row_cnt - 1]
        - Parameter `col` (`int`): Column index [0 .. col_cnt - 1]
        - Parameter `value` (`str`): Text to display in the cell

        - Returns: None

```python
table_0.set_cell_value(row, col, value)
```
### `get_cell_value(row, col)`

        Get the value of a cell.

        - Parameter `row` (`int`): Row index
        - Parameter `col` (`int`): Column index
        - Returns: Text in the cell
        - Return type: str

```python
table_0.get_cell_value()
```
### `set_row_count(row_cnt)`

        Set the number of rows.

        - Parameter `row_cnt` (`int`): Number of rows.
        - Returns: None

```python
table_0.set_row_count(row_cnt)
```
### `set_column_count(col_cnt)`

        Set the number of columns.

        - Parameter `col_cnt` (`int`): Number of columns.
        - Returns: None

```python
table_0.set_column_count(col_cnt)
```
### `get_row_count()`

        Get the number of rows.

        - Returns: Number of row.
        - Return type: int

```python
row_cnt = table_0.get_row_count()
```
### `get_column_count()`

        Get the number of columns.

        - Returns: Number of columns.
        - Return type: int

```python
col_cnt = table_0.get_column_count()
```
### `set_column_width(col, width)`

        Set the width of a column.

        - Parameter `col` (`int`): Column index [0 .. LV_TABLE_COL_MAX - 1].
        - Parameter `width` (`int`): Column width.
        - Returns: None

```python
table_0.set_column_width(col, width)
```
### `get_column_width(col)`

        Get the width of a column.

        - Parameter `col` (`int`): Column index [0 .. LV_TABLE_COL_MAX - 1].
        - Returns: Column width.
        - Return type: int

```python
width = table_0.get_column_width()
```
### `set_pos(x, y)`

        Set the position of the Table.

        - Parameter `x` (`int`): The x position of the Table.
        - Parameter `y` (`int`): The y position of the Table.
        - Returns: None

```python
table_0.set_pos(x, y)
```
### `set_x(x)`

        Set the x position of the Table.

        - Parameter `x` (`int`): The x position of the Table.
        - Returns: None

```python
table_0.set_x(x)
```
### `set_y(y)`

        Set the y position of the Table.

        - Parameter `y` (`int`): The y position of the Table.
        - Returns: None

```python
table_0.set_y(y)
```
### `get_x()`

        Get the x position of the Table.

        - Returns: The x position of the Table.
        - Return type: int

```python
x = table_0.get_x()
```
### `get_y()`

        Get the y position of the Table.

        - Returns: The y position of the Table.
        - Return type: int

```python
y = table_0.get_y()
```
### `set_size(width, height)`

        Set the size of the Table.

        - Parameter `width` (`int`): The width of the Table.
        - Parameter `height` (`int`): The height of the Table.
        - Returns: None

```python
table_0.set_size(width, height)
```
### `set_width(width)`

        Set the width of the Table.

        - Parameter `width` (`int`): The width of the Table.
        - Returns: None

```python
table_0.set_width(width)
```
### `get_width()`

        Get the width of the Table.

        - Returns: The width of the Table.
        - Return type: int

```python
width = table_0.get_width()
```
### `set_height(height)`

        Set the height of the Table.

        - Parameter `height` (`int`): The height of the Table.
        - Returns: None

```python
table_0.set_height(height)
```
### `get_height()`

        Get the height of the Table.

        - Returns: The height of the Table.
        - Return type: int

```python
height = table_0.get_height()
```
### `align_to(obj, align, x, y)`

        Align the Table relative to another object.

        - Parameter `obj`: The reference object (e.g. page0).
        - Parameter `align` (`int`): Alignment option (see lv.ALIGN constants below).
        - Parameter `x` (`int`): X offset after alignment.
        - Parameter `y` (`int`): Y offset after alignment.
        - Returns: None

```python
table_0.align_to(page0, lv.ALIGN.CENTER, 0, 0)
```
### `lv.ALIGN`

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
