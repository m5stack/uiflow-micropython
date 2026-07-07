# RCA Module

<!-- .. sku: M125 -->

<!-- .. include:: ../refs/module.rca.ref -->

Module RCA is a female jack terminal block for transmitting composite video (audio or video), one of the most common A/V connectors, which transmits  video or audio signals from a component device to an output  device (i.e., a display or speaker).

Support the following products:

    |RCAModule|

## UiFlow2 Example

#### Draw Text

Open the |core2_rca_example.m5f2| project in UiFlow2.

This example displays the text "RCA" on the screen.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Draw Text

This example displays the text "RCA" on the screen.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import RCAModule

label0 = None
label1 = None
module_rca = None

def setup():
    global label0, label1, module_rca

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Core2", 133, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    module_rca = RCAModule(
        26,
        width=216,
        height=144,
        output_width=0,
        output_height=0,
        signal_type=RCAModule.NTSC,
        use_psram=0,
        output_level=0,
    )
    label1 = Widgets.Label(
        "RCA", 88, 61, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18, module_rca
    )

def loop():
    global label0, label1, module_rca
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

Example output:

    None

## **API**

#### Class RCAModule

## RCAModule
Initialize the RCA Module.

:param int pin: The dac pin to which the RCA Module is connected.
:param int width: The width of the RCA display.
:param int height: The height of the RCA display.
:param int output_width: The width of the output of the RCA display.
:param int output_height: The height of the output of the RCA display.
:param int signal_type: The signal type of the RCA display. NTSC=0, NTSC_J=1, PAL=2, PAL_M=3, PAL_N=4.
:param int use_psram: The use of psram of the RCA display.
:param int output_level: The output level of the RCA display.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from module import RCAModule
        module_rca = RCAModule(26, width=216, height=144, output_width=0, output_height=0, signal_type=RCAModule.NTSC, use_psram=0, output_level=0)

    RCAModule class inherits Display class, See :ref:`hardware.Display <hardware.Display>` for more details.
