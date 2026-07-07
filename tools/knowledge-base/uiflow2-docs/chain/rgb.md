# Chain RGB

<!-- .. include:: ../refs/chain.rgb.ref -->

RGBChain is the helper class for Chain RGB display devices on the Chain bus. It
provides methods to control an 8 x 8 RGB display using RGB888 integer color values,
including pixel drawing, full-screen buffer refresh, ASCII character display,
scrolling text, brightness, and rotation.

Support the following products:

    |Chain RGB|

## Constants

Display modes use ``RGBChain.MODE_PIXEL`` and ``RGBChain.MODE_SCROLL``.

Scroll directions use ``RGBChain.SCROLL_DIR_LEFT``,
``RGBChain.SCROLL_DIR_RIGHT``, ``RGBChain.SCROLL_DIR_UP``, and
``RGBChain.SCROLL_DIR_DOWN``.

Scroll modes use ``RGBChain.SCROLL_MODE_ONCE``, ``RGBChain.SCROLL_MODE_LOOP``,
and ``RGBChain.SCROLL_MODE_BOUNCE``.

Scroll states use ``RGBChain.SCROLL_STATE_START``,
``RGBChain.SCROLL_STATE_PAUSE``, and ``RGBChain.SCROLL_STATE_RESET``.

Display rotation uses ``RGBChain.ROTATION_0``, ``RGBChain.ROTATION_90``,
``RGBChain.ROTATION_180``, and ``RGBChain.ROTATION_270``.

## UiFlow2 Example

#### Scroll text, rotation, and brightness control

Open the |basic_chain_rgb_example.m5f2| project in UiFlow2.

This example initializes Chain RGB in scroll mode and displays the text
``M5STACK`` in cyan. It also shows a simple controller UI on the host display
and uses the hardware buttons to control the Chain RGB module.

- ``BtnA`` toggles the scroll state between start and pause.
- ``BtnB`` cycles the display rotation through 0, 90, 180, and 270 degrees.
- ``BtnC`` cycles the display brightness level.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Examples

#### Scroll text, rotation, and brightness control

This example initializes Chain RGB in scroll mode and displays the text
``M5STACK`` in cyan. It also shows a simple controller UI on the host display and
uses the hardware buttons to control the Chain RGB module:

- ``BtnA`` toggles the scroll state between start and pause.
- ``BtnB`` cycles the display rotation through 0, 90, 180, and 270 degrees.
- ``BtnC`` cycles the display brightness level.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

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

Example output:

    None

## **API**

#### RGBChain

## RGBChain
RGB Chain class for interacting with 8x8 RGB display devices over Chain bus.

:param ChainBus bus: The Chain bus instance.
:param int device_id: The device ID of the RGB display on the Chain bus.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from chain import ChainBus
        from chain import RGBChain

        bus2 = ChainBus(2, tx=21, rx=22)
        chain_rgb_0 = RGBChain(bus2, 1)

### `rgb888_to_rgb565`
Convert 8-bit RGB channel values to RGB565.

:param int r: Red channel, range 0-255.
:param int g: Green channel, range 0-255.
:param int b: Blue channel, range 0-255.
:return: RGB565 color value.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        color = RGBChain.rgb888_to_rgb565(255, 0, 0)

### `color888_to_rgb565`
Convert a 0xRRGGBB color value to RGB565.

:param int color: 24-bit RGB color value in 0xRRGGBB format.
:return: RGB565 color value.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        color = RGBChain.color888_to_rgb565(0xFF0000)

### `rgb565_to_color888`
Convert an RGB565 color value to a 0xRRGGBB color value.

:param int color: RGB565 color value.
:return: 24-bit RGB color value in 0xRRGGBB format.
:rtype: int

### `set_display_mode`
Set the display mode.

:param int mode: Display mode. Use :attr:`RGBChain.MODE_PIXEL` (0) for pixel mode or :attr:`RGBChain.MODE_SCROLL` (1) for scrolling string mode.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_rgb_0.set_display_mode(RGBChain.MODE_PIXEL)

### `get_display_mode`
Get the display mode.

:return: Display mode. 0 means pixel mode, 1 means scrolling string mode. Returns None if failed.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        mode = chain_rgb_0.get_display_mode()

### `set_pixel`
Set one pixel color on the 8x8 display.

:param int x: X coordinate, range 0-7.
:param int y: Y coordinate, range 0-7.
:param int color: RGB888 color value in ``0xRRGGBB`` format.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_rgb_0.set_pixel(0, 0, 0xFF0000)

### `set_pixels`
Set multiple pixel colors on the 8x8 display.

:param coordinates: Iterable of ``(x, y, color)`` values. Supports 1-64 pixels.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_rgb_0.set_pixels(((0, 0, 0xFF0000), (1, 0, 0x00FF00)))

### `get_pixel`
Get one pixel RGB888 color from the 8x8 display.

:param int x: X coordinate, range 0-7.
:param int y: Y coordinate, range 0-7.
:return: RGB888 color value in 0xRRGGBB format, or None if failed.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        color = chain_rgb_0.get_pixel(0, 0)

### `get_pixels`
Get multiple pixel RGB888 colors from the 8x8 display.

:param coordinates: Iterable of ``(x, y)`` coordinates. Supports 1-64 pixels.
:return: Tuple of RGB888 color values in 0xRRGGBB format, or None if failed.
:rtype: tuple

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        colors = chain_rgb_0.get_pixels(((0, 0), (1, 0)))

### `set_display_buffer`
Refresh the full 8x8 display buffer.

:param buffer: 64 RGB888 color values in 0xRRGGBB format, row-major order, left to right and top to bottom.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_rgb_0.set_display_buffer((0xFF0000,) * 64)

### `get_display_buffer`
Get the full 64-color RGB888 display buffer.

:return: Tuple of 64 RGB888 color values in 0xRRGGBB format, or None if failed.
:rtype: tuple

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        buffer = chain_rgb_0.get_display_buffer()

### `set_matrix`
Refresh the display from an 8x8 color matrix.

:param matrix: 8 rows x 8 columns of RGB888 color values in 0xRRGGBB format.
:return: True if the operation was successful, False otherwise.
:rtype: bool

MicroPython Code Block:

    .. code-block:: python

        success = chain_rgb_0.set_matrix(((0xFF0000,) * 8,) * 8)

### `fill`
Fill all 64 pixels with one RGB888 color.

:param int color: RGB888 color value in 0xRRGGBB format.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_rgb_0.fill(0x0000FF)

### `set_display_char`
Set one ASCII character in pixel mode.

:param char: Character or ASCII code in range 32-127.
:param int x_offset: X offset, range 0-7.
:param int y_offset: Y offset, range 0-7.
:param int color: RGB888 color value in 0xRRGGBB format.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_rgb_0.set_display_char("R", 1, 0, 0x00FF00)

### `set_scroll_text`
Set the scrolling ASCII text.

:param text: ASCII string or bytes to display. Supports ASCII characters 32-127.
:param int direction: Scroll direction. Use :attr:`RGBChain.SCROLL_DIR_LEFT` (0), :attr:`RGBChain.SCROLL_DIR_RIGHT` (1), :attr:`RGBChain.SCROLL_DIR_UP` (2), or :attr:`RGBChain.SCROLL_DIR_DOWN` (3).
:param int mode: Scroll mode. Use :attr:`RGBChain.SCROLL_MODE_ONCE` (0), :attr:`RGBChain.SCROLL_MODE_LOOP` (1), or :attr:`RGBChain.SCROLL_MODE_BOUNCE` (3).
:param int speed: Scroll speed in milliseconds per pixel. Range: 0-65535.
:param int color: RGB888 text color in 0xRRGGBB format. 0x000000 enables gradient rainbow color for scroll text.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_rgb_0.set_scroll_text("M5Stack", RGBChain.SCROLL_DIR_LEFT, RGBChain.SCROLL_MODE_LOOP, 100, 0x000000)

### `set_scroll_state`
Set the scrolling text state.

:param int state: Scroll state. Use :attr:`RGBChain.SCROLL_STATE_START` (0), :attr:`RGBChain.SCROLL_STATE_PAUSE` (1), or :attr:`RGBChain.SCROLL_STATE_RESET` (2).
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_rgb_0.set_scroll_state(RGBChain.SCROLL_STATE_START)

### `get_scroll_state`
Get the scrolling text state.

:return: Scroll state. 0 means scrolling, 1 means paused, 2 means reset/idle. Returns None if failed.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        state = chain_rgb_0.get_scroll_state()

### `set_display_rotation`
Set the display rotation.

:param int rotation: Display rotation. 0 default, 1 clockwise 90 degrees, 2 clockwise 180 degrees, 3 clockwise 270 degrees.
:param bool save: Whether to save the setting to flash.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_rgb_0.set_display_rotation(RGBChain.ROTATION_0, save=False)

### `get_display_rotation`
Get the display rotation.

:return: Display rotation. 0 default, 1 clockwise 90 degrees, 2 clockwise 180 degrees, 3 clockwise 270 degrees. Returns None if failed.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        rotation = chain_rgb_0.get_display_rotation()

### `set_brightness`
Set the screen brightness percentage.

:param int brightness: Brightness percentage. Range: 0-100.
:param bool save: Whether to save the setting to flash.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_rgb_0.set_brightness(50, save=False)

### `get_brightness`
Get the screen brightness percentage.

:return: Brightness percentage, range 0-100. Returns None if failed.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        brightness = chain_rgb_0.get_brightness()

### `clear_display`
Clear the display.

:return: True if the operation was successful, False otherwise.
:rtype: bool

MicroPython Code Block:

    .. code-block:: python

        success = chain_rgb_0.clear_display()

    For general Chain device methods, please refer to the :class:`ChainKey <chain.key.KeyChain>` class.
