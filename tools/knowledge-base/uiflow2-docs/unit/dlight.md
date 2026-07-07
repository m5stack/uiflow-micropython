# DLight Unit

<!-- .. include:: ../refs/unit.dlight.ref -->

Support the following products:

    |Dlight|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import DLightUnit

label0 = None
i2c0 = None
dlight_0 = None

def setup():
    global label0, i2c0, dlight_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 132, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    dlight_0 = DLightUnit(i2c0)
    dlight_0.configure(dlight_0.CONTINUOUSLY, dlight_0.H_RESOLUTION_MODE)

def loop():
    global label0, i2c0, dlight_0
    M5.update()
    label0.setText(str(dlight_0.get_lux()))

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

    |dlight_core_example.m5f2|

## class DLight

## Constructors

<!-- .. class:: DLightUnit(i2c, address: int = 0x23) -->

    Create a DLight object.

    :param i2c: the I2C object.
    :param address: the I2C address of the device. Default is 0x23.

    UIFLOW2:

<!-- .. _unit.DLightUnit.Methods: -->

## Methods

<!-- .. method:: DLightUnit.get_lux() -->

   Get light lux.

    UIFLOW2:

<!-- .. method:: DLightUnit.configure() -->

    Configure the measurement mode (continuous measurement/single measurement) and resolution.

    UIFLOW2:
