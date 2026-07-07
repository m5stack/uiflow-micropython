# ExtEncoder Unit

<!-- .. include:: ../refs/unit.extencoder.ref -->

The following products are supported:

    |ExtEncoderUnit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ExtEncoderUnit

label0 = None
i2c0 = None
extencoder_0 = None

def setup():
    global label0, i2c0, extencoder_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 132, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    extencoder_0 = ExtEncoderUnit(i2c0, 0x59)

def loop():
    global label0, i2c0, extencoder_0
    M5.update()
    if extencoder_0.get_rotary_status():
        label0.setText(str(extencoder_0.get_rotary_value()))

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

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |cores3_extencoder_example.m5f2|

## class ExtEncoderUnit

## Constructors

<!-- .. class:: ExtEncoderUnit(i2c, address: int | list | tuple = 0x59) -->

    Creates a ExtEncoderUnit object.

    UIFLOW2:

## Methods

<!-- .. method:: ExtEncoderUnit.get_rotary_status() -> bool -->

    Gets the rotation status of the ExtEncoderUnit object.

    UIFLOW2:

<!-- .. method:: ExtEncoderUnit.get_rotary_value() -> int -->

    Gets the rotation value of the ExtEncoderUnit object.

    UIFLOW2:

<!-- .. method:: ExtEncoderUnit.get_rotary_increments() -> int -->

    Gets the rotation increment of the ExtEncoderUnit object. Can be used to determine
    the direction of rotation.

    UIFLOW2:

<!-- .. method:: ExtEncoderUnit.reset_rotary_value() -> None -->

    Resets the rotation value of the ExtEncoderUnit object.

    UIFLOW2:

<!-- .. method:: ExtEncoderUnit.set_rotary_value(new_value: int) -> None -->

    Sets the rotation value of the ExtEncoderUnit object.

    :param int new_value: adjust the current value.

    UIFLOW2:

<!-- .. method:: ExtEncoderUnit.get_perimeter() -> int -->

    Gets the perimeter of the ExtEncoderUnit object. The unit is millimeters.

    UIFLOW2:

<!-- .. method:: ExtEncoderUnit.set_perimeter(perimeter: int) -> None -->

    Sets the perimeter of the ExtEncoderUnit object.

    :param int perimeter: the perimeter of the ExtEncoderUnit object. The unit is millimeters.

    UIFLOW2:

<!-- .. method:: ExtEncoderUnit.get_pulse() -> int -->

    pluse per round.

    UIFLOW2:

<!-- .. method:: ExtEncoderUnit.set_pulse(pulse: int) -> None -->

    Sets the pulse per round.

    :param int pulse: the pulse per round.

    UIFLOW2:

<!-- .. method:: ExtEncoderUnit.get_zero_mode() -> int -->

    Gets the zero mode of the ExtEncoderUnit object.

    UIFLOW2:

<!-- .. method:: ExtEncoderUnit.set_zero_mode(mode: int) -> None -->

    Sets the zero mode of the ExtEncoderUnit object.

    :param int mode: the zero mode of the ExtEncoderUnit object.

    UIFLOW2:

<!-- .. method:: ExtEncoderUnit.get_meter_value() -> int -->

    Gets the meter value of the ExtEncoderUnit object. The unit is millimeters.

    UIFLOW2:

<!-- .. method:: ExtEncoderUnit.get_zero_pulse_value() -> int -->

    Gets the zero pulse value of the ExtEncoderUnit object.

    UIFLOW2:

<!-- .. method:: ExtEncoderUnit.set_zero_pulse_value(value: int) -> None -->

    Sets the zero pulse value of the ExtEncoderUnit object.

    :param int value: the zero pulse value of the ExtEncoderUnit object.

    UIFLOW2:

<!-- .. method:: ExtEncoderUnit.get_firmware_version() -> int -->

    Gets the firmware version of the ExtEncoderUnit object.

    UIFLOW2:

<!-- .. method:: ExtEncoderUnit.set_address(address) -> int -->

    Sets the I2C address of the ExtEncoderUnit object.

    UIFLOW2:
