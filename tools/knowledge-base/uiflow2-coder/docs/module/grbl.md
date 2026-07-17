
# GRBL Module

GRBL 13.2 is a three-axis stepper motor driver module in the M5Stack stacking module series. It uses an ATmega328P-AU controller with three sets of DRV8825PWPR stepper motor driver chip control ways, which can drive three bipolar steppers at the same time.

Support the following products:

GRBLModule

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from module import GRBLModule

grbl_0 = None

def setup():
    global grbl_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    grbl_0 = GRBLModule(address=0x70)
    print(grbl_0.get_message())
    print(grbl_0.get_status())
    print(grbl_0.get_idle_state())
    print(grbl_0.get_lock_state())
    grbl_0.set_mode(GRBLModule.MODE_ABSOLUTE)
    grbl_0.unlock()
    grbl_0.turn(5, 5, 10, 5)
    grbl_0.wait_idle()
    grbl_0.lock()

def loop():
    global grbl_0
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

## class GRBLModule

## Constructors

### `class GRBLModule(address)`

    Initialize the GRBLModule.

    - Parameter `address` (`hex`): The I2C address of the device.

## Methods

### `GRBLModule.g_code(command)`

    Send the G-code command.

    - Parameter `command`: The G-code command.

### `GRBLModule.get_code_time(code)`

    Get the time of the code.

    - Parameter `code`: The G-code command

### `GRBLModule.turn(x, y, z, speed)`

    Turn the motor to a specific position.

    - Parameter `x`: The position of the X motor, 1.6&#x3D;360°.
    - Parameter `y`: The position of the Y motor, 1.6&#x3D;360°.
    - Parameter `z`: The position of the Z motor, 1.6&#x3D;360°.
    - Parameter `speed`: The speed of the motor.

### `GRBLModule.set_mode(mode)`

    Set the mode of the motor.

    - Parameter `mode`: The mode of the motor.
        Options:
        - `Absolute`: GRBLModule.MODE_ABSOLUTE
        - `Relative`: GRBLModule.MODE_RELATIVE

### `GRBLModule.init(x_step, y_step, z_step, acc)`

    Initialize the motor.

    - Parameter `x_step`: The step of the X motor.
    - Parameter `y_step`: The step of the Y motor.
    - Parameter `z_step`: The step of the Z motor.
    - Parameter `acc`: The acceleration of the motor.

### `GRBLModule.flush()`

    Flush the buffer.

### `GRBLModule.get_message()`

    Get the message.

### `GRBLModule.get_status()`

    Get the status.

### `GRBLModule.get_idle_state()`

    Get the idle state.

### `GRBLModule.get_lock_state()`

    Get the lock state.

### `GRBLModule.wait_idle()`

    Wait until the motor is idle.

### `GRBLModule.unlock_alarm_state()`

    Unlock the alarm state.

### `GRBLModule.lock()`

    Lock the motor.

### `GRBLModule.unlock()`

    Unlock the motor.

## Constants

### `GRBLModule.MODE_ABSOLUTE`
### `GRBLModule.MODE_RELATIVE`

    Motor mode
