
# Button Unit

<!-- .. include:: ../refs/unit.button.ref -->

BUTTON is a single button Unit. The button status can be detected by the input pin by simply capturing the high/low electrical level. If the button is pressed, the signal level will be *high* if the button is released, the signal level will be *low*.

Support the following products:

|ButtonUnit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import ButtonUnit

title0 = None
label1 = None
label0 = None
button_0 = None

def setup():
    global title0, label1, label0, button_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "ButtonUnit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "Button State:", 395, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "Button Counter Value:", 1, 102, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    button_0 = ButtonUnit((33, 32), True, type=2)

def loop():
    global title0, label1, label0, button_0
    M5.update()
    label0.setText(str((str("Button Counter Value:") + str((button_0.count_value)))))

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

    |button_core2_example.m5f2|

## class ButtonUnit

## Constructors

<!-- .. class:: ButtonUnit(pin_num, active_low, pullup_active) -->

    Initialize a Button instance with the specified pin, active-low configuration, and pull-up resistor state.

    :param  pin_num: The GPIO pin number connected to the button.
    :param bool active_low: Determines whether the button signal is active-low. Default is True.
    :param bool pullup_active: Specifies whether the internal pull-up resistor is enabled. Default is True.

    UIFLOW2:

## Methods

<!-- .. method:: ButtonUnit.count_reset() -->

    Reset the count value to zero.

    UIFLOW2:

<!-- .. method:: ButtonUnit.isHolding() -->

    Check if the button is currently being held.

    UIFLOW2:

<!-- .. method:: ButtonUnit.setCallback(type, cb) -->

    Set a callback function for a specified button event type.

    :param  type: The event type (e.g., WAS_CLICKED, WAS_DOUBLECLICKED).
    :param  cb: The callback function to be executed for the event.

    UIFLOW2:

<!-- .. method:: ButtonUnit.tick(pin) -->

    Monitor the state transitions of a button based on its pin state and trigger appropriate handlers.

    UIFLOW2:
