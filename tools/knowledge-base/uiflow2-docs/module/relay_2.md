
# Relay2 Module

<!-- .. include:: ../refs/module.relay_2.ref -->

Support the following products:

|Relay2Module|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from module import Relay2Module
from hardware import *

title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
relay2_0 = None

def setup():
    global title0, label0, label1, label2, label3, relay2_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("2Relay Module Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Relay 1:", 2, 53, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Relay 2:", 2, 119, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("I2C Addr:", 1, 177, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label(
        "FW Version:", 181, 177, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    relay2_0 = Relay2Module(address=0x25)
    label2.setText(str((str("I2C Addr:") + str((relay2_0.get_i2c_address())))))
    label3.setText(str((str("FW Version:") + str((relay2_0.get_firmware_version())))))

def loop():
    global title0, label0, label1, label2, label3, relay2_0
    M5.update()
    label0.setText(str((str("Relay 1:") + str((relay2_0.get_relay_status(1))))))
    label1.setText(str((str("Relay 2:") + str((relay2_0.get_relay_status(2))))))
    if BtnA.isPressed():
        relay2_0.set_relay_state(1, 1)
    else:
        relay2_0.set_relay_state(1, 0)
    if BtnB.isPressed():
        relay2_0.set_relay_state(2, 1)
    else:
        relay2_0.set_relay_state(2, 0)

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

## class Relay2Module

## Constructors

<!-- .. class:: Relay2Module(address) -->

    Initialize the 2Relay Module with the specified I2C address.

    :param int|list|tuple address: I2C address of the Relay2Module.

    UIFLOW2:

## Methods

<!-- .. method:: Relay2Module.set_relay_state(num, state) -> None -->

    Set the state of a specific relay.

    :param int num: The relay number (1 or 2).
    :param bool state: True to turn on, False to turn off.

    UIFLOW2:

<!-- .. method:: Relay2Module.get_relay_status(num) -> bool -->

    Get the status of a specific relay.

    :param int num: The relay number (1 or 2).

    UIFLOW2:

<!-- .. method:: Relay2Module.set_all_relay_state(state) -> None -->

    Set the state of both relays simultaneously.

    :param bool state: True to turn on both relays, False to turn off both relays.

    UIFLOW2:

<!-- .. method:: Relay2Module.get_firmware_version() -> int -->

    Get the firmware version of the Relay2 Module.

    UIFLOW2:

<!-- .. method:: Relay2Module.set_i2c_address(addr) -> None -->

    Set a new I2C address(0x08~0x77) for the Relay2 Module.

    :param int addr: The new I2C address to set.

    UIFLOW2:

<!-- .. method:: Relay2Module.get_i2c_address() -> int -->

    Get the current I2C address of the Relay2 Module.

    UIFLOW2:
