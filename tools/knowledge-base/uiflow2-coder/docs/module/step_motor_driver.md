
# StepMotorDriver Module

StepMotor Driver Module 13.2 V1.1 is a stepper motor driver adapted to M5 main control, using STM32+HR8825 stepper motor drive scheme, providing 3-way bipolar stepper motor control interface.

Support the following products:

StepMotorDriverModule

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from module import StepMotorDriverModule
import time

stepmotor_driver_0 = None

DIR = None

def setup():
    global stepmotor_driver_0, DIR

    M5.begin()
    Widgets.fillScreen(0x222222)

    stepmotor_driver_0 = StepMotorDriverModule(
        address=0x27, step_pin=(16, 12, 15), dir_pin=(17, 13, 0)
    )
    print(stepmotor_driver_0.get_all_limit_switch_state())
    print(stepmotor_driver_0.get_limit_switch_state(0))
    print(stepmotor_driver_0.get_fault_io_state(StepMotorDriverModule.MOTOR_X))
    print(stepmotor_driver_0.get_firmware_version())
    stepmotor_driver_0.reset_motor(
        StepMotorDriverModule.MOTOR_X, StepMotorDriverModule.MOTOR_STATE_ENABLE
    )
    stepmotor_driver_0.set_motor_state(StepMotorDriverModule.MOTOR_STATE_ENABLE)
    stepmotor_driver_0.set_microstep(StepMotorDriverModule.STEP_FULL)
    stepmotor_driver_0.set_motor_direction(StepMotorDriverModule.MOTOR_X, 1)
    stepmotor_driver_0.set_motor_pwm_freq(StepMotorDriverModule.MOTOR_X, 1000)
    stepmotor_driver_0.motor_control(StepMotorDriverModule.MOTOR_X, 1)
    DIR = 0

def loop():
    global stepmotor_driver_0, DIR
    M5.update()
    if DIR:
        stepmotor_driver_0.set_motor_direction(StepMotorDriverModule.MOTOR_X, 1)
    else:
        stepmotor_driver_0.set_motor_direction(StepMotorDriverModule.MOTOR_X, 0)
    DIR = not DIR
    time.sleep(2)

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

## class StepMotorDriverModule

## Constructors

### `class StepMotorDriverModule(address, step_pin, dir_pin)`

    Initialize the StepMotorDriverModule.

    - Parameter `address` (`hex`): The I2C address of the device.
    - Parameter `step_pin` (`tuple`): The step pin (X, Y, Z) of the motor.
    - Parameter `dir_pin` (`tuple`): The dir pin (X, Y, Z) of the motor.

## Methods

### `StepMotorDriverModule.reset_motor(motor_id, state)`

    Reset the motor.

    - Parameter `motor_id`: The motor to reset.
        Options:
        - `X`: StepMotorDriverModule.MOTOR_X
        - `Y`: StepMotorDriverModule.MOTOR_Y
        - `Z`: StepMotorDriverModule.MOTOR_Z
    - Parameter `state` (`bool`): The state of the motor.

### `StepMotorDriverModule.set_motor_state(state)`

    Enable or disable the motor.

    - Parameter `state` (`bool`): The state of the motor.

### `StepMotorDriverModule.set_microstep(step)`

    Set the microstep.

    - Parameter `step`: The microstep value.
        Options:
        - `FULL`: StepMotorDriverModule.STEP_FULL
        - `1/2`: StepMotorDriverModule.STEP1_2
        - `1/4`: StepMotorDriverModule.STEP1_4
        - `1/8`: StepMotorDriverModule.STEP1_8
        - `1/16`: StepMotorDriverModule.STEP1_16
        - `1/32`: StepMotorDriverModule.STEP1_32

### `StepMotorDriverModule.set_motor_pwm_freq(motor_id, freq)`

    Set the motor pwm freq.

    - Parameter `motor_id`: The motor to set the freq.
        Options:
        - `X`: StepMotorDriverModule.MOTOR_X
        - `Y`: StepMotorDriverModule.MOTOR_Y
        - `Z`: StepMotorDriverModule.MOTOR_Z
    - Parameter `freq` (`int`): The freq value.

### `StepMotorDriverModule.set_motor_direction(motor_id, direction)`

    Set the motor direction.

    - Parameter `motor_id`: The motor to set the direction.
        Options:
        - `X`: StepMotorDriverModule.MOTOR_X
        - `Y`: StepMotorDriverModule.MOTOR_Y
        - `Z`: StepMotorDriverModule.MOTOR_Z
    - Parameter `direction` (`bool`): The direction value.
        Options:
        - `Positive`: 1
        - `Negative`: 0

### `StepMotorDriverModule.get_all_limit_switch_state()`

    Get all io state.

### `StepMotorDriverModule.get_limit_switch_state(switch_id)`

    Get the io state.

    - Parameter `switch_id` (`int`): The io id.

### `StepMotorDriverModule.get_fault_io_state(motor_id)`

    Get the fault io state.

    - Parameter `motor_id` (`int`): The motor id.
        Options:
        - `X`: StepMotorDriverModule.MOTOR_X
        - `Y`: StepMotorDriverModule.MOTOR_Y
        - `Z`: StepMotorDriverModule.MOTOR_Z

### `StepMotorDriverModule.motor_control(motor_id, state)`

    Control the motor to rotate/stop.

    - Parameter `motor_id`: The motor id.
        Options:
        - `X`: StepMotorDriverModule.MOTOR_X
        - `Y`: StepMotorDriverModule.MOTOR_Y
        - `Z`: StepMotorDriverModule.MOTOR_Z
    - Parameter `state` (`bool`): The state value.
        Options:
        - `Rotate`: 1
        - `Stop`: 0

### `StepMotorDriverModule.get_firmware_version()`

    Get the firmware version.

### `StepMotorDriverModule.set_i2c_address(new_address)`

    Set the i2c address.

    - Parameter `new_address` (`int`): The new address.

## Constants

### `StepMotorDriverModule.MOTOR_X`
### `StepMotorDriverModule.MOTOR_Y`
### `StepMotorDriverModule.MOTOR_Z`

    Motor IDs

### `StepMotorDriverModule.MOTOR_STATE_ENABLE`
### `StepMotorDriverModule.MOTOR_STATE_DISABLE`

    Motor states

### `StepMotorDriverModule.INPUT_REG`
### `StepMotorDriverModule.OUTPUT_REG`
### `StepMotorDriverModule.POLINV_REG`
### `StepMotorDriverModule.CONFIG_REG`
### `StepMotorDriverModule.FAULT_REG`
### `StepMotorDriverModule.RESET_REG`
### `StepMotorDriverModule.FIRM_REG`
### `StepMotorDriverModule.I2C_REG`

    Register addresses

### `StepMotorDriverModule.STEP_FULL`
### `StepMotorDriverModule.STEP1_2`
### `StepMotorDriverModule.STEP1_4`
### `StepMotorDriverModule.STEP1_8`
### `StepMotorDriverModule.STEP1_16`
### `StepMotorDriverModule.STEP1_32`

    Microstep values
