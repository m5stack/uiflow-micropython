# Finger Hat

<!-- .. include:: ../refs/hat.finger.ref -->

The following products are supported:

    |FingerHat|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hat import FingerHat

label0 = None
hat_finger_0 = None

def setup():
    global label0, hat_finger_0

    M5.begin()
    label0 = Widgets.Label("label0", 4, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    hat_finger_0 = FingerHat(1, (26, 0))

def loop():
    global label0, hat_finger_0
    M5.update()
    label0.setText(str(hat_finger_0.get_user_list()))

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

    |stickc_plus2_finger_example.m5f2|

## class FingerHat

## Constructors

<!-- .. class:: FingerHat(id: Literal[0, 1, 2] = 2, port: list | tuple = None) -->

    Create a FingerHat object.

    :param id: The ID of the UART, 0 or 1 or 2.
    :param port: UART pin numbers.

    UIFLOW2:

FingerUnit class inherits FingerUnit class, See :ref:`unit.FingerUnit.Methods <unit.FingerUnit.Methods>` for more details.
