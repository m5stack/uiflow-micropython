# PIR Unit

<!-- .. include:: ../refs/unit.pir.ref -->

Support the following products:

    |PIR|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import PIRUnit

label0 = None
pir_0 = None

def pir_0_active_event(pir):
    global label0, pir_0
    label0.setText(str("Detected"))

def pir_0_negative_event(pir):
    global label0, pir_0
    label0.setText(str("Not detected"))

def setup():
    global label0, pir_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 132, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    pir_0 = PIRUnit((36, 26))
    pir_0.set_callback(pir_0_active_event, pir_0.IRQ_ACTIVE)
    pir_0.set_callback(pir_0_negative_event, pir_0.IRQ_NEGATIVE)
    pir_0.enable_irq()

def loop():
    global label0, pir_0
    M5.update()

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

    |pir_core_example.m5f2|

## class PIR

## Constructors

<!-- .. class:: PIR(IO1,IO2) -->

    Create a PIR object.

    The parameters are:
        - ``IO1,IO2`` I2C pin.

    UIFLOW2:

## Methods

<!-- .. method:: PIR.get_status() -->

    Get detection status.

    UIFLOW2:

<!-- .. method:: PIR.enable_irq() -->

   Enable Human detection function.

    UIFLOW2:

<!-- .. method:: PIR.disable_irq() -->

    Disable Human detection function.

    UIFLOW2:

<!-- .. method:: PIR.set_callback() -->

    Polling method, placed in the loop function, constantly check.

    UIFLOW2:
