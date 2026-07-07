# Chain Angle

<!-- .. include:: ../refs/chain.angle.ref -->

AngleChain is the helper class for angle sensor devices on the Chain bus. It provides methods to read angle values in different resolutions (12-bit and 8-bit ADC) and configure the clockwise rotation direction.

Support the following products:

    |Chain Angle|

## UiFlow2 Example

#### Angle reading with RGB brightness control

Open the |m5core_chain_angle_basic_example.m5f2| project in UiFlow2.

This example demonstrates how to read angle values from the Chain Angle sensor and control RGB brightness based on the angle value.
The example reads 8-bit ADC values (0-255) and maps them to brightness values (0-100) for visual feedback.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Angle reading with RGB brightness control

This example demonstrates how to read angle values from the Chain Angle sensor and control RGB brightness based on the angle value.
The example reads 8-bit ADC values (0-255) and maps them to brightness values (0-100) for visual feedback.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from chain import ChainBus
from chain import AngleChain
import time
import m5utils

title0 = None
label_brightness = None
label_val = None
bus2 = None
chain_angle_0 = None
last_time = None
value = None
brightness = None

def setup():
    global title0, label_brightness, label_val, bus2, chain_angle_0, last_time, value, brightness
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Chain Angle Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_brightness = Widgets.Label(
        "Brightness: ", 5, 117, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24
    )
    label_val = Widgets.Label("Value:", 5, 69, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    bus2 = ChainBus(2, tx=21, rx=22)
    chain_angle_0 = AngleChain(bus2, 1)
    chain_angle_0.set_rgb_color(0x00CCCC)

def loop():
    global title0, label_brightness, label_val, bus2, chain_angle_0, last_time, value, brightness
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        value = chain_angle_0.get_adc8()
        brightness = int(m5utils.remap(value, 0, 255, 0, 100))
        label_val.setText(str((str("Value: ") + str(value))))
        label_brightness.setText(str((str("Brightness: ") + str(brightness))))
        chain_angle_0.set_rgb_brightness(brightness, save=False)

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

#### AngleChain

## AngleChain
Angle Chain class for interacting with angle devices over Chain bus.

:param ChainBus bus: The Chain bus instance.
:param int device_id: The device ID of the angle sensor on the Chain bus.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from chain import ChainBus
        from chain import AngleChain

        chainbus_0 = ChainBus(2, 32, 33, verbose=True)
        angle_0 = AngleChain(chainbus_0, 1)

### `get_adc12`
Get the angle value in 12-bit ADC resolution.

:return: Angle value in 12-bit ADC (0-4095), or None if failed.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        angle = angle_0.get_adc12()

### `get_adc8`
Get the angle value in 8-bit ADC resolution.

:return: Angle value in 8-bit ADC (0-255), or None if failed.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        angle = angle_0.get_adc8()

### `set_cw_increase`
Set whether clockwise rotation increases the angle value.

:param bool increase: Whether clockwise rotation increases. False means clockwise decreases, True means clockwise increases.
:param bool save: Whether to save to flash. False means don't save, True means save.
:return: True if the setting was set successfully, False otherwise.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        success = angle_0.set_cw_increase(True, False)

### `get_cw_increase`
Get whether clockwise rotation increases the angle value.

:return: Whether clockwise rotation increases. False means clockwise decreases, True means clockwise increases. Returns False if failed.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        increase = angle_0.get_cw_increase()

    For other button and some general methods, please refer to the :class:`ChainKey <chain.key.KeyChain>` class.
