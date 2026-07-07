# Atomic CAN Base

<!-- .. sku: A103/KO57 -->

<!-- .. include:: ../refs/base.can.ref -->

This is the driver library for the ATOM CAN Base to accept and send data from the CAN module.

Support the following products:

    ================== ==================
    |Atom CAN|         |Atomic CAN Base|
    ================== ==================

## UiFlow2 Example

#### CAN communication

Open the |atoms3_can_example.m5f2| project in UiFlow2.

This example shows how to receive and send data using the Atom CAN Base.

UiFlow2 Code Block:

Example output:

    Output of received CAN message data via serial port.

## MicroPython Example

#### CAN communication

This example shows how to receive and send data using the Atom CAN Base.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import ATOMCANBase
import time

title0 = None
label0 = None
label1 = None
base_can = None

def setup():
    global title0, label0, label1, base_can

    M5.begin()
    title0 = Widgets.Title("CAN Base", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("TX:", 1, 38, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("RX:", 1, 68, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    base_can = ATOMCANBase(0, (6, 5), ATOMCANBase.NORMAL, baudrate=1000000)

def loop():
    global title0, label0, label1, base_can
    M5.update()
    if BtnA.isPressed():
        label0.setText(str("TX: Send"))
        base_can.send("uiflow2", 0, timeout=0, rtr=False, extframe=False)
        time.sleep(1)
        label0.setText(str("TX: Not Send"))
    if base_can.any(0):
        label1.setText(str("RX: Rec"))
        print(base_can.recv(0, timeout=5000))
        time.sleep(1)
        label1.setText(str("RX: Not Rec"))

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

    Output of received CAN message data via serial port.

## **API**

#### ATOMCANBase

## ATOMCANBase
Create an ATOMCANBase object

:param int id: The CAN ID to use, Default is 0.
:param port: A list or tuple containing the TX and RX pin numbers.
:type port: list | tuple
:param int mode: The CAN mode to use(NORMAL, NO_ACKNOWLEDGE, LISTEN_ONLY), Default is NORMAL.
:param int baudrate: The baudrate to use, Default is 1000000.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from base import ATOMCANBase

        base_can = ATOMCANBase(0, (6, 5), ATOMCANBase.NORMAL, baudrate=1000000)

    ATOMCANBase class inherits CAN class, See :class:`hardware.CAN <hardware.CAN>` for more details.
