# Catch Unit

<!-- .. include:: ../refs/unit.catch.ref -->

Catch is a gripper that uses a SG92R servo as a power source. The servo uses a
PWM signal to drive the gripper gear to rotate and control the gripper for
clamping and releasing operations. The structure adopts a design compatible with
Lego 8mm round holes. You can combine it with other Lego components to build
creative control structures, such as robotic arms, gripper carts, etc.

Support the following products:

    |CatchUnit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import CatchUnit
import time

catch_0 = None

import random

def setup():
    global catch_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    catch_0 = CatchUnit((8, 9))

def loop():
    global catch_0
    M5.update()
    catch_0.set_clamp_percent(random.randint(1, 100))
    time.sleep_ms(100)

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

    |cores3_catch_example.m5f2|

## class CatchUnit

## Constructors

<!-- .. class:: CatchUnit(port: tuple) -->

    Initialize the Servo.

    :param tuple port: The port to which the Servo is connected.

    UIFLOW2:

## Methods

<!-- .. method:: CatchUnit.clamp() -> None -->

    Clamp the gripper.

    UIFLOW2:

<!-- .. method:: CatchUnit.release() -> None -->

    Release the gripper.

    UIFLOW2:

<!-- .. method:: CatchUnit.set_duty(duty: int) -> None -->

    Set the duty cycle.

    :param int duty: The duty cycle. from 20 to 54.

    UIFLOW2:

<!-- .. method:: CatchUnit.set_clamp_percent(percent: int) -> None -->

    Set the clamping percentage.

    :param int percent: The clamping percentage. from 0 to 100.

    UIFLOW2:

<!-- .. method:: CatchUnit.deinit() -> None -->

    Deinitialize the Servo.

    UIFLOW2:
