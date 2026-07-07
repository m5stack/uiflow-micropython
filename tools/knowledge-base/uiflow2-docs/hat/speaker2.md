<!-- .. _hat.Speaker2: -->

# Speaker2 Hat

<!-- .. sku: U055-B -->

<!-- .. include:: ../refs/hat.speaker2.ref -->

This is the driver library of Speaker2 Hat, which is provides a set of methods to control the speaker.

Support the following products:

    |Speaker2|

## UiFlow2 Example

#### play audio

Open the |speaker2_stickcplus2_example.m5f2| project in UiFlow2.

This example demonstrates how to play audio.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### play audio

This example demonstrates how to play audio.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hat import Speaker2Hat

title1 = None
label0 = None
label1 = None
hat_spk2_0 = None

def setup():
    global title1, label0, label1, hat_spk2_0

    Widgets.setRotation(3)
    M5.begin()
    title1 = Widgets.Title("SPK2 StickcPlus2 e.g.", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label(
        "Press BtnA to Beep", 1, 39, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "Press BtnB to play wav", 1, 74, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    hat_spk2_0 = Speaker2Hat((26, 0))
    hat_spk2_0.setVolumePercentage(1)

def loop():
    global title1, label0, label1, hat_spk2_0
    M5.update()
    if BtnA.wasPressed():
        hat_spk2_0.tone(2000, 100)
    if BtnB.wasPressed():
        hat_spk2_0.playWavFile("/flash/res/audio/poweron_2_5s.wav")

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

#### Speaker2

## Speaker2Hat

    Speaker2 class inherits Speaker class, See :ref:`hardware.Speaker.Methods <hardware.Speaker.Methods>` for more details.
