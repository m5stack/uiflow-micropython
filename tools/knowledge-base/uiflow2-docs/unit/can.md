<!-- .. _unit.CANUnit: -->

<!-- .. py:currentmodule:: unit -->

# CANUnit

<!-- .. include:: ../refs/unit.can.ref -->

The CAN Unit is used to communicate via the CAN bus.
The following products are supported:

    ================== ==================
    |CAN Unit|         |MiniCAN Unit|
    ================== ==================

## UiFlow2 Example

#### TX Example

Open the |stickc_plus2_can_tx_example.m5f2| project in UiFlow2.

This example demonstrates how to transmit data using CAN Unit.

Click the BtnA to change the data to be sent.

UiFlow2 Code Block:

Example output:

    None

#### RX Example

Open the |dial_can_rx_example.m5f2| project in UiFlow2.

This example demonstrates how to receive data using CAN Unit.

UiFlow2 Code Block:

Example output:

    Screen will display the received CAN data.

## MicroPython Example

#### TX Example

This example demonstrates how to transmit data using CAN Unit.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import CANUnit
from hardware import *

label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
can_0 = None

import random

id2 = None
payload = None

def setup():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        can_0, \
        id2, \
        payload

    M5.begin()
    label0 = Widgets.Label("Master", 35, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("ID:", 4, 39, 1.0, 0xF5A41D, 0x080808, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("RTR:", 4, 90, 1.0, 0xF5A41D, 0x000000, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Ext:", 4, 141, 1.0, 0xF5A41D, 0x000000, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Msg:", 3, 192, 1.0, 0xF5A41D, 0x000000, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("label5", 3, 64, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("label6", 4, 115, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("label7", 4, 166, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label8 = Widgets.Label("label8", 4, 217, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    can_0 = CANUnit((33, 32), CANUnit.NORMAL, baudrate=25000)
    id2 = 123
    payload = "uiflow2"
    label5.setText(str(id2))
    label6.setText(str(False))
    label7.setText(str(False))
    label0.setText(str(payload))

def loop():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        can_0, \
        id2, \
        payload
    M5.update()
    can_0.send(payload, id2, timeout=0, rtr=False, extframe=False)
    if BtnA.wasClicked():
        id2 = random.randint(1, 100)
        label5.setText(str(id2))
        payload = str((random.randint(32, 126)))
        label8.setText(str(payload))

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

#### RX Example

This example demonstrates how to receive data using CAN Unit.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import MiniCANUnit

label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
minican_0 = None

frame = None

def setup():
    global label0, label1, label2, label3, label4, label5, label6, label7, label8, minican_0, frame

    M5.begin()
    label0 = Widgets.Label("Slaver", 90, 13, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("ID:", 35, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Ext:", 25, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("RTR:", 20, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Msg:", 18, 90, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("label5", 72, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("label6", 72, 89, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("label7", 72, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label8 = Widgets.Label("label8", 72, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    minican_0 = MiniCANUnit((1, 2), MiniCANUnit.NORMAL, baudrate=25000)

def loop():
    global label0, label1, label2, label3, label4, label5, label6, label7, label8, minican_0, frame
    M5.update()
    if minican_0.any(0):
        frame = minican_0.recv(0, timeout=5000)
        label5.setText(str(frame[0]))
        label6.setText(str(frame[4]))
        label7.setText(str(frame[2]))
        label8.setText(str(frame[1]))

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

    Screen will display the received CAN data.

## API

#### CANUnit

<!-- .. class:: CANUnit(port, mode, baudrate=125000) -->

    Create a CANUnit object.

    :param int id: The CAN ID.
    :param tuple port: The port pins (tx, rx).
    :param int mode: One of CAN.NORMAL, CAN.NO_ACKNOWLEDGE, CAN.LISTEN_ONLY.
    :param int baudrate: The baudrate of CANUnit.

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from unit import CANUnit

            can = CANUnit(id=0, port=(13, 14), mode=CANUnit.NORMAL, baudrate=125000)

<!-- .. note:: -->

        CANUnit class inherits CAN class. See :class:`hardware.CAN <hardware.CAN>` for more details.

<!-- .. class:: CANUnit(tx, rx, mode, prescaler=32, sjw=3, bs1=15, bs2=4, triple_sampling=False) -->
    :no-index:

    Initialise the CAN bus with the given parameters.

    :param int id: The CAN ID.
    :param tuple port: The port pins (tx, rx).
    :param int mode: One of CAN.NORMAL, CAN.NO_ACKNOWLEDGE, CAN.LISTEN_ONLY.
    :param int prescaler: The value by which the CAN input clock is divided to generate the nominal bit time quanta. The prescaler can be a value between 1 and 1024 inclusive for classic CAN.
    :param int sjw: The resynchronisation jump width in units of time quanta for nominal bits; it can be a value between 1 and 4 inclusive for classic CAN.
    :param int bs1: Defines the location of the sample point in units of the time quanta for nominal bits; it can be a value between 1 and 16 inclusive for classic CAN.
    :param int bs2: Defines the location of the transmit point in units of the time quanta for nominal bits; it can be a value between 1 and 8 inclusive for classic CAN.
    :param bool triple_sampling: is Enables triple sampling when the TWAI controller samples a bit.

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from unit import CANUnit

            can = CANUnit(id=0, port=(13, 14), mode=CANUnit.NORMAL, prescaler=128, sjw=3, bs1=16, bs2=8, triple_sampling=False)

<!-- .. note:: -->

        CANUnit class inherits CAN class. See :class:`hardware.CAN <hardware.CAN>` for more details.
