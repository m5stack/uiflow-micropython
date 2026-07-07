# Tab5 Keyboard

<!-- .. py:currentmodule:: tab5.keyboard -->

<!-- .. include:: ../refs/tab5.keyboard.ref -->

The `Keyboard` class controls the Tab5 keyboard controller over I2C. It supports
character input callbacks, raw key matrix events, keyboard mode configuration,
backlight brightness, RGB LED settings, and I2C address management.

## UiFlow2 Example

#### keyboard input

Open the |tab5_keyboard_example.m5f2| project in UiFlow2.

This example reads character input from the Tab5 keyboard and appends it to a text area.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### keyboard input

This example reads character input from the Tab5 keyboard and appends it to a text area.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

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

Example output:

    None

## **API**

#### Keyboard

## Keyboard
Create a Tab5 keyboard controller object.

:param I2C i2c: The I2C bus the Tab5 keyboard is connected to.
:param int address: The I2C address of the keyboard controller. Default is ``0x6D``.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from tab5 import Keyboard
        from hardware import Pin, SoftI2C

        softi2c_0 = SoftI2C(scl=Pin(1), sda=Pin(0), freq=100000)
        keyboard = Keyboard(softi2c_0, 0x6D)

### `available`
Check whether unread keyboard events are queued.

:returns: ``True`` if the controller has pending events.
:rtype: bool

### `set_int_enable`
Enable keyboard interrupt sources.

:param int mask: Interrupt mask composed from ``INT_NORMAL`` and ``INT_CHAR``.

### `get_int_status`
Get the current keyboard interrupt status.

:returns: The latched interrupt status bits.
:rtype: int

### `clear_int`
Clear the current keyboard interrupt status.

### `get_event_count`
Get the number of unread keyboard events.

:returns: The number of queued events.
:rtype: int

### `set_brightness`
Set the keyboard backlight brightness.

:param int brightness: Brightness value in the range ``0`` to ``255``.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        keyboard.set_brightness(20)

### `get_brightness`
Get the keyboard backlight brightness.

:returns: The current brightness value.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        keyboard.get_brightness()

### `set_keyboard_mode`
Set the keyboard event mode.

:param int mode: Event mode such as ``MODE_NORMAL`` or ``MODE_CHAR``.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        keyboard.set_keyboard_mode(keyboard.MODE_CHAR)

### `get_keyboard_mode`
Get the current keyboard event mode.

:returns: The current keyboard mode.
:rtype: int

### `set_rgb_mode`
Set the RGB LED control mode.

:param int mode: RGB mode such as ``RGB_MODE_BOUND`` or ``RGB_MODE_CUSTOM``.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        keyboard.set_rgb_mode(keyboard.RGB_MODE_BOUND)

### `get_rgb_mode`
Get the RGB LED control mode.

:returns: The current RGB mode.
:rtype: int

### `read_key_event`
Read one key matrix event.

:returns: A tuple of ``(row, col, pressed)`` or ``None`` when no event is available.
:rtype: tuple | None

### `get_char_event_length`
Get the byte length of the queued character event.

:returns: The length of the character payload.
:rtype: int

### `read_char_event`
Read one decoded character event.

:returns: A tuple of ``(modifier, text)`` or ``None`` when no event is available.
:rtype: tuple | None

### `is_pressed`
Check whether the keyboard has pending input.

:returns: ``True`` if unread input is available.
:rtype: bool

### `set_callback`
Register the callback used by :meth:`tick`.

:param callable handler: Callback that receives the keyboard event payload.

MicroPython Code Block:

    .. code-block:: python

        def on_keyboard(data):
            print(data)

        keyboard.set_callback(on_keyboard)

### `tick`
Dispatch one pending keyboard event to the registered callback.

### `set_rgb_color`
Set the color of a keyboard RGB LED.

:param int led_num: The LED index to update.
:param int color: The 24-bit RGB color value.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        keyboard.set_rgb_color(0, 0x6600CC)

### `get_rgb_color`
Get the color of a keyboard RGB LED.

:param int led_num: The LED index to read.
:returns: The 24-bit RGB color value.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        keyboard.get_rgb_color(0)

### `get_firmware_version`
Get the firmware version of the keyboard controller.

:returns: The firmware version byte.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        keyboard.get_firmware_version()

### `set_i2c_address`
Set a new I2C address for the keyboard controller.

:param int addr: The new I2C address. Valid range is ``0x08`` to ``0x77``.
:returns: The active I2C address after the update.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        keyboard.set_i2c_address(0x6D)

### `get_i2c_address`
Get the current I2C address of the keyboard controller.

:returns: The current I2C address.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        keyboard.get_i2c_address()
