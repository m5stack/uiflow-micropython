# Buzzer Unit

<!-- .. include:: ../refs/unit.buzzer.ref -->

Support the following products:

    |Buzzer|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import BuzzerUnit

buzzer_0 = None

def setup():
    global buzzer_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    buzzer_0 = BuzzerUnit((8, 9))

def loop():
    global buzzer_0
    M5.update()
    if M5.Touch.getCount():
        buzzer_0.once(freq=4000, duty=50, duration=50)

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

    |cores3_buzzer_example.m5f2|

## class BuzzerUnit

## Constructors

<!-- .. class:: BuzzerUnit(port) -->

    Create an BuzzerUnit object.

    The parameters are:
        - ``port`` Is the pin number of the port

    UIFLOW2:

## Methods

<!-- .. method:: BuzzerUnit.once(freq=10, duty=50, duration=50) -->

    Play buzzer once.

    :param int freq: The frequency of the vibration, range is 100 - 10000Hz.
    :param int duty: The duty cycle of the vibration, range is 0 - 100.
    :param int duration: The duration of the vibration, range is 0 - 10000ms.

    UIFLOW2:

<!-- .. method:: BuzzerUnit.set_freq(freq: int) -->

    Set the frequency of the buzzer.

    :param int freq: The frequency of the vibration, range is 100 - 10000Hz.

    UIFLOW2:

<!-- .. method:: BuzzerUnit.set_duty(duty: int) -->

    Set the duty cycle of the buzzer.

    :param int duty: The duty cycle of the vibration, range is 0 - 100.

    UIFLOW2:

<!-- .. method:: BuzzerUnit.turn_off() -->

    Turn off the buzzer.

    UIFLOW2:

<!-- .. method:: BuzzerUnit.deint() -->

    Deinitialize the buzzer.

    UIFLOW2:
