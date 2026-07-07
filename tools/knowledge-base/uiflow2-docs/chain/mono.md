# Chain Mono

<!-- .. include:: ../refs/chain.mono.ref -->

MonoChain is the helper class for Chain Mono display devices on the Chain bus. It
provides methods to control an 8 x 8 monochrome display, including pixel drawing,
full-screen buffer refresh, ASCII character display, scrolling text, brightness,
and rotation.

Support the following products:

    |Chain Mono|

## Constants

Display modes use ``MonoChain.MODE_PIXEL`` and ``MonoChain.MODE_SCROLL``.

Scroll directions use ``MonoChain.SCROLL_DIR_LEFT``,
``MonoChain.SCROLL_DIR_RIGHT``, ``MonoChain.SCROLL_DIR_UP``, and
``MonoChain.SCROLL_DIR_DOWN``.

Scroll modes use ``MonoChain.SCROLL_MODE_ONCE``,
``MonoChain.SCROLL_MODE_LOOP``, and ``MonoChain.SCROLL_MODE_BOUNCE``.

Scroll states use ``MonoChain.SCROLL_STATE_START``,
``MonoChain.SCROLL_STATE_PAUSE``, and ``MonoChain.SCROLL_STATE_RESET``.

Display rotation uses ``MonoChain.ROTATION_0``, ``MonoChain.ROTATION_90``,
``MonoChain.ROTATION_180``, and ``MonoChain.ROTATION_270``.

## UiFlow2 Example

#### Scroll text, rotation, and brightness control

Open the |basic_chain_mono_example.m5f2| project in UiFlow2.

This example initializes Chain Mono in scroll mode and displays the text
``M5STACK``. It also shows a simple controller UI on the host display and uses
the hardware buttons to control the Chain Mono module.

- ``BtnA`` toggles the scroll state between start and pause.
- ``BtnB`` cycles the display rotation through 0, 90, 180, and 270 degrees.
- ``BtnC`` cycles the display brightness level.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Examples

#### Scroll text, rotation, and brightness control

This example initializes Chain Mono in scroll mode and displays the text
``M5STACK``. It also shows a simple controller UI on the host display and uses
the hardware buttons to control the Chain Mono module:

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

Example output:

    None

## **API**

#### MonoChain

## MonoChain
Mono Chain class for interacting with 8x8 monochrome display devices over Chain bus.

:param ChainBus bus: The Chain bus instance.
:param int device_id: The device ID of the Mono display on the Chain bus.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from chain import ChainBus
        from chain import MonoChain

        bus2 = ChainBus(2, tx=21, rx=22)
        chain_mono_0 = MonoChain(bus2, 1)

### `set_display_mode`
Set the display mode.

:param int mode: Display mode. Use :attr:`MonoChain.MODE_PIXEL` (0) for pixel mode or :attr:`MonoChain.MODE_SCROLL` (1) for scrolling string mode.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_mono_0.set_display_mode(MonoChain.MODE_PIXEL)

### `get_display_mode`
Get the display mode.

:return: Display mode. 0 means pixel mode, 1 means scrolling string mode. Returns None if failed.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        mode = chain_mono_0.get_display_mode()

### `set_pixel`
Set one pixel state on the 8x8 display.

:param int x: X coordinate, range 0-7.
:param int y: Y coordinate, range 0-7.
:param bool state: Pixel state. True means on, False means off.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_mono_0.set_pixel(0, 0, True)

### `set_pixels`
Set multiple pixel states on the 8x8 display.

:param coordinates: Iterable of ``(x, y, state)`` or ``(x, y)`` values. Supports 1-64 pixels.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_mono_0.set_pixels(((0, 0, True), (1, 0, False)))

### `get_pixel`
Get one pixel state from the 8x8 display.

:param int x: X coordinate, range 0-7.
:param int y: Y coordinate, range 0-7.
:return: Pixel state. True means on, False means off. Returns None if failed.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        state = chain_mono_0.get_pixel(0, 0)

### `get_pixels`
Get multiple pixel states from the 8x8 display.

:param coordinates: Iterable of ``(x, y)`` coordinates. Supports 1-64 pixels.
:return: Tuple of 0/1 pixel states, or None if failed.
:rtype: tuple

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        states = chain_mono_0.get_pixels(((0, 0), (1, 0)))

### `set_display_buffer`
Refresh the full 8x8 display buffer.

:param buffer: 8 row bytes. Row 0 is Y=0, bit7 maps to X=0 and bit0 maps to X=7.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_mono_0.set_display_buffer((0xFF, 0x81, 0x81, 0x81, 0x81, 0x81, 0x81, 0xFF))

### `get_display_buffer`
Get the full 8-byte display buffer.

:return: Tuple of 8 row bytes, or None if failed.
:rtype: tuple

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        buffer = chain_mono_0.get_display_buffer()

### `set_matrix`
Refresh the display from an 8x8 matrix.

:param matrix: 8 rows of row bytes or boolean/0/1 values.
:return: True if the operation was successful, False otherwise.
:rtype: bool

MicroPython Code Block:

    .. code-block:: python

        success = chain_mono_0.set_matrix(((1, 0, 0, 0, 0, 0, 0, 1),) * 8)

### `set_display_char`
Set one ASCII character in pixel mode.

:param char: Character or ASCII code in range 32-127.
:param int x_offset: X offset, range 0-7.
:param int y_offset: Y offset, range 0-7.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_mono_0.set_display_char("A", 1, 0)

### `set_scroll_text`
Set the scrolling ASCII text.

:param text: ASCII string or bytes to display. Supports ASCII characters 32-127.
:param int direction: Scroll direction. Use :attr:`MonoChain.SCROLL_DIR_RIGHT` (0), :attr:`MonoChain.SCROLL_DIR_LEFT` (1), :attr:`MonoChain.SCROLL_DIR_UP` (2), or :attr:`MonoChain.SCROLL_DIR_DOWN` (3).
:param int mode: Scroll mode. Use :attr:`MonoChain.SCROLL_MODE_ONCE` (0), :attr:`MonoChain.SCROLL_MODE_LOOP` (1), or :attr:`MonoChain.SCROLL_MODE_BOUNCE` (3).
:param int speed: Scroll speed in milliseconds per pixel. Range: 0-65535.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_mono_0.set_scroll_text("M5Stack", MonoChain.SCROLL_DIR_LEFT, MonoChain.SCROLL_MODE_LOOP, 100)

### `set_scroll_state`
Set the scrolling text state.

:param int state: Scroll state. Use :attr:`MonoChain.SCROLL_STATE_START` (0), :attr:`MonoChain.SCROLL_STATE_PAUSE` (1), or :attr:`MonoChain.SCROLL_STATE_RESET` (2).
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_mono_0.set_scroll_state(MonoChain.SCROLL_STATE_START)

### `get_scroll_state`
Get the scrolling text state.

:return: Scroll state. 0 means scrolling, 1 means paused, 2 means reset/idle. Returns None if failed.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        state = chain_mono_0.get_scroll_state()

### `set_display_rotation`
Set the display rotation.

:param int rotation: Display rotation. 0 default, 1 clockwise 90 degrees, 2 clockwise 180 degrees, 3 clockwise 270 degrees.
:param bool save: Whether to save the setting to flash.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_mono_0.set_display_rotation(MonoChain.ROTATION_0, save=False)

### `get_display_rotation`
Get the display rotation.

:return: Display rotation. 0 default, 1 clockwise 90 degrees, 2 clockwise 180 degrees, 3 clockwise 270 degrees. Returns None if failed.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        rotation = chain_mono_0.get_display_rotation()

### `set_brightness`
Set the screen brightness level.

:param int brightness: Brightness level. Range: 0-7.
:param bool save: Whether to save the setting to flash.
:return: True if the operation was successful, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_mono_0.set_brightness(7, save=False)

### `get_brightness`
Get the screen brightness level.

:return: Brightness level, range 0-7. Returns None if failed.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        brightness = chain_mono_0.get_brightness()

### `set_rgb_color`
Set Chain RGB LED color.

Mono display modules do not provide a separate Chain RGB LED, so this method returns False.

:param int color: RGB color value.
:return: Always False.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_mono_0.set_rgb_color(0xFF0000)

### `get_rgb_color`
Get Chain RGB LED color.

Mono display modules do not provide a separate Chain RGB LED, so this method returns -1.

:return: Always -1.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        color = chain_mono_0.get_rgb_color()

### `set_rgb_brightness`
Set Chain RGB LED brightness.

Mono display modules do not provide a separate Chain RGB LED, so this method returns False.

:param int brightness: Brightness value.
:param bool save: Whether to save the setting to flash.
:return: Always False.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = chain_mono_0.set_rgb_brightness(50, save=False)

### `get_rgb_brightness`
Get Chain RGB LED brightness.

Mono display modules do not provide a separate Chain RGB LED, so this method returns -1.

:return: Always -1.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        brightness = chain_mono_0.get_rgb_brightness()

### `clear_display`
Clear the display.

:return: True if the operation was successful, False otherwise.
:rtype: bool

MicroPython Code Block:

    .. code-block:: python

        success = chain_mono_0.clear_display()

    For general Chain device methods, please refer to the :class:`ChainKey <chain.key.KeyChain>` class.
