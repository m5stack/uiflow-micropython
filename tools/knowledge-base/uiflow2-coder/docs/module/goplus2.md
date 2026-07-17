
# GoPlus2Module

Support the following products:

GoPlus2Module

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from module import GoPlus2Module
import time

title0 = None
label0 = None
label1 = None
goplus20 = None

def setup():
    global title0, label0, label1, goplus20

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("GoPlus2 Module Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("Motor Speed:", 2, 72, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Servo Angle:", 2, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    goplus20 = GoPlus2Module(0x38)
    goplus20.set_digital_output(1, 1)
    goplus20.set_digital_output(2, 1)
    goplus20.set_digital_output(3, 1)

def loop():
    global title0, label0, label1, goplus20
    M5.update()
    label0.setText(str((str("Motor Speed:") + str("180"))))
    label1.setText(str((str("Servo Angle:") + str("-127"))))
    goplus20.set_servo_angle(1, 180)
    goplus20.set_servo_angle(2, 180)
    goplus20.set_servo_angle(3, 180)
    goplus20.set_servo_angle(4, 180)
    goplus20.set_motor_speed(1, -127)
    goplus20.set_motor_speed(2, -127)
    time.sleep(4)
    label0.setText(str((str("Motor Speed:") + str("-180"))))
    label1.setText(str((str("Servo Angle:") + str("127"))))
    goplus20.set_servo_angle(1, 0)
    goplus20.set_servo_angle(2, 0)
    goplus20.set_servo_angle(3, 0)
    goplus20.set_servo_angle(4, 127)
    goplus20.set_motor_speed(1, 127)
    time.sleep(4)

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

## class GoPlus2Module

## Constructors

### `class GoPlus2Module(address)`

    Initialize the GoPlus2Module.

    - Parameter `address` (`intlisttuple`): The I2C address of the GoPlus2 module (default is 0x38).

## Methods

### `GoPlus2Module.set_servo_angle(servo_num, angle) -> None`

    Set the angle of the specified servo.

    - Parameter `servo_num` (`int`): The number of the servo (1 to 4).
    - Parameter `angle` (`int`): The angle to set the servo to (0 to 180 degrees).

### `GoPlus2Module.set_servo_pulse_width(servo_num, pulse_width) -> None`

    Set the pulse width for the specified servo.

    - Parameter `servo_num` (`int`): The number of the servo (1 to 4).
    - Parameter `pulse_width` (`int`): The pulse width to set (in microseconds).

### `GoPlus2Module.set_motor_speed(motor_num, speed) -> None`

    Set the speed of the specified motor.

    - Parameter `motor_num` (`int`): The number of the motor (1 or 2).
    - Parameter `speed` (`int`): The speed to set (negative for reverse).

### `GoPlus2Module.set_digital_output(pin_num, value) -> None`

    Set the digital output for the specified pin.

    - Parameter `pin_num` (`int`): The number of the pin (1 to 3).
    - Parameter `value` (`int`): The value to set (0 or 1).

### `GoPlus2Module.get_digital_input(pin_num) -> int`

    Get the digital input value of the specified pin.

    - Parameter `pin_num` (`int`): The number of the pin (1 to 3).

### `GoPlus2Module.get_analog_input(pin_num) -> int`

    Get the analog input value of the specified pin.

    - Parameter `pin_num` (`int`): The number of the pin (1 to 3).
