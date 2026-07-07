# Grove2Grove Unit

<!-- .. include:: ../refs/unit.grove2grove.ref -->

UNIT-GROVE2GROVE is a Grove expansion Unit with On/Off Control + Current Meter
functions. On/Off control adopts switch value, Current meter is 0 - 3.3V analog
signal.

Support the following products:

    |Grove2GroveUnit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import Grove2GroveUnit

label0 = None
label1 = None
grove2grove_0 = None

def setup():
    global label0, label1, grove2grove_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("current:", 50, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 150, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    grove2grove_0 = Grove2GroveUnit((8, 9))
    grove2grove_0.on()

def loop():
    global label0, label1, grove2grove_0
    M5.update()
    label1.setText(str(grove2grove_0.get_current()))

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

    |cores3_grove2_grove_example.m5f2|

## class Grove2GroveUnit

## Constructors

<!-- .. class:: Grove2GroveUnit(port: tuple) -->

    Initialize the Grove2GroveUnit.

    :param tuple port: The port to which the Grove2GroveUnit is connected. port[0]: adc pin, port[1]: grove pin.

    UIFLOW2:

## Methods

<!-- .. method:: Grove2GroveUnit.get_current() -> float -->

    Get the current of the sensor.

    :return: The current of the sensor.

    UIFLOW2:

<!-- .. method:: Grove2GroveUnit.on() -> None -->

    Turn on the grove.

    UIFLOW2:

<!-- .. method:: Grove2GroveUnit.off() -> None -->

    Turn off the grove.

    UIFLOW2:

<!-- .. method:: Grove2GroveUnit.set_en(state: int) -> None -->

    Set the state of the grove.

    :param int state: The state of the grove.

    UIFLOW2:
