# Chain Mono

MonoChain is the helper class for Chain Mono display devices on the Chain bus. It
provides methods to control an 8 x 8 monochrome display, including pixel drawing,
full-screen buffer refresh, ASCII character display, scrolling text, brightness,
and rotation.

Support the following products:

    Chain Mono

## Constants

Display modes use `MonoChain.MODE_PIXEL` and `MonoChain.MODE_SCROLL`.

Scroll directions use `MonoChain.SCROLL_DIR_LEFT`,
`MonoChain.SCROLL_DIR_RIGHT`, `MonoChain.SCROLL_DIR_UP`, and
`MonoChain.SCROLL_DIR_DOWN`.

Scroll modes use `MonoChain.SCROLL_MODE_ONCE`,
`MonoChain.SCROLL_MODE_LOOP`, and `MonoChain.SCROLL_MODE_BOUNCE`.

Scroll states use `MonoChain.SCROLL_STATE_START`,
`MonoChain.SCROLL_STATE_PAUSE`, and `MonoChain.SCROLL_STATE_RESET`.

Display rotation uses `MonoChain.ROTATION_0`, `MonoChain.ROTATION_90`,
`MonoChain.ROTATION_180`, and `MonoChain.ROTATION_270`.

## MicroPython Examples

#### Scroll text, rotation, and brightness control

This example initializes Chain Mono in scroll mode and displays the text
`M5STACK`. It also shows a simple controller UI on the host display and uses
the hardware buttons to control the Chain Mono module:

- `BtnA` toggles the scroll state between start and pause.
- `BtnB` cycles the display rotation through 0, 90, 180, and 270 degrees.
- `BtnC` cycles the display brightness level.

```python
import os, sys, io
import M5
from M5 import *
from chain import ChainBus
from chain import MonoChain

label_title = None
label_text = None
label_state = None
label_rotation = None
label_direction = None
bus2 = None
chain_mono_0 = None
scroll_state = None
display_rotation = None
brightness = None

def btna_was_clicked_event(state):
    global \
        label_title, \
        label_text, \
        label_state, \
        label_rotation, \
        label_direction, \
        bus2, \
        chain_mono_0, \
        scroll_state, \
        display_rotation, \
        brightness
    scroll_state = (scroll_state if isinstance(scroll_state, (int, float)) else 0) + 1
    if scroll_state >= 2:
        scroll_state = 0
    chain_mono_0.set_scroll_state(scroll_state)

def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_text, \
        label_state, \
        label_rotation, \
        label_direction, \
        bus2, \
        chain_mono_0, \
        scroll_state, \
        display_rotation, \
        brightness
    display_rotation = (display_rotation if isinstance(display_rotation, (int, float)) else 0) + 1
    if display_rotation >= 4:
        display_rotation = 0
    chain_mono_0.set_display_rotation(display_rotation, save=False)

def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_text, \
        label_state, \
        label_rotation, \
        label_direction, \
        bus2, \
        chain_mono_0, \
        scroll_state, \
        display_rotation, \
        brightness
    brightness = (brightness if isinstance(brightness, (int, float)) else 0) + 1
    if brightness >= 7:
        brightness = 0
    chain_mono_0.set_brightness(brightness, save=False)

def setup():
    global \
        label_title, \
        label_text, \
        label_state, \
        label_rotation, \
        label_direction, \
        bus2, \
        chain_mono_0, \
        scroll_state, \
        display_rotation, \
        brightness

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "Chain Mono Control", 37, 11, 1.0, 0x0F92E8, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_text = Widgets.Label(
        "M5STACK", 62, 80, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat40
    )
    label_state = Widgets.Label(
        "state", 40, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_rotation = Widgets.Label(
        "brighness", 204, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_direction = Widgets.Label(
        "rotation", 118, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    bus2 = ChainBus(2, tx=21, rx=22)
    chain_mono_0 = MonoChain(bus2, 1)
    chain_mono_0.set_display_mode(MonoChain.MODE_SCROLL)
    chain_mono_0.set_display_rotation(MonoChain.ROTATION_0, save=True)
    chain_mono_0.set_scroll_text(
        "M5STACK", MonoChain.SCROLL_DIR_RIGHT, MonoChain.SCROLL_MODE_LOOP, 100
    )
    scroll_state = 0
    brightness = 5
    display_rotation = 0
    chain_mono_0.set_brightness(brightness, save=False)
    chain_mono_0.set_display_rotation(display_rotation, save=True)

def loop():
    global \
        label_title, \
        label_text, \
        label_state, \
        label_rotation, \
        label_direction, \
        bus2, \
        chain_mono_0, \
        scroll_state, \
        display_rotation, \
        brightness
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

## **API**

#### MonoChain

## `MonoChain`
Mono Chain class for interacting with 8x8 monochrome display devices over Chain bus.

- Parameter `bus` (`ChainBus`): The Chain bus instance.
- Parameter `device_id` (`int`): The device ID of the Mono display on the Chain bus.

```python
from chain import ChainBus
from chain import MonoChain

bus2 = ChainBus(2, tx=21, rx=22)
chain_mono_0 = MonoChain(bus2, 1)
```

### `set_display_mode`
Set the display mode.

- Parameter `mode` (`int`): Display mode. Use `MonoChain.MODE_PIXEL` (0) for pixel mode or `MonoChain.MODE_SCROLL` (1) for scrolling string mode.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_mono_0.set_display_mode(MonoChain.MODE_PIXEL)
```

### `get_display_mode`
Get the display mode.

- Returns: Display mode. 0 means pixel mode, 1 means scrolling string mode. Returns None if failed.
- Return type: int

```python
mode = chain_mono_0.get_display_mode()
```

### `set_pixel`
Set one pixel state on the 8x8 display.

- Parameter `x` (`int`): X coordinate, range 0-7.
- Parameter `y` (`int`): Y coordinate, range 0-7.
- Parameter `state` (`bool`): Pixel state. True means on, False means off.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_mono_0.set_pixel(0, 0, True)
```

### `set_pixels`
Set multiple pixel states on the 8x8 display.

- Parameter `coordinates`: Iterable of `(x, y, state)` or `(x, y)` values. Supports 1-64 pixels.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_mono_0.set_pixels(((0, 0, True), (1, 0, False)))
```

### `get_pixel`
Get one pixel state from the 8x8 display.

- Parameter `x` (`int`): X coordinate, range 0-7.
- Parameter `y` (`int`): Y coordinate, range 0-7.
- Returns: Pixel state. True means on, False means off. Returns None if failed.
- Return type: bool

```python
state = chain_mono_0.get_pixel(0, 0)
```

### `get_pixels`
Get multiple pixel states from the 8x8 display.

- Parameter `coordinates`: Iterable of `(x, y)` coordinates. Supports 1-64 pixels.
- Returns: Tuple of 0/1 pixel states, or None if failed.
- Return type: tuple

```python
states = chain_mono_0.get_pixels(((0, 0), (1, 0)))
```

### `set_display_buffer`
Refresh the full 8x8 display buffer.

- Parameter `buffer`: 8 row bytes. Row 0 is Y=0, bit7 maps to X=0 and bit0 maps to X=7.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_mono_0.set_display_buffer((0xFF, 0x81, 0x81, 0x81, 0x81, 0x81, 0x81, 0xFF))
```

### `get_display_buffer`
Get the full 8-byte display buffer.

- Returns: Tuple of 8 row bytes, or None if failed.
- Return type: tuple

```python
buffer = chain_mono_0.get_display_buffer()
```

### `set_matrix`
Refresh the display from an 8x8 matrix.

- Parameter `matrix`: 8 rows of row bytes or boolean/0/1 values.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_mono_0.set_matrix(((1, 0, 0, 0, 0, 0, 0, 1),) * 8)
```

### `set_display_char`
Set one ASCII character in pixel mode.

- Parameter `char`: Character or ASCII code in range 32-127.
- Parameter `x_offset` (`int`): X offset, range 0-7.
- Parameter `y_offset` (`int`): Y offset, range 0-7.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_mono_0.set_display_char("A", 1, 0)
```

### `set_scroll_text`
Set the scrolling ASCII text.

- Parameter `text`: ASCII string or bytes to display. Supports ASCII characters 32-127.
- Parameter `direction` (`int`): Scroll direction. Use `MonoChain.SCROLL_DIR_RIGHT` (0), `MonoChain.SCROLL_DIR_LEFT` (1), `MonoChain.SCROLL_DIR_UP` (2), or `MonoChain.SCROLL_DIR_DOWN` (3).
- Parameter `mode` (`int`): Scroll mode. Use `MonoChain.SCROLL_MODE_ONCE` (0), `MonoChain.SCROLL_MODE_LOOP` (1), or `MonoChain.SCROLL_MODE_BOUNCE` (3).
- Parameter `speed` (`int`): Scroll speed in milliseconds per pixel. Range: 0-65535.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_mono_0.set_scroll_text("M5Stack", MonoChain.SCROLL_DIR_LEFT, MonoChain.SCROLL_MODE_LOOP, 100)
```

### `set_scroll_state`
Set the scrolling text state.

- Parameter `state` (`int`): Scroll state. Use `MonoChain.SCROLL_STATE_START` (0), `MonoChain.SCROLL_STATE_PAUSE` (1), or `MonoChain.SCROLL_STATE_RESET` (2).
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_mono_0.set_scroll_state(MonoChain.SCROLL_STATE_START)
```

### `get_scroll_state`
Get the scrolling text state.

- Returns: Scroll state. 0 means scrolling, 1 means paused, 2 means reset/idle. Returns None if failed.
- Return type: int

```python
state = chain_mono_0.get_scroll_state()
```

### `set_display_rotation`
Set the display rotation.

- Parameter `rotation` (`int`): Display rotation. 0 default, 1 clockwise 90 degrees, 2 clockwise 180 degrees, 3 clockwise 270 degrees.
- Parameter `save` (`bool`): Whether to save the setting to flash.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_mono_0.set_display_rotation(MonoChain.ROTATION_0, save=False)
```

### `get_display_rotation`
Get the display rotation.

- Returns: Display rotation. 0 default, 1 clockwise 90 degrees, 2 clockwise 180 degrees, 3 clockwise 270 degrees. Returns None if failed.
- Return type: int

```python
rotation = chain_mono_0.get_display_rotation()
```

### `set_brightness`
Set the screen brightness level.

- Parameter `brightness` (`int`): Brightness level. Range: 0-7.
- Parameter `save` (`bool`): Whether to save the setting to flash.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_mono_0.set_brightness(7, save=False)
```

### `get_brightness`
Get the screen brightness level.

- Returns: Brightness level, range 0-7. Returns None if failed.
- Return type: int

```python
brightness = chain_mono_0.get_brightness()
```

### `set_rgb_color`
Set Chain RGB LED color.

Mono display modules do not provide a separate Chain RGB LED, so this method returns False.

- Parameter `color` (`int`): RGB color value.
- Returns: Always False.
- Return type: bool

```python
success = chain_mono_0.set_rgb_color(0xFF0000)
```

### `get_rgb_color`
Get Chain RGB LED color.

Mono display modules do not provide a separate Chain RGB LED, so this method returns -1.

- Returns: Always -1.
- Return type: int

```python
color = chain_mono_0.get_rgb_color()
```

### `set_rgb_brightness`
Set Chain RGB LED brightness.

Mono display modules do not provide a separate Chain RGB LED, so this method returns False.

- Parameter `brightness` (`int`): Brightness value.
- Parameter `save` (`bool`): Whether to save the setting to flash.
- Returns: Always False.
- Return type: bool

```python
success = chain_mono_0.set_rgb_brightness(50, save=False)
```

### `get_rgb_brightness`
Get Chain RGB LED brightness.

Mono display modules do not provide a separate Chain RGB LED, so this method returns -1.

- Returns: Always -1.
- Return type: int

```python
brightness = chain_mono_0.get_rgb_brightness()
```

### `clear_display`
Clear the display.

- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_mono_0.clear_display()
```

    For general Chain device methods, please refer to the `ChainKey <chain.key.KeyChain>` class.
