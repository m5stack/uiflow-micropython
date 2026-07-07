# Pin

<!-- .. include:: ../refs/hardware.pin.ref -->

The Pin class is used to manage GPIO operations. Below is the detailed support for the Pin class:

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
import time

title0 = None
label0 = None
label1 = None
pin6 = None
pin7 = None

def setup():
    global title0, label0, label1, pin6, pin7

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Pin example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Pin 6 State:", 1, 83, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Pin 7 State:", 1, 132, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    pin6 = Pin(6, mode=Pin.OUT)
    pin7 = Pin(7, mode=Pin.IN)

def loop():
    global title0, label0, label1, pin6, pin7
    M5.update()
    pin6.value(1)
    label0.setText(str((str("Pin 6 State:") + str((pin6.value())))))
    time.sleep(1)
    pin6.value(0)
    label0.setText(str((str("Pin 6 State:") + str((pin6.value())))))
    time.sleep(1)
    label1.setText(str((str("Pin 7 State:") + str((pin7.value())))))

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

    |pin_cores3_example.m5f2|

## class Pin

## Constructors

<!-- .. class:: Pin(id, mode=-1, pull=-1) -->

    Access the pin peripheral (GPIO pin) associated with the given ``id``.

    :param int id: is mandatory and can be an arbitrary object.
    :param int mode: specifies the pin mode.

        - ``Pin.IN`` - Pin is configured for input.  If viewed as an output the pin is in high-impedance state.

        - ``Pin.OUT`` - Pin is configured for (normal) output.

    :param int pull: specifies if the pin has a (weak) pull resistor attached.

        - ``None`` - No pull up or down resistor.
        - ``Pin.PULL_UP`` - Pull up resistor enabled.
        - ``Pin.PULL_DOWN`` - Pull down resistor enabled.

    UIFLOW2:

## Methods

<!-- .. method:: Pin.value([value]) -->

   Set the value of the pin.

   The argument ``value`` can be anything that converts to a boolean.
   If it converts to ``True``, the pin is set to state '1', otherwise it is set
   to state '0'.

   The behaviour of this method depends on the mode of the pin:

     - ``Pin.IN`` - The value is stored in the output buffer for the pin.  The
       pin state does not change, it remains in the high-impedance state.  The
       stored value will become active on the pin as soon as it is changed to
       ``Pin.OUT`` mode.
     - ``Pin.OUT`` - The output buffer is set to the given value immediately.

    UIFLOW2:

<!-- .. method:: Pin.off() -> None -->

    Sets the pin to low level.

    UIFLOW2:

<!-- .. method:: Pin.on() -> None -->

    Sets the pin to high level.

    UIFLOW2:

## Constants

<!-- .. data:: Pin.IN -->

    Input mode

<!-- .. data:: Pin.OUT -->

    Output mode

<!-- .. data:: Pin.PULL_UP -->

    Pull-up resistor

<!-- .. data:: Pin.PULL_DOWN -->

    Pull-down resistor
