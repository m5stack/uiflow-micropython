# ToF Hat

<!-- .. include:: ../refs/hat.tof.ref -->

The following products are supported:

    |ToFHat|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from hat import ToFHat

label0 = None
i2c0 = None
hat_tof_0 = None

def setup():
    global label0, i2c0, hat_tof_0

    M5.begin()
    label0 = Widgets.Label("label0", 39, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(26), sda=Pin(0), freq=100000)
    hat_tof_0 = ToFHat(i2c0)

def loop():
    global label0, i2c0, hat_tof_0
    M5.update()
    label0.setText(str((str((hat_tof_0.get_range())) + str("mm"))))

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

    |stickc_plus2_tof_example.m5f2|

## class ToFHat

## Constructors

<!-- .. class:: ToFHat(i2c: I2C, address: int = 0x29, io_timeout_ms: int = 0) -->

    Creates an instance of the ToFHat class.

    :param i2c: the I2C object.
    :param address: the I2C address of the device. Default is 0x23.
    :param io_timeout_ms: the timeout of I2C communication. Default is 0ms.

    UIFLOW2:

ToFHat class inherits ToFUnit class, See :ref:`unit.ToFUnit.Methods <unit.ToFUnit.Methods>` for more details.
