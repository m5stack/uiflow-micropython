
# M5Page

M5Page is a widget that can be used to create pages in the user interface. It can be used to organize other widgets and provide navigation between different pages.

> Important: All m5ui widgets (`M5Label`, `M5Chart`, `M5Button`, etc.) must be
> created with `parent=page0` (or another `M5Page` instance). If
> `parent` is omitted, the widget is attached to the default screen,
> and calling `page0.screen_load()` will load a blank page without
> those widgets.
>
> Correct order:
>
> 1. `m5ui.init()`
> 2. Create `page0 = M5Page(bg_c=0xFFFFFF)`
> 3. Create widgets with `parent=page0`
> 4. `page0.screen_load()`
## MicroPython Example

#### page event

When you press and hold the screen, the screen background color turns black. When you release the screen, the background color returns to white.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv

page0 = None

def page0_pressed_event(event_struct):
    global page0

    page0.set_bg_color(0x000000, 255, 0)

def page0_released_event(event_struct):
    global page0

    page0.set_bg_color(0xFFFFFF, 255, 0)

def page0_clicked_event(event_struct):
    global page0

    page0.set_bg_color(0x000000, 255, 0)

def page0_long_pressed_event(event_struct):
    global page0

    page0.set_bg_color(0x000000, 255, 0)

def page0_event_handler(event_struct):
    global page0
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        page0_pressed_event(event_struct)
    if event == lv.EVENT.RELEASED and True:
        page0_released_event(event_struct)
    if event == lv.EVENT.CLICKED and True:
        page0_clicked_event(event_struct)
    if event == lv.EVENT.LONG_PRESSED and True:
        page0_long_pressed_event(event_struct)
    return

def setup():
    global page0

    M5.begin()
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)

    page0.add_event_cb(page0_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()

def loop():
    global page0
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

#### M5Button

## `M5Page`
Create a page object.

- Parameter `bg_c` (`int`): The background color of the page in hexadecimal format. Default is 0xFFFFFF (white).

    None

```python
from m5ui import M5Page
import lvgl as lv

m5ui.init()
page_0 = M5Page(bg_c=0xFFFFFF)
```

### `screen_load`
Load the page as the active screen.

```python
page_0.screen_load()
```

### `set_style_radius`

### `set_flag(flag, value)`

        Set a flag on the object. If `value` is True, the flag is added; if False, the flag is removed.

        - Parameter `flag` (`int`): The flag to set.
        - Parameter `value` (`bool`): If True, the flag is added; if False, the flag is removed.
        - Returns: None

```python
page_0.set_flag(lv.obj.FLAG.HIDDEN, True)
```
### `toggle_flag(flag)`

        Toggle a flag on the object. If the flag is set, it is removed; if not set, it is added.

        - Parameter `flag` (`int`): The flag to toggle.
        - Returns: None

```python
page_0.toggle_flag(lv.obj.FLAG.HIDDEN)
```
### `set_state(state, value)`

        Set the state of the page. If `value` is True, the state is set; if False, the state is unset.

        - Parameter `state` (`int`): The state to set.
        - Parameter `value` (`bool`): If True, the state is set; if False, the state is unset.
        - Returns: None

```python
page_0.set_state(lv.STATE.PRESSED, True)
```
### `toggle_state(state)`

        Toggle the state of the page. If the state is set, it is unset; if not set, it is set.

        - Parameter `state` (`int`): The state to toggle.
        - Returns: None

```python
page_0.toggle_state(lv.STATE.PRESSED)
```
### `set_bg_color(color, opa, part)`

        Set the background color of the page.

        - Parameter `color` (`int`): The color to set.
        - Parameter `opa` (`int`): The opacity of the color.
        - Parameter `part` (`int`): The part of the object to apply the style to (e.g., lv.PART.MAIN).
        - Returns: None

```python
page_0.set_bg_color(lv.color_hex(0x000000), 255, lv.PART.MAIN | lv.STATE.DEFAULT)
```
### `add_event_cb(handler, event, user_data)`

        Add an event callback to the page. The callback will be called when the specified event occurs.

        - Parameter `handler` (`function`): The callback function to call.
        - Parameter `event` (`int`): The event to listen for.
        - Parameter `user_data` (`Any`): Optional user data to pass to the callback.
        - Returns: None

```python
def page0_pressed_event(event_struct):
    global page0
    page0.set_bg_color(0x000000, 255, 0)

def page0_released_event(event_struct):
    global page0
    page0.set_bg_color(0xffffff, 255, 0)

def page0_clicked_event(event_struct):
    global page0
    page0.set_bg_color(0x000000, 255, 0)

def page0_event_handler(event_struct):
    global page0
    event = event_struct.code
    if event == lv.EVENT.PRESSED and True:
        page0_pressed_event(event_struct)
    if event == lv.EVENT.RELEASED and True:
        page0_released_event(event_struct)
    if event == lv.EVENT.CLICKED and True:
        page0_clicked_event(event_struct)
    if event == lv.EVENT.LONG_PRESSED and True:
        page0_long_pressed_event(event_struct)
    return

page_0.add_event_cb(page0_event_handler, lv.EVENT.ALL, None)
```
