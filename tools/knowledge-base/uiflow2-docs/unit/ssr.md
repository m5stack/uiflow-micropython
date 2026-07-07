
# SSR Unit

<!-- .. include:: ../refs/unit.ssr.ref -->

UNIT SSR Solid-state relays are different from traditional electromagnetic relays in that their switching life are much longer than that of electromagnetic relays. With integrated MOC3043M optocoupler isolation and zero-crossing detection,It supports input 3.3-5V DC control signal, and control output single-phase 220-250V AC power.

Support the following products:

|SSRUnit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import SSRUnit
import time

ssr_0 = None

def setup():
    global ssr_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    ssr_0 = SSRUnit((8, 9))

def loop():
    global ssr_0
    M5.update()
    ssr_0.set_state(1)
    time.sleep(1)
    ssr_0.off()
    time.sleep(1)

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

    |cores3_ssr_example.m5f2|

## class SSRUnit

## Constructors

<!-- .. method:: SSRUnit(port) -->

    Initialize the SSR.

    - ``port``: The port to which the Fader is connected. port[1]: control pin

    UIFLOW2:

## Methods

<!-- .. method:: SSRUnit.on() -->

    Turn on the SSR.

    UIFLOW2:

<!-- .. method:: SSRUnit.off() -->

    Turn off the SSR.

    UIFLOW2:

<!-- .. method:: SSRUnit.set_state(state) -->

    Set the state of the SSR.

    - ``state``: The state of the SSR.

    UIFLOW2:
