
# M5Label

M5Label is a widget that can be used to create labels in the user interface. It can display text and can be styled with different fonts, colors, and sizes.

> Important: **Available Fonts**: For `m5ui` widgets, use LVGL fonts such as
> `lv.font_montserrat_12`, `14`, `16`, `18`, `24`, `40`, `44`,
> and `48`. Some builds, such as Tab5, also include `20`, `22`, `30`,
> and `36`. Check with `hasattr(lv, "font_montserrat_20")` before using
> an optional size in cross-board examples. The Alibaba CJK fonts are
> `M5.Lcd.FONTS` fonts for `M5.Lcd` / `M5.Widgets` drawing, not
> `lv.font_montserrat_*` objects.
## MicroPython Example

#### scroll label

This example demonstrates how to create a label that scrolls text in a circular manner.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None
label0 = None

def setup():
    global page0, label0

    M5.begin()
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label0 = m5ui.M5Label(
        "It is a circularly scrolling text. ",
        x=60,
        y=110,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    page0.screen_load()
    label0.set_long_mode(lv.label.LONG_MODE.SCROLL_CIRCULAR)
    label0.set_width(150)
    label0.align_to(page0, lv.ALIGN.CENTER, 0, 0)

def loop():
    global page0, label0
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

#### M5Label

> Note: Unlike `M5Button` and `M5Chart`, the `M5Label` constructor does
> **not** accept `w` or `h` parameters. Label size is determined
> automatically by its text content. To explicitly set a label's width,
> call `label.set_width(150)` after creation.
## `M5Label`
Create a label object.

- Parameter `text` (`str`): The text to display on the label.
- Parameter `x` (`int`): The x position of the label.
- Parameter `y` (`int`): The y position of the label.
- Parameter `text_c` (`int`): The text color of the label in hexadecimal format.
- Parameter `bg_c` (`int`): The background color of the label in hexadecimal format.
- Parameter `bg_opa` (`int`): The background opacity of the label (0-255).
- Parameter `font` (`lv.lv_font_t`): The font to use for the button text.
- Parameter `parent` (`lv.obj`): The parent object to attach the button to. If not specified, the button will be attached to the default screen.

    None

```python
from m5ui import M5Label
import lvgl as lv

m5ui.init()
label_0 = M5Label(text="Hello, World!", x=10, y=10, text_c=0x212121, bg_c=0xFFFFFF, bg_opa=0, font=lv.font_montserrat_14, parent=page0)
```

### `set_shadow`
Set a shadow for the label.

- Parameter `color` (`int`): The color of the shadow in hexadecimal format or an integer.
- Parameter `opa` (`int`): The opacity of the shadow (0-255).
- Parameter `align` (`int`): The alignment of the shadow relative to the label.
- Parameter `offset_x` (`int`): The horizontal offset of the shadow.
- Parameter `offset_y` (`int`): The vertical offset of the shadow.
- Returns: None

```python
label_0.set_shadow(color=0x000000, opa=128, align=lv.ALIGN.BOTTOM_RIGHT, offset_x=5, offset_y=5)
```

### `unset_shadow`
Remove the shadow from the label.

```python
label_0.unset_shadow()
```

### `set_style_radius`

### `set_size`

### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.
        - Returns: None

```python
label_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `toggle_flag(flag)`

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        - Parameter `flag` (`int`): The flag to toggle.
        - Returns: None

```python
label_0.toggle_flag(lv.obj.FLAG.HIDDEN)
```
### `set_state(state, value)`

        Set the state of the label. If `value` is True, the state is set; if False, the state is unset.

        - Parameter `state` (`int`): The state to set.
        - Parameter `value` (`bool`): If True, the state is set; if False, the state is unset.
        - Returns: None

```python
label_0.set_state(lv.STATE.PRESSED, True)
```
### `toggle_state(state)`

        Toggle the state of the label. If the state is set, it is unset; if not set, it is set.

        - Parameter `state` (`int`): The state to toggle.
        - Returns: None

```python
label_0.toggle_state(lv.STATE.PRESSED)
```
### `set_style_text_font(font, part)`

        Set the font of the label text.

        - Parameter `font` (`lv.lv_font_t`): The font to set.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
label_0.set_style_text_font(lv.font_montserrat_14, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_text_color(color, opa, part)`

        Set the color of the text.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
label_0.set_text_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_bg_color(color, opa, part)`

        Set the background color of the label.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
label_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `set_pos(x, y)`

        Set the position of the label.

        - Parameter `x` (`int`): The x-coordinate of the label.
        - Parameter `y` (`int`): The y-coordinate of the label.
        - Returns: None

```python
label_0.set_pos(100, 100)
```
### `set_x(x)`

        Set the x-coordinate of the label.

        - Parameter `x` (`int`): The x-coordinate of the label.
        - Returns: None

```python
label_0.set_x(100)
```
### `set_y(y)`

        Set the y-coordinate of the label.

        - Parameter `y` (`int`): The y-coordinate of the label.
        - Returns: None

```python
label_0.set_y(100)
```
### `set_size(width, height)`

        Set the size of the label.

        - Parameter `width` (`int`): The width of the label.
        - Parameter `height` (`int`): The height of the label.
        - Returns: None

```python
label_0.set_size(100, 50)
```
### `set_width(width)`

        Set the width of the label.

        - Parameter `width` (`int`): The width of the label.
        - Returns: None

```python
label_0.set_width(100)
```
### `get_width()`

        Get the width of the label.

        - Returns: The width of the label.
        - Return type: int

```python
label_0.get_width()
```
### `align_to(obj, align, x, y)`

        Align the label to another object.

        - Parameter `obj` (`lv.obj`): The object to align to.
        - Parameter `align` (`int`): The alignment type.
        - Parameter `x` (`int`): The x-offset from the aligned object.
        - Parameter `y` (`int`): The y-offset from the aligned object.
        - Returns: None

```python
label_0.align_to(page_0, lv.ALIGN.CENTER, 0, 0)
```
