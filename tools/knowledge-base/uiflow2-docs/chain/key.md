# Chain Key

<!-- .. include:: ../refs/chain.key.ref -->

Chain Key is a key module that can be connected to the M5Chain series devices. This module provides functions to read the key states.

Support the following products:

    |Chain Key|

## UiFlow2 Example

#### USB Keyboard

Open the |chain_key_usb_keyboard_example.m5f2| project in UiFlow2.

This example demonstrates how to use the Chain Key as a USB keyboard.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### USB Keyboard

This example demonstrates how to use the Chain Key as a USB keyboard.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import KeyChain
from chain import ChainBus
from usb.device.keyboard import Keyboard
from usb.device.hid import KeyCode

bus2 = None
keyboard = None
chain_key_0 = None

key_press = None

def chain_key_0_click_event(args):
    global bus2, keyboard, chain_key_0, key_press
    key_press = True

def setup():
    global bus2, keyboard, chain_key_0, key_press

    M5.begin()
    bus2 = ChainBus(2, tx=6, rx=5)
    keyboard = Keyboard()
    chain_key_0 = KeyChain(bus2, 1)
    chain_key_0.set_click_callback(chain_key_0_click_event)
    key_press = False

def loop():
    global bus2, keyboard, chain_key_0, key_press
    M5.update()
    if keyboard.is_open():
        if key_press:
            keyboard.input(KeyCode.A)
            key_press = False

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None

## **API**

#### KeyChain

## KeyChain
Create a KeyChain object.

:param ChainBus bus: ChainBus object.
:param int device_id: Device ID.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from chain import ChainBus
        from chain import KeyChain

        chainbus_0 = ChainBus(2, 32, 33, verbose=True)
        keychain_0 = KeyChain(chainbus_0, 1)

### `get_button_state`
get button state.

:return: Button state, True if pressed, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        keychain_0.get_button_state()

### `set_click_callback`
set button click callback.

:param callback: Callback function.

.. note::
    Chain related methods cannot be called in the callback function.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        def keychain_0_click_callback(args):
            print("click")

        keychain_0.set_click_callback(keychain_0_click_callback)

### `set_double_click_callback`
set button double click callback.

:param callback: Callback function.

.. note::
    Chain related methods cannot be called in the callback function.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        def keychain_0_double_click_callback(args):
            print("double click")

        keychain_0.set_double_click_callback(keychain_0_double_click_callback)

### `set_long_press_callback`
set button long press callback.

:param callback: Callback function.

.. note::
    Chain related methods cannot be called in the callback function.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        def keychain_0_long_press_callback(args):
            print("long press")

        keychain_0.set_long_press_callback(keychain_0_long_press_callback)

### `set_button_double_click_trigger_interval`
set button double click trigger interval.

:param int interval_ms: Interval time in milliseconds. range: 100-1000
:return: True if success, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        keychain_0.set_button_double_click_trigger_interval(100)

### `set_button_long_press_trigger_interval`
set button long press trigger interval.

:param int interval_ms: Interval time in milliseconds. range: 3000-30000
:return: True if success, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        keychain_0.set_button_long_press_trigger_interval(3000)

### `get_button_double_click_trigger_interval`
get button double click trigger interval.

:return: Interval time in milliseconds.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        interval = keychain_0.get_button_double_click_trigger_interval()

### `get_button_long_press_trigger_interval`
get button long press trigger interval.

:return: Interval time in milliseconds.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        interval = keychain_0.get_button_long_press_trigger_interval()

### `set_button_mode`
set button mode.

:param int mode: Button mode. Use :attr:`KeyChain.MODE_POLL` or :attr:`KeyChain.MODE_EVENT`.
:return: True if success, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        keychain_0.set_button_mode(KeyChain.MODE_EVENT)

### `get_button_mode`
get button mode.

:return: Button mode. :attr:`KeyChain.MODE_POLL` or :attr:`KeyChain.MODE_EVENT`.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        mode = keychain_0.get_button_mode()

### `set_rgb_color`
set RGB color.

:param int color: RGB color value.
:return: True if success, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        keychain_0.set_rgb_color(0xFF0000)

### `get_rgb_color`
get RGB color.

:param index: Index of the RGB LED.
:return: RGB color value.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        color = keychain_0.get_rgb_color()

### `set_rgb_brightness`
set RGB brightness.

:param int brightness: Brightness value (0-100).
:param bool save: Whether to save the brightness setting to flash.
:return: True if success, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        keychain_0.set_rgb_brightness(80)

### `get_rgb_brightness`
get RGB brightness.

:return: Brightness value (0-100).
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        brightness = keychain_0.get_rgb_brightness()

### `get_bootloader_version`
get bootloader version.

:return: Bootloader version.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        version = keychain_0.get_bootloader_version()

### `get_firmware_version`
get firmware version.

:return: Firmware version.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        version = keychain_0.get_firmware_version()

### `get_device_type`
get device type.

:return: Device type. Returns -1 if failed.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        device_type = keychain_0.get_device_type()

### `get_device_uid`
get device UID.

:param int uid_type: UID type, 0 for 4-byte UID, 1 for 12-byte UID.
:return: Tuple of UID bytes (4 bytes or 12 bytes). Returns empty tuple on error.
:rtype: tuple

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        uid = keychain_0.get_device_uid(0)  # 4-byte UID
        uid = keychain_0.get_device_uid(1)  # 12-byte UID
