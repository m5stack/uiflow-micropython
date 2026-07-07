# Relay2 Unit

<!-- .. sku: U131 -->

<!-- .. include:: ../refs/unit.relay2.ref -->

This is the driver library of Relay2 Unit, which is used to control the relay.

Support the following products:

    |RELAY2|

## UiFlow2 Example

#### control relay

Open the |relay2_core2_example.m5f2| project in UiFlow2.

This example controls the relay of the Relay2 Unit and displays it on the screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### control relay

This example controls the relay of the Relay2 Unit and displays it on the screen.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import Relay2Unit

title0 = None
label2 = None
label0 = None
label3 = None
label1 = None
relay2_0 = None

def setup():
    global title0, label2, label0, label3, label1, relay2_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "Relay2Unit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("Relay1", 38, 214, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("label0", 2, 91, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Relay2", 220, 214, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 2, 136, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    relay2_0 = Relay2Unit((33, 32))

def loop():
    global title0, label2, label0, label3, label1, relay2_0
    M5.update()
    label0.setText(str((str("Relay1 State:") + str((relay2_0.get_relay_status(1))))))
    label1.setText(str((str("Relay2 State:") + str((relay2_0.get_relay_status(2))))))
    if BtnA.wasPressed():
        relay2_0.set_relay_cntrl(1, not (relay2_0.get_relay_status(1)))
    elif BtnC.wasPressed():
        relay2_0.set_relay_cntrl(2, not (relay2_0.get_relay_status(2)))

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

#### Relay2Unit

## Relay2Unit
Create an Relay2Unit object.

:param tuple port: The port of the relay.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from unit import Relay2Unit

        relay2_0 = Relay2Unit((32, 26))

### `set_relay_cntrl`
Set the on/off status of a relay

:param int num: The relay number(the range is 1-2).
:param int control: The control value(0: off, 1: on).

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        relay2_0.set_relay_cntrl(1, 1)

### `get_relay_status`
Getting the on/off status of a relay

:param int num: The relay number.
:returns: relay status.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        relay2_0.get_relay_status()
