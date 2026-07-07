# PWRCAN

<!-- .. include:: ../refs/hardware.pwrcan.ref -->

The PWRCAN is a CAN interface that can be used to communicate with other devices.

The following are the host's support for PWRCAN:

<!-- .. table:: -->
    :widths: auto
    :align: center
######

###### |Controller       | Status         |

###### | PowerHub        | |S|            |

<!-- .. |S| unicode:: U+2714 -->

## UiFlow2 Example

#### pwrcan_send_receive

Open the |pwrcan_send_receive_powerhub_example.m5f2| project in UiFlow2.

This example demonstrates how to utilize PWRCAN interfaces to sender and receive data.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### pwrcan_send_receive

This example demonstrates how to utilize PWRCAN interfaces to sender and receive data.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import PWRCAN

pwrcan = None

def setup():
    global pwrcan

    M5.begin()
    Power.setExtPortBusConfig(direction=1, output_enable=1, voltage=12000, current_limit=232)
    pwrcan = PWRCAN(id=0, port=(40, 39), mode=PWRCAN.NORMAL, baudrate=25000)

def loop():
    global pwrcan
    M5.update()
    if BtnA.wasPressed():
        pwrcan.send("uiflow2", 0, timeout=0, rtr=False, extframe=False)
    if pwrcan.any(0):
        print(pwrcan.recv(0, timeout=5000))

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

#### PWRCAN

<!-- .. class:: PWRCAN(id, mode, tx, rx, prescaler=32, sjw=3, bs1=15, bs2=4, triple_sampling=False) -->

    Initialise the CAN bus with the given parameters.

    :param int id: The CAN bus ID.
    :param int mode: One of NORMAL, NO_ACKNOWLEDGE, LISTEN_ONLY.
    :param int tx: The pin to use for transmitting data.
    :param int rx: The pin to use for receiving data.
    :param int prescaler: The value by which the CAN input clock is divided to generate the nominal bit time quanta. Value between 1 and 1024 inclusive for classic CAN.
    :param int sjw: The resynchronisation jump width in units of time quanta for nominal bits; value between 1 and 4 inclusive for classic CAN.
    :param int bs1: Defines the location of the sample point in units of the time quanta for nominal bits; value between 1 and 16 inclusive for classic CAN.
    :param int bs2: Defines the location of the transmit point in units of the time quanta for nominal bits; value between 1 and 8 inclusive for classic CAN.
    :param bool triple_sampling: Enables triple sampling when the TWAI controller samples a bit.

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from hardware import PWRCAN

            can = PWRCAN(id=0, port=(40, 39), mode=PWRCAN.NORMAL, baudrate=25000)

    PWRCAN class inherits CAN class. See :class:`hardware.CAN <hardware.CAN>` for more details.
