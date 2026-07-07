# DLight Hat

<!-- .. include:: ../refs/hat.dlight.ref -->

The following products are supported:

    |DLightHAT|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from hat import DLightHat

label0 = None
i2c0 = None
hat_dlight_0 = None

def setup():
    global label0, i2c0, hat_dlight_0

    M5.begin()
    label0 = Widgets.Label("label0", 39, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(26), sda=Pin(0), freq=100000)
    hat_dlight_0 = DLightHat(i2c0)
    hat_dlight_0.configure(hat_dlight_0.CONTINUOUSLY, hat_dlight_0.H_RESOLUTION_MODE)

def loop():
    global label0, i2c0, hat_dlight_0
    M5.update()
    label0.setText(str(hat_dlight_0.get_lux()))

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

    |stickc_plus2_dlight_example.m5f2|

## class DLightHat

## Constructors

<!-- .. class:: DLightHat(i2c, address: int = 0x23) -->

    Create a DLightHat object.

    :param i2c: I2C object
    :param address: the I2C address of the device. Default is 0x23.

    UIFLOW2:

DLightHat class inherits DLightUnit class, See :ref:`unit.DLightUnit.Methods <unit.DLightUnit.Methods>` for more details.
