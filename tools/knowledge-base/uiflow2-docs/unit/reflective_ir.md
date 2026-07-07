# Reflective IR Unit

<!-- .. include:: ../refs/unit.reflective_ir.ref -->

Support the following products:

    |Reflective IR Unit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import ReflectiveIRUnit

rect0 = None
reflectiveir_0 = None

def reflectiveir_0_not_detected_event(reflectiveir):
    global rect0, reflectiveir_0
    rect0.setColor(color=0x33CC00, fill_c=0x33CC00)

def reflectiveir_0_detected_event(reflectiveir):
    global rect0, reflectiveir_0
    rect0.setColor(color=0xCC0000, fill_c=0xCC0000)

def setup():
    global rect0, reflectiveir_0

    M5.begin()
    rect0 = Widgets.Rectangle(44, 97, 30, 30, 0xFFFFFF, 0xFFFFFF)

    reflectiveir_0 = ReflectiveIRUnit((33, 32))
    reflectiveir_0.set_callback(
        reflectiveir_0_not_detected_event, ReflectiveIRUnit.EVENT_NOT_DETECTED
    )
    reflectiveir_0.set_callback(reflectiveir_0_detected_event, ReflectiveIRUnit.EVENT_DETECTED)
    reflectiveir_0.enable_irq()

def loop():
    global rect0, reflectiveir_0
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

    |stickc_plus_reflectiverir_example.m5f2|

## class ReflectiveIRUnit

## Constructors

<!-- .. class:: ReflectiveIRUnit(port: tuple) -->

    Create a ReflectiveIRUnit object.

    :param tuple port: Specify the port to which the Reflective IR Unit is connected.

    UIFLOW2:

## Methods

<!-- .. method:: ReflectiveIRUnit.get_analog_value() -> int -->

    This method allows read the ADC value of the Reflective IR Unit and return an integer value. The value ranges from 0 to 65535.

    UIFLOW2:

<!-- .. method:: ReflectiveIRUnit.get_digital_value() -> int -->

    This method allows read the digital value of the Reflective IR Unit and return an integer value. The value ranges from 0 to 1.

    UIFLOW2:

<!-- .. method:: ReflectiveIRUnit.enable_irq() -> None -->

   Enable Obstacle detection event

    UIFLOW2:

<!-- .. method:: ReflectiveIRUnit.disable_irq() -> None -->

    Disable Obstacle detection event

    UIFLOW2:

<!-- .. method:: ReflectiveIRUnit.set_callback(handler, trigger=ReflectiveIRUnit.EVENT_DETECTED | ReflectiveIRUnit.EVENT_NOT_DETECTED) -> None -->

    Set the callback function for the Reflective IR Unit.

    :param handler: The callback function to be set.
    :param trigger: The trigger condition for the callback function.

    UIFLOW2:

## Constants

<!-- .. data:: ReflectiveIRUnit.EVENT_DETECTED -->
          ReflectiveIRUnit.EVENT_NOT_DETECTED

    select the EVENT type of the Reflective IR Unit.
