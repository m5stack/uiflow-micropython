# Dual Button Unit

The Dual Button Unit provides two independent buttons. Use `DualButtonUnit`
for click, double-click, hold, and callback handling, or
`SimpleDualButtonUnit` for direct pin reads and debounced edge polling.

Support the following products:

    Dual_Button

## MicroPython Example

#### Button events and callbacks

This example demonstrates how to use `DualButtonUnit` for button state,
click, hold, and callback handling.

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

Example output:

    The button state is printed when the blue button event occurs.

#### Simple polling

This example demonstrates how to use `SimpleDualButtonUnit` to read the
pins directly and poll debounced press and release edges without `tick()`
or callbacks.

```python
import os, sys, io
import time

import M5
from M5 import *
from unit import SimpleDualButtonUnit

blue = None
red = None

def setup():
    global blue, red

    M5.begin()
    Widgets.fillScreen(0x222222)

    blue, red = SimpleDualButtonUnit((36, 26))

def loop():
    global blue, red
    M5.update()
    blue.update()
    red.update()

    if blue.was_pressed():
        print("blue pressed, pin value:", blue.value())
    if blue.was_released():
        print("blue released, active:", blue.is_active())

    if red.was_pressed():
        print("red pressed, pin value:", red.value())
    if red.was_released():
        print("red released, active:", red.is_active())

    time.sleep_ms(10)

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

    Press and release events for the blue and red buttons are printed.

## **API**

#### DualButtonUnit

### `DualButtonUnit(port)`

    Create two full-featured button objects.

    - Parameter `port` (`tuple`): Two button pin numbers.
    - Returns: The blue and red `hardware.Button` objects.
    - Return type: tuple

### `Dual_Button.isHolding()`

    Return whether the button is currently being held.

### `Dual_Button.setCallback(type, cb)`

    Register a callback for the specified button event.

    - Parameter `type` (`int`): Button event type.
    - Parameter `cb` (`callable`): Function called when the event occurs.

### `Dual_Button.tick(pin)`

    Poll the button state machine. Call this method regularly in the loop.

    - Parameter `pin`: Optional pin argument passed by an interrupt handler. Use
        `None` when polling from the loop.

#### SimpleDualButtonUnit

### `SimpleDualButtonUnit(port, active_low=True, debounce_ms=50)`

    Create two `SimpleButton` objects for direct polling.

    - Parameter `port` (`tuple`): Two button pin numbers.
    - Parameter `active_low` (`bool`): Use low level as the active state when `True`.
        Active-low inputs use an internal pull-up and active-high inputs use
        an internal pull-down.
    - Parameter `debounce_ms` (`int`): Time in milliseconds that an input must remain
        stable before generating an edge event. Set to `0` to disable
        debounce.
    - Returns: The blue and red button objects.
    - Return type: tuple

#### SimpleButton

### `class SimpleButton(pin_num, active_low=True, debounce_ms=50)`

    Provide direct pin reads and debounced edge polling without callbacks.

    Call `SimpleButton.update` regularly before reading edge events.
    The `SimpleButton.value` and `SimpleButton.is_active` methods
    read the pin directly and do not require `update()`.

### `SimpleButton.value()`

        Return the raw pin value.

        - Returns: `0` or `1`.
        - Return type: int

### `SimpleButton.is_active()`

        Return whether the button is currently active according to
        `active_low`.

        - Returns: `True` when the button is active.
        - Return type: bool

### `SimpleButton.update()`

        Sample the pin and update the debounced edge state. Call this method
        once per loop iteration.

### `SimpleButton.was_pressed()`

        Return whether a debounced press was detected by the latest call to
        `SimpleButton.update`.

        - Return type: bool

### `SimpleButton.was_released()`

        Return whether a debounced release was detected by the latest call to
        `SimpleButton.update`.

        - Return type: bool
