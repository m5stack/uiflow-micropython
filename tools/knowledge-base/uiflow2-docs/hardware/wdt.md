# WDT

<!-- .. include:: ../refs/hardware.wdt.ref -->

The WDT is used to restart the system when the application crashes and ends
up into a non recoverable state. Once started it cannot be stopped or reconfigured in any way.
After enabling, the application must "feed" the
watchdog periodically to prevent it from expiring and resetting the system.

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *

title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
wdt = None

isTouch = None

def setup():
    global title0, label0, label1, label2, label3, wdt, isTouch

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("WDT CoreS3 example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Touch State:", 2, 92, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("WDT State:", 2, 155, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label(
        "pls touch screen to feed the dog", 0, 27, 1.0, 0xFFCF00, 0x222222, Widgets.FONTS.DejaVu18
    )
    label3 = Widgets.Label("label3", -117, 96, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    wdt = WDT(timeout=2500)
    isTouch = 0

def loop():
    global title0, label0, label1, label2, label3, wdt, isTouch
    M5.update()
    isTouch = M5.Touch.getCount()
    label0.setText(str((str("Touch State:") + str(isTouch))))
    if isTouch:
        wdt.feed()
        label1.setText(str("WDT State: Feed!"))
    else:
        label1.setText(str("WDT State: Not Feed! Will crush!"))

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

    |wdt_cores3_example.m5f2|

## class WDT -- watchdog timer

## Constructors

<!-- .. class:: WDT(id=0, timeout=5000) -->

   Create a WDT object and start it. The timeout must be given in milliseconds.
   Once it is running the timeout cannot be changed and the WDT cannot be stopped either.

   Notes: On the esp8266 a timeout cannot be specified, it is determined by the underlying system.
   On rp2040 devices, the maximum timeout is 8388 ms.

    UIFLOW2:

## Methods

<!-- .. method:: WDT.feed() -->

   Feed the WDT to prevent it from resetting the system. The application
   should place this call in a sensible place ensuring that the WDT is
   only fed after verifying that everything is functioning correctly.

    UIFLOW2:
