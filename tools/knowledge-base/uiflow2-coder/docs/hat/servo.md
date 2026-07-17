# Servo Hat

SERVO HAT as the name suggests, is a servo motor module with the new and
upgraded "ES9251II" digital servo,This comes with 145°±10° range of motion and
can be controlled by PWM signals. The signal pin of the hat is connected to G26
on M5StickC.

Support the following products:

    ServoHat

Micropython Example:
```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from hat import ServoHat
servo = ServoHat((26, 0))
servo.set_duty(100)
servo.set_percent(50)
```

## class ServoHat

## Constructors

### `class ServoHat(port: tuple)`

    Initialize the Servo.

    - Parameter `port` (`tuple`): The port to which the Servo is connected. port[0]: servo pin

## Methods

### `ServoHat.set_duty(duty: int) -> None`

    Set the duty cycle.

    - Parameter `duty` (`int`): The duty cycle. from 26 to 127.

### `ServoHat.set_percent(percent: int) -> None`

    Set the clamping percentage.

    - Parameter `percent` (`int`): The clamping percentage. from 0 to 100.

### `ServoHat.deinit()`

    Deinitialize the Servo.
