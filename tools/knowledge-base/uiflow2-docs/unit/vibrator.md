# Vibrator Unit

<!-- .. include:: ../refs/unit.vibrator.ref -->

Support the following products:

    |Vibrator|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import VibratorUnit

label0 = None
vibrator_0 = None

def btnB_wasClicked_event(state):  # noqa: N802
    global label0, vibrator_0
    vibrator_0.once(freq=1000, duty=15, duration=50)

def setup():
    global label0, vibrator_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("play", 127, 210, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)

    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnB_wasClicked_event)

    vibrator_0 = VibratorUnit((36, 26))

def loop():
    global label0, vibrator_0
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

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |core_vibrator_example.m5f2|

## class VibratorUnit

## Constructors

<!-- .. class:: VibratorUnit(port: tuple = (26, 0)) -->

    Create an VibratorUnit object.

    :param port: The port where the VibratorUnit is connected to.

    UIFLOW2:

## Methods

<!-- .. method:: VibratorUnit.once(freq=10, duty=50, duration=50) -> None -->

    Play the haptic effect once on the motor.

    :param int freq: The frequency of vibration ranges from 10-55Hz.
    :param int duty: The duty cycle of vibration ranges from 0-100, representing the corresponding percentage.
    :param int duration: The duration of the vibration effect, in milliseconds.

    UIFLOW2:

<!-- .. method:: VibratorUnit.set_freq(freq) -->

    Set the vibration frequency.

    :param int freq: The frequency of vibration ranges from 10-55Hz.

    UIFLOW2:

<!-- .. method:: VibratorUnit.set_duty(freq) -> None -->

    Set the vibration duty cycle.

    :param int duty: The duty cycle of vibration ranges from 0-100, representing the corresponding percentage.

    UIFLOW2:

<!-- .. method:: VibratorUnit.turn_off() -> None -->

    Turn off the motor.

    UIFLOW2:

<!-- .. method:: VibratorUnit.deint() -> None -->

    Deinitialize the motor.

    UIFLOW2:
