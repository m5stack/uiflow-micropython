# Tab5 Keyboard

The `Keyboard` class controls the Tab5 keyboard controller over I2C. It supports
character input callbacks, raw key matrix events, keyboard mode configuration,
backlight brightness, RGB LED settings, and I2C address management.

## MicroPython Example

#### keyboard input

This example reads character input from the Tab5 keyboard and appends it to a text area.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from tab5 import Keyboard
from hardware import Pin
from hardware import SoftI2C

page0 = None
textarea0 = None
tab5_keyboard_0 = None

key_char = None

def tab5_keyboard_0_char_pressed_event(kb):
    global page0, textarea0, tab5_keyboard_0, key_char
    key_char = kb
    textarea0.add_text(str(key_char))

def setup():
    global page0, textarea0, tab5_keyboard_0, key_char

    M5.begin()
    Widgets.setRotation(3)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    textarea0 = m5ui.M5TextArea(
        text="textarea0",
        placeholder="Placeholder...",
        x=0,
        y=0,
        w=1280,
        h=720,
        font=lv.font_montserrat_24,
        bg_c=0xFFFFFF,
        border_c=0xE0E0E0,
        text_c=0x212121,
        parent=page0,
    )

    softi2c_0 = SoftI2C(scl=Pin(1), sda=Pin(0), freq=100000)
    tab5_keyboard_0 = Keyboard(softi2c_0, 0x6D)
    tab5_keyboard_0.set_callback(tab5_keyboard_0_char_pressed_event)
    tab5_keyboard_0.set_keyboard_mode(tab5_keyboard_0.MODE_CHAR)
    page0.screen_load()
    textarea0.set_text("")

def loop():
    global page0, textarea0, tab5_keyboard_0, key_char
    M5.update()
    tab5_keyboard_0.tick()

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

#### Keyboard

## `Keyboard`
Create a Tab5 keyboard controller object.

- Parameter `i2c` (`I2C`): The I2C bus the Tab5 keyboard is connected to.
- Parameter `address` (`int`): The I2C address of the keyboard controller. Default is `0x6D`.

```python
from tab5 import Keyboard
from hardware import Pin, SoftI2C

softi2c_0 = SoftI2C(scl=Pin(1), sda=Pin(0), freq=100000)
keyboard = Keyboard(softi2c_0, 0x6D)
```

### `available`
Check whether unread keyboard events are queued.

- Returns: `True` if the controller has pending events.
- Return type: bool

### `set_int_enable`
Enable keyboard interrupt sources.

- Parameter `mask` (`int`): Interrupt mask composed from `INT_NORMAL` and `INT_CHAR`.

### `get_int_status`
Get the current keyboard interrupt status.

- Returns: The latched interrupt status bits.
- Return type: int

### `clear_int`
Clear the current keyboard interrupt status.

### `get_event_count`
Get the number of unread keyboard events.

- Returns: The number of queued events.
- Return type: int

### `set_brightness`
Set the keyboard backlight brightness.

- Parameter `brightness` (`int`): Brightness value in the range `0` to `255`.

```python
keyboard.set_brightness(20)
```

### `get_brightness`
Get the keyboard backlight brightness.

- Returns: The current brightness value.
- Return type: int

```python
keyboard.get_brightness()
```

### `set_keyboard_mode`
Set the keyboard event mode.

- Parameter `mode` (`int`): Event mode such as `MODE_NORMAL` or `MODE_CHAR`.

```python
keyboard.set_keyboard_mode(keyboard.MODE_CHAR)
```

### `get_keyboard_mode`
Get the current keyboard event mode.

- Returns: The current keyboard mode.
- Return type: int

### `set_rgb_mode`
Set the RGB LED control mode.

- Parameter `mode` (`int`): RGB mode such as `RGB_MODE_BOUND` or `RGB_MODE_CUSTOM`.

```python
keyboard.set_rgb_mode(keyboard.RGB_MODE_BOUND)
```

### `get_rgb_mode`
Get the RGB LED control mode.

- Returns: The current RGB mode.
- Return type: int

### `read_key_event`
Read one key matrix event.

- Returns: A tuple of `(row, col, pressed)` or `None` when no event is available.
- Return type: tuple | None

### `get_char_event_length`
Get the byte length of the queued character event.

- Returns: The length of the character payload.
- Return type: int

### `read_char_event`
Read one decoded character event.

- Returns: A tuple of `(modifier, text)` or `None` when no event is available.
- Return type: tuple | None

### `is_pressed`
Check whether the keyboard has pending input.

- Returns: `True` if unread input is available.
- Return type: bool

### `set_callback`
Register the callback used by `tick`.

- Parameter `handler` (`callable`): Callback that receives the keyboard event payload.

```python
def on_keyboard(data):
    print(data)

keyboard.set_callback(on_keyboard)
```

### `tick`
Dispatch one pending keyboard event to the registered callback.

### `set_rgb_color`
Set the color of a keyboard RGB LED.

- Parameter `led_num` (`int`): The LED index to update.
- Parameter `color` (`int`): The 24-bit RGB color value.

```python
keyboard.set_rgb_color(0, 0x6600CC)
```

### `get_rgb_color`
Get the color of a keyboard RGB LED.

- Parameter `led_num` (`int`): The LED index to read.
- Returns: The 24-bit RGB color value.
- Return type: int

```python
keyboard.get_rgb_color(0)
```

### `get_firmware_version`
Get the firmware version of the keyboard controller.

- Returns: The firmware version byte.
- Return type: int

```python
keyboard.get_firmware_version()
```

### `set_i2c_address`
Set a new I2C address for the keyboard controller.

- Parameter `addr` (`int`): The new I2C address. Valid range is `0x08` to `0x77`.
- Returns: The active I2C address after the update.
- Return type: int

```python
keyboard.set_i2c_address(0x6D)
```

### `get_i2c_address`
Get the current I2C address of the keyboard controller.

- Returns: The current I2C address.
- Return type: int

```python
keyboard.get_i2c_address()
```
