# Chain RGB

RGBChain is the helper class for Chain RGB display devices on the Chain bus. It
provides methods to control an 8 x 8 RGB display using RGB888 integer color values,
including pixel drawing, full-screen buffer refresh, ASCII character display,
scrolling text, brightness, and rotation.

Support the following products:

    Chain RGB

## Constants

Display modes use `RGBChain.MODE_PIXEL` and `RGBChain.MODE_SCROLL`.

Scroll directions use `RGBChain.SCROLL_DIR_LEFT`,
`RGBChain.SCROLL_DIR_RIGHT`, `RGBChain.SCROLL_DIR_UP`, and
`RGBChain.SCROLL_DIR_DOWN`.

Scroll modes use `RGBChain.SCROLL_MODE_ONCE`, `RGBChain.SCROLL_MODE_LOOP`,
and `RGBChain.SCROLL_MODE_BOUNCE`.

Scroll states use `RGBChain.SCROLL_STATE_START`,
`RGBChain.SCROLL_STATE_PAUSE`, and `RGBChain.SCROLL_STATE_RESET`.

Display rotation uses `RGBChain.ROTATION_0`, `RGBChain.ROTATION_90`,
`RGBChain.ROTATION_180`, and `RGBChain.ROTATION_270`.

## MicroPython Examples

#### Scroll text, rotation, and brightness control

This example initializes Chain RGB in scroll mode and displays the text
`M5STACK` in cyan. It also shows a simple controller UI on the host display and
uses the hardware buttons to control the Chain RGB module:

- `BtnA` toggles the scroll state between start and pause.
- `BtnB` cycles the display rotation through 0, 90, 180, and 270 degrees.
- `BtnC` cycles the display brightness level.

```python
import os, sys, io
import M5
from M5 import *
from chain import ChainBus
from chain import RGBChain

label_title = None
label_text = None
label_state = None
label_rotation = None
label_direction = None
bus2 = None
chain_rgb_0 = None
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
        chain_rgb_0, \
        scroll_state, \
        display_rotation, \
        brightness
    scroll_state = (scroll_state if isinstance(scroll_state, (int, float)) else 0) + 1
    if scroll_state >= 2:
        scroll_state = 0
    chain_rgb_0.set_scroll_state(scroll_state)

def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_text, \
        label_state, \
        label_rotation, \
        label_direction, \
        bus2, \
        chain_rgb_0, \
        scroll_state, \
        display_rotation, \
        brightness
    display_rotation = (display_rotation if isinstance(display_rotation, (int, float)) else 0) + 1
    if display_rotation >= 4:
        display_rotation = 0
    chain_rgb_0.set_display_rotation(display_rotation, save=False)

def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_text, \
        label_state, \
        label_rotation, \
        label_direction, \
        bus2, \
        chain_rgb_0, \
        scroll_state, \
        display_rotation, \
        brightness
    brightness = (brightness if isinstance(brightness, (int, float)) else 0) + 10
    if brightness >= 50:
        brightness = 0
    chain_rgb_0.set_brightness(brightness, save=False)

def setup():
    global \
        label_title, \
        label_text, \
        label_state, \
        label_rotation, \
        label_direction, \
        bus2, \
        chain_rgb_0, \
        scroll_state, \
        display_rotation, \
        brightness

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "Chain RGB Control", 45, 11, 1.0, 0x0F92E8, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_text = Widgets.Label(
        "M5STACK", 62, 80, 1.0, 0x17E6CF, 0x000000, Widgets.FONTS.Montserrat40
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
    chain_rgb_0 = RGBChain(bus2, 1)
    chain_rgb_0.set_display_mode(RGBChain.MODE_SCROLL)
    chain_rgb_0.set_scroll_text(
        "M5STACK", RGBChain.SCROLL_DIR_LEFT, RGBChain.SCROLL_MODE_LOOP, 100, 0x17E6CF
    )
    scroll_state = 0
    brightness = 20
    display_rotation = 0
    chain_rgb_0.set_display_rotation(display_rotation, save=False)
    chain_rgb_0.set_brightness(brightness, save=False)

def loop():
    global \
        label_title, \
        label_text, \
        label_state, \
        label_rotation, \
        label_direction, \
        bus2, \
        chain_rgb_0, \
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

#### RGBChain

## `RGBChain`
RGB Chain class for interacting with 8x8 RGB display devices over Chain bus.

- Parameter `bus` (`ChainBus`): The Chain bus instance.
- Parameter `device_id` (`int`): The device ID of the RGB display on the Chain bus.

```python
from chain import ChainBus
from chain import RGBChain

bus2 = ChainBus(2, tx=21, rx=22)
chain_rgb_0 = RGBChain(bus2, 1)
```

### `rgb888_to_rgb565`
Convert 8-bit RGB channel values to RGB565.

- Parameter `r` (`int`): Red channel, range 0-255.
- Parameter `g` (`int`): Green channel, range 0-255.
- Parameter `b` (`int`): Blue channel, range 0-255.
- Returns: RGB565 color value.
- Return type: int

```python
color = RGBChain.rgb888_to_rgb565(255, 0, 0)
```

### `color888_to_rgb565`
Convert a 0xRRGGBB color value to RGB565.

- Parameter `color` (`int`): 24-bit RGB color value in 0xRRGGBB format.
- Returns: RGB565 color value.
- Return type: int

```python
color = RGBChain.color888_to_rgb565(0xFF0000)
```

### `rgb565_to_color888`
Convert an RGB565 color value to a 0xRRGGBB color value.

- Parameter `color` (`int`): RGB565 color value.
- Returns: 24-bit RGB color value in 0xRRGGBB format.
- Return type: int

### `set_display_mode`
Set the display mode.

- Parameter `mode` (`int`): Display mode. Use `RGBChain.MODE_PIXEL` (0) for pixel mode or `RGBChain.MODE_SCROLL` (1) for scrolling string mode.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_rgb_0.set_display_mode(RGBChain.MODE_PIXEL)
```

### `get_display_mode`
Get the display mode.

- Returns: Display mode. 0 means pixel mode, 1 means scrolling string mode. Returns None if failed.
- Return type: int

```python
mode = chain_rgb_0.get_display_mode()
```

### `set_pixel`
Set one pixel color on the 8x8 display.

- Parameter `x` (`int`): X coordinate, range 0-7.
- Parameter `y` (`int`): Y coordinate, range 0-7.
- Parameter `color` (`int`): RGB888 color value in `0xRRGGBB` format.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_rgb_0.set_pixel(0, 0, 0xFF0000)
```

### `set_pixels`
Set multiple pixel colors on the 8x8 display.

- Parameter `coordinates`: Iterable of `(x, y, color)` values. Supports 1-64 pixels.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_rgb_0.set_pixels(((0, 0, 0xFF0000), (1, 0, 0x00FF00)))
```

### `get_pixel`
Get one pixel RGB888 color from the 8x8 display.

- Parameter `x` (`int`): X coordinate, range 0-7.
- Parameter `y` (`int`): Y coordinate, range 0-7.
- Returns: RGB888 color value in 0xRRGGBB format, or None if failed.
- Return type: int

```python
color = chain_rgb_0.get_pixel(0, 0)
```

### `get_pixels`
Get multiple pixel RGB888 colors from the 8x8 display.

- Parameter `coordinates`: Iterable of `(x, y)` coordinates. Supports 1-64 pixels.
- Returns: Tuple of RGB888 color values in 0xRRGGBB format, or None if failed.
- Return type: tuple

```python
colors = chain_rgb_0.get_pixels(((0, 0), (1, 0)))
```

### `set_display_buffer`
Refresh the full 8x8 display buffer.

- Parameter `buffer`: 64 RGB888 color values in 0xRRGGBB format, row-major order, left to right and top to bottom.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_rgb_0.set_display_buffer((0xFF0000,) * 64)
```

### `get_display_buffer`
Get the full 64-color RGB888 display buffer.

- Returns: Tuple of 64 RGB888 color values in 0xRRGGBB format, or None if failed.
- Return type: tuple

```python
buffer = chain_rgb_0.get_display_buffer()
```

### `set_matrix`
Refresh the display from an 8x8 color matrix.

- Parameter `matrix`: 8 rows x 8 columns of RGB888 color values in 0xRRGGBB format.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_rgb_0.set_matrix(((0xFF0000,) * 8,) * 8)
```

### `fill`
Fill all 64 pixels with one RGB888 color.

- Parameter `color` (`int`): RGB888 color value in 0xRRGGBB format.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_rgb_0.fill(0x0000FF)
```

### `set_display_char`
Set one ASCII character in pixel mode.

- Parameter `char`: Character or ASCII code in range 32-127.
- Parameter `x_offset` (`int`): X offset, range 0-7.
- Parameter `y_offset` (`int`): Y offset, range 0-7.
- Parameter `color` (`int`): RGB888 color value in 0xRRGGBB format.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_rgb_0.set_display_char("R", 1, 0, 0x00FF00)
```

### `set_scroll_text`
Set the scrolling ASCII text.

- Parameter `text`: ASCII string or bytes to display. Supports ASCII characters 32-127.
- Parameter `direction` (`int`): Scroll direction. Use `RGBChain.SCROLL_DIR_LEFT` (0), `RGBChain.SCROLL_DIR_RIGHT` (1), `RGBChain.SCROLL_DIR_UP` (2), or `RGBChain.SCROLL_DIR_DOWN` (3).
- Parameter `mode` (`int`): Scroll mode. Use `RGBChain.SCROLL_MODE_ONCE` (0), `RGBChain.SCROLL_MODE_LOOP` (1), or `RGBChain.SCROLL_MODE_BOUNCE` (3).
- Parameter `speed` (`int`): Scroll speed in milliseconds per pixel. Range: 0-65535.
- Parameter `color` (`int`): RGB888 text color in 0xRRGGBB format. 0x000000 enables gradient rainbow color for scroll text.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_rgb_0.set_scroll_text("M5Stack", RGBChain.SCROLL_DIR_LEFT, RGBChain.SCROLL_MODE_LOOP, 100, 0x000000)
```

### `set_scroll_state`
Set the scrolling text state.

- Parameter `state` (`int`): Scroll state. Use `RGBChain.SCROLL_STATE_START` (0), `RGBChain.SCROLL_STATE_PAUSE` (1), or `RGBChain.SCROLL_STATE_RESET` (2).
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_rgb_0.set_scroll_state(RGBChain.SCROLL_STATE_START)
```

### `get_scroll_state`
Get the scrolling text state.

- Returns: Scroll state. 0 means scrolling, 1 means paused, 2 means reset/idle. Returns None if failed.
- Return type: int

```python
state = chain_rgb_0.get_scroll_state()
```

### `set_display_rotation`
Set the display rotation.

- Parameter `rotation` (`int`): Display rotation. 0 default, 1 clockwise 90 degrees, 2 clockwise 180 degrees, 3 clockwise 270 degrees.
- Parameter `save` (`bool`): Whether to save the setting to flash.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_rgb_0.set_display_rotation(RGBChain.ROTATION_0, save=False)
```

### `get_display_rotation`
Get the display rotation.

- Returns: Display rotation. 0 default, 1 clockwise 90 degrees, 2 clockwise 180 degrees, 3 clockwise 270 degrees. Returns None if failed.
- Return type: int

```python
rotation = chain_rgb_0.get_display_rotation()
```

### `set_brightness`
Set the screen brightness percentage.

- Parameter `brightness` (`int`): Brightness percentage. Range: 0-100.
- Parameter `save` (`bool`): Whether to save the setting to flash.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_rgb_0.set_brightness(50, save=False)
```

### `get_brightness`
Get the screen brightness percentage.

- Returns: Brightness percentage, range 0-100. Returns None if failed.
- Return type: int

```python
brightness = chain_rgb_0.get_brightness()
```

### `clear_display`
Clear the display.

- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_rgb_0.clear_display()
```

    For general Chain device methods, please refer to the `ChainKey <chain.key.KeyChain>` class.
