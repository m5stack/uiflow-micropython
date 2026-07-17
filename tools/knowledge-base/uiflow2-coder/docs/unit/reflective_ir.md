# Reflective IR Unit

Support the following products:

    Reflective IR Unit

Micropython Example:

```python
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

## class ReflectiveIRUnit

## Constructors

### `class ReflectiveIRUnit(port: tuple)`

    Create a ReflectiveIRUnit object.

    - Parameter `port` (`tuple`): Specify the port to which the Reflective IR Unit is connected.

## Methods

### `ReflectiveIRUnit.get_analog_value() -> int`

    This method allows read the ADC value of the Reflective IR Unit and return an integer value. The value ranges from 0 to 65535.

### `ReflectiveIRUnit.get_digital_value() -> int`

    This method allows read the digital value of the Reflective IR Unit and return an integer value. The value ranges from 0 to 1.

### `ReflectiveIRUnit.enable_irq() -> None`

   Enable Obstacle detection event

### `ReflectiveIRUnit.disable_irq() -> None`

    Disable Obstacle detection event

### `ReflectiveIRUnit.set_callback(handler, trigger=ReflectiveIRUnit.EVENT_DETECTED | ReflectiveIRUnit.EVENT_NOT_DETECTED) -> None`

    Set the callback function for the Reflective IR Unit.

    - Parameter `handler`: The callback function to be set.
    - Parameter `trigger`: The trigger condition for the callback function.

## Constants

### `ReflectiveIRUnit.EVENT_DETECTED`
          ReflectiveIRUnit.EVENT_NOT_DETECTED

    select the EVENT type of the Reflective IR Unit.
