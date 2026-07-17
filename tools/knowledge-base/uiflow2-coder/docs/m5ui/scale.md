
# M5Scale

M5Scale is a widget that can be used to create scales in the user interface. Scale Widgets show linear or circular scales with configurable ranges, tick counts, placement, labeling, and subsections (Sections) with custom styling.

## MicroPython Example

#### scroll example

This example demonstrates how to create a scale widget with a range of values and custom styling.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
scale0 = None

def setup():
    global page0, scale0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    scale0 = m5ui.M5Scale(
        x=7,
        y=92,
        w=300,
        h=0,
        start_pos=0,
        end_pos=100,
        tick_count=11,
        tick_every=2,
        show_mode=lv.scale.MODE.HORIZONTAL_TOP,
        parent=page0,
    )

    page0.screen_load()
    scale0.set_style_line_width(2, lv.PART.MAIN)
    scale0.set_line_color(0x6600CC, 255, lv.PART.MAIN)
    scale0.set_style_line_width(4, lv.PART.INDICATOR)
    scale0.set_line_color(0xFF9900, 255, lv.PART.INDICATOR)
    scale0.set_style_line_width(6, lv.PART.ITEMS)
    scale0.set_line_color(0x66FF99, 255, lv.PART.ITEMS)

def loop():
    global page0, scale0
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

## **API**

#### M5Scale

## `M5Scale`
Create a scale object.

- Parameter `x` (`int`): The x position of the scale.
- Parameter `y` (`int`): The y position of the scale.
- Parameter `w` (`int`): The width of the scale. If not specified, it will be set based on the mode.
- Parameter `h` (`int`): The height of the scale. If not specified, it will be set based on the mode.
- Parameter `start_pos` (`int`): The starting position of the scale.
- Parameter `end_pos` (`int`): The ending position of the scale.
- Parameter `tick_count` (`int`): The total number of ticks on the scale.
- Parameter `tick_every` (`int`): The interval between major ticks on the scale.
- Parameter `mode` (`int`): The mode of the scale. It can be one of the following:

    Options:

        - `lv.scale.MODE.HORIZONTAL_TOP`: Horizontal top scale.
        - `lv.scale.MODE.HORIZONTAL_BOTTOM`: Horizontal bottom scale.
        - `lv.scale.MODE.VERTICAL_LEFT`: Vertical left scale.
        - `lv.scale.MODE.VERTICAL_RIGHT`: Vertical right scale.
        - `lv.scale.MODE.ROUND_INNER`: Round inner scale.
        - `lv.scale.MODE.ROUND_OUTER`: Round outer scale.

- Parameter `parent` (`lv.obj`): The parent object to attach the scale to. If not specified, the scale will be attached to the default screen.

```python
from m5ui import M5Scale
import lvgl as lv

m5ui.init()
scale_0 = M5Scale(x=10, y=10, w=200, h=20, start_pos=0, end_pos=100, tick_count=11, tick_every=2, mode=lv.scale.MODE.HORIZONTAL_TOP, parent=page0)
```

### `set_mode`

### `set_size`

### `set_pos`

### `set_x`

### `set_y`

### `align_to`

### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.

```python
scale_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `set_range(start_pos, end_pos)`

        Set the range of the scale.

        - Parameter `start_pos` (`int`): The start position of the scale.
        - Parameter `end_pos` (`int`): The end position of the scale.

```python
scale_0.set_range(0, 100)
```
### `set_major_tick_every(tick_every)`

        Set the interval for major ticks on the scale.

        - Parameter `tick_every` (`int`): The interval for major ticks.

```python
scale_0.set_major_tick_every(10)
```
### `set_total_tick_count(tick_count)`

        Set the total tick count of the scale.

        - Parameter `tick_count` (`int`): The total tick count.

```python
scale_0.set_total_tick_count(11)
```
### `set_label_show(label_show)`

        Set the visibility of the scale labels.

        - Parameter `label_show` (`bool`): If True, the labels are shown; if False, they are hidden.

```python
scale_0.set_label_show(True)
```
### `set_mode(show_mode)`

        Set the display mode of the scale.

        - Parameter `show_mode` (`int`): The display mode.

            Optional:

                - `lv.scale.MODE.HORIZONTAL_TOP`: Horizontal top scale.
                - `lv.scale.MODE.HORIZONTAL_BOTTOM`: Horizontal bottom scale.
                - `lv.scale.MODE.VERTICAL_LEFT`: Vertical left scale.
                - `lv.scale.MODE.VERTICAL_RIGHT`: Vertical right scale.
                - `lv.scale.MODE.ROUND_INNER`: Round inner scale.
                - `lv.scale.MODE.ROUND_OUTER`: Round outer scale.

```python
scale_0.set_mode(lv.SCALE.MODE.HORIZONTAL_TOP)
```
### `set_text_src(text_src)`

        Set the source of the scale label text.

        - Parameter `text_src` (`list`): The source of the scale label text.

```python
scale_0.set_text_src(["0", "10", "20", "30", "40", "50", "60", "70", "80", "90", "100", None])
```
### `set_line_color(color, opa, part)`

        Set the color of the line.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).

```python
scale_0.set_line_color(0xFF0000, 255, lv.PART.MAIN)
scale_0.set_line_color(0x00FF00, 255, lv.PART.ITEMS)
scale_0.set_line_color(0x0000FF, 255, lv.PART.INDICATOR)
```
### `set_style_line_width(width, part)`

        Set the line width of the scale.

        - Parameter `width` (`int`): The line width to set.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).

```python
scale_0.set_style_line_width(2, lv.PART.MAIN)
scale_0.set_style_line_width(2, lv.PART.ITEMS)
scale_0.set_style_line_width(2, lv.PART.INDICATOR)
```
### `set_text_color(color, opa, part)`

        Set the color of the text.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color.
        - Parameter `part` (`int`): The part of the object to apply the style to lv.PART.INDICATOR.

```python
scale_0.set_text_color(0xFF0000, 255, lv.PART.INDICATOR)
```
### `set_style_text_font(font, part)`

        Set the font of the scale label text.

        - Parameter `font` (`lv.lv_font_t`): The font to set.
        - Parameter `part` (`int`): The part of the object to apply the style to lv.PART.INDICATOR.

```python
scale_0.set_style_text_font(lv.font_montserrat_14, lv.PART.INDICATOR)
```
### `set_pos(x, y)`

        Set the position of the scale.

        - Parameter `x` (`int`): The x-coordinate of the scale.
        - Parameter `y` (`int`): The y-coordinate of the scale.

```python
scale_0.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the scale.

        - Parameter `x` (`int`): The x-coordinate of the scale.

```python
scale_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the scale.

        - Parameter `y` (`int`): The y-coordinate of the scale.

```python
scale_0.set_y(100)
```
### `set_size(width, height)`

        Set the size of the scale.

        - Parameter `width` (`int`): The width of the scale.
        - Parameter `height` (`int`): The height of the scale.

```python
scale_0.set_size(100, 50)
```
### `set_width(width)`

        Set the width of the scale.

        - Parameter `width` (`int`): The width of the scale.

```python
scale_0.set_width(100)
```
### `set_height(height)`

        Set the height of the scale.

        - Parameter `height` (`int`): The height of the scale.

```python
scale_0.set_height(50)
```
### `align_to(obj, align, x, y)`

        Align the scale to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.

```python
scale_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
```
