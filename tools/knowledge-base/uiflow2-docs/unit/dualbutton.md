# Dual_Button Unit

<!-- .. include:: ../refs/unit.dual_button.ref -->

Support the following products:

    |Dual_Button|

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import DualButtonUnit

dual_button_0_blue = None
dual_button_0_red = None

def dual_button_0_blue_wasClicked_event(state):  # noqa: N802
    global dual_button_0_blue, dual_button_0_red
    print(dual_button_0_blue.isHolding())

def setup():
    global dual_button_0_blue, dual_button_0_red

    M5.begin()
    Widgets.fillScreen(0x222222)

    dual_button_0_blue, dual_button_0_red = DualButtonUnit((36, 26))
    dual_button_0_blue.setCallback(
        type=dual_button_0_blue.CB_TYPE.WAS_CLICKED, cb=dual_button_0_blue_wasClicked_event
    )
    print(dual_button_0_blue.isHolding())

def loop():
    global dual_button_0_blue, dual_button_0_red
    M5.update()
    dual_button_0_blue.tick(None)

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

    |dual_button_core_example.m5f2|

## class DualButton

## Constructors

<!-- .. class:: DualButton(IO1,IO2) -->

    Create a DualButton object.

    The parameters are:
        - ``IO1,IO2`` Define two key pins.

    UIFLOW2:

## Methods

<!-- .. method:: Dual_Button.isHolding() -->

    The parameters are:

    UIFLOW2:

<!-- .. method:: Dual_Button.setCallback() -->

    Execute the program when the key is pressed.

    UIFLOW2:

<!-- .. method:: Dual_Button.tick() -->

    The polling method, placed in the loop function, constantly detects the state of the key.

    UIFLOW2:
