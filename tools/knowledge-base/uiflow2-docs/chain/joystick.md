# Chain Joystick

<!-- .. include:: ../refs/chain.joystick.ref -->

Chain Joystick is a joystick module that can be connected to the M5Chain series devices. This module provides functions to read the joystick position and button states.

Support the following products:

    |Chain Joystick|

## UiFlow2 Example

#### USB Mouse

Open the |chain_joystick_usb_mouse_example.m5f2| project in UiFlow2.

This example demonstrates how to use the Chain Joystick as a USB mouse.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### USB Mouse

This example demonstrates how to use the Chain Joystick as a USB mouse.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import JoystickChain
from chain import ChainBus
from usb.device.mouse import Mouse
import m5utils

bus2 = None
mouse = None
chain_joystick_0 = None

key_press = None
x = None
y = None

def chain_joystick_0_click_event(args):
    global bus2, mouse, chain_joystick_0, key_press, x, y
    key_press = True

def setup():
    global bus2, mouse, chain_joystick_0, key_press, x, y

    M5.begin()
    bus2 = ChainBus(2, tx=6, rx=5)
    chain_joystick_0 = JoystickChain(bus2, 1)
    chain_joystick_0.set_click_callback(chain_joystick_0_click_event)
    print(chain_joystick_0.get_firmware_version())
    mouse = Mouse()
    key_press = False

def loop():
    global bus2, mouse, chain_joystick_0, key_press, x, y
    M5.update()
    if mouse.is_open():
        x = int(m5utils.remap(chain_joystick_0.get_x(), -128, 127, -64, 64))
        y = int(m5utils.remap(chain_joystick_0.get_y(), -128, 127, 64, -64))
        mouse.move(x, y)
        if key_press:
            mouse.click_left(True)
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

#### JoystickChain

## JoystickChain
Joystick Chain class for interacting with joystick devices over Chain bus.

:param ChainBus bus: The Chain bus instance.
:param int device_id: The device ID of the joystick on the Chain bus.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from chain import ChainBus
        from chain import JoystickChain

        chainbus_0 = ChainBus(2, 32, 33, verbose=True)
        joystick_0 = JoystickChain(chainbus_0, 1)

### `get_x`
Get the X position of the joystick.

:return: X position (-128 to 127).
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        x = joystick_0.get_x()

### `get_y`
Get the Y position of the joystick.

:return: Y position (-128 to 127).
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        y = joystick_0.get_y()

### `get_x_16bit`
Get the X position of the joystick in 16-bit resolution.

:return: X position (-4095 to 4095).
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        x = joystick_0.get_x_16bit()

### `get_y_16bit`
Get the Y position of the joystick in 16-bit resolution.

:return: Y position (-4095 to 4095).
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        y = joystick_0.get_y_16bit()

### `get_x_raw`
Get the raw X ADC value of the joystick.

:return: Raw X ADC value (0-255).
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        x = joystick_0.get_x_raw()

### `get_y_raw`
Get the raw Y ADC value of the joystick.

:return: Raw Y ADC value (0-255).
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        y = joystick_0.get_y_raw()

### `get_x_16bit_raw`
Get the raw X ADC value of the joystick in 16-bit resolution.

:return: Raw X ADC value (0-65535).
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        x = joystick_0.get_x_16bit_raw()

### `get_y_16bit_raw`
Get the raw Y ADC value of the joystick in 16-bit resolution.

:return: Raw Y ADC value (0-65535).
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        y = joystick_0.get_y_16bit_raw()

### `get_mapping_value`
Get the mapping values of the joystick.

:return: A tuple containing the mapping values (x_negative_min, x_negative_max, x_positive_min, x_positive_max, y_negative_min, y_negative_max, y_positive_min, y_positive_max).
:rtype: tuple

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        mapping = joystick_0.get_mapping_value()

### `set_mapping_value`
Set the mapping values of the joystick.

:param tuple value: A tuple containing the mapping values (x_negative_min, x_negative_max, x_positive_min, x_positive_max, y_negative_min, y_negative_max, y_positive_min, y_positive_max).
:param bool save: Whether to save the mapping values to non-volatile memory.
:return: True if the mapping values were set successfully, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = joystick_0.set_mapping_value((100, 200, 300, 400, 100, 200, 300, 400), True)

    For other button and some general methods, please refer to the :class:`ChainKey <chain.key.KeyChain>` class.
