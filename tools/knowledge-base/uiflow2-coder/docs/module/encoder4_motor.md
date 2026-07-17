# 4EncoderMotor Module

4EncoderMotor Module is a 4-channel encoder motor driver module that utilizes the STM32+BL5617 solution. It is suitable for various applications such as robot motion control, automation equipment, smart vehicles, laboratory equipment, and industrial automation systems.

This is the driver library for the 4EncoderMotor Module, use to control motor and read encoder value.

Support the following products:

    4EncoderMotor    4EncoderMotor-V11

## MicroPython Example

#### Motor control

This example shows how to control the motor and read the encoder value.

```python
import os, sys, io
import M5
from M5 import *
from module import Encoder4MotorModule

title0 = None
label0 = None
label1 = None
label2 = None
label3 = None
encoder4_motor_0 = None

def setup():
    global title0, label0, label1, label2, label3, encoder4_motor_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "4EncoderMotor Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 1, 56, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 1, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 1, 144, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 1, 185, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    encoder4_motor_0 = Encoder4MotorModule(address=0x24)
    encoder4_motor_0.set_all_motors_mode(0x02)
    encoder4_motor_0.set_speed_point_value(0x00, 50)
    encoder4_motor_0.set_speed_point_value(0x01, 50)
    encoder4_motor_0.set_speed_point_value(0x02, 50)
    encoder4_motor_0.set_speed_point_value(0x03, 50)

def loop():
    global title0, label0, label1, label2, label3, encoder4_motor_0
    M5.update()
    label0.setText(
        str((str("Motor1 Speed:") + str((encoder4_motor_0.get_motor_speed_value(0x00)))))
    )
    label1.setText(
        str((str("Motor2 Speed:") + str((encoder4_motor_0.get_motor_speed_value(0x01)))))
    )
    label2.setText(
        str((str("Motor3 Speed:") + str((encoder4_motor_0.get_motor_speed_value(0x02)))))
    )
    label3.setText(
        str((str("Motor4 Speed:") + str((encoder4_motor_0.get_motor_speed_value(0x03)))))
    )

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

## **API**

#### Encoder4MotorModule

## `Encoder4MotorModule`
Create an Encoder4MotorModule object

- Parameter `address` (`int`): The I2C address of the device. Default is 0x24.

```python
from module import Encoder4MotorModule

encoder4_motor = Encoder4MotorModule(0x24)
```

### `available`

### `set_motor_mode`
Set the motor mode.

- Parameter `motor` (`int`): The motor to set the mode.
- Parameter `mode` (`int`): The mode of the motor.

    Options:
        - `NORMAL_MODE`: 0
        - `POSITION_MODE`: 1
        - `SPEED_MODE`: 2

```python
encoder4_motor.set_motor_mode(0, encoder4_motor.NORMAL_MODE)
```

### `set_all_motors_mode`
Set the mode of all motors.

- Parameter `mode` (`int`): The mode of the motors.

    Options:
        - `NORMAL_MODE`: 0
        - `POSITION_MODE`: 1
        - `SPEED_MODE`: 2

```python
encoder4_motor.set_all_motors_mode(encoder4_motor.NORMAL_MODE)
```

### `set_motor_pwm_dutycycle`
Set the PWM duty cycle of a motor.

- Parameter `motor` (`int`): The motor to set the PWM duty cycle.
- Parameter `duty` (`int`): The PWM duty cycle.

```python
encoder4_motor.set_motor_pwm_dutycycle(0, 127)
```

### `get_motor_encoder_value`
Get the encoder value of a motor.

- Parameter `pos` (`int`): The motor to get the encoder value.

- Returns: The encoder value.
- Return type: int

```python
encoder4_motor.get_motor_encoder_value(0)
```

### `set_motor_encoder_value`
Set the encoder value of a motor.

- Parameter `pos` (`int`): The motor to set the encoder value.
- Parameter `value` (`int`): The encoder value.

```python
encoder4_motor.set_motor_encoder_value(0, 100)
```

### `get_encoder_mode`
Get the encoder mode.

- Returns: The encoder mode.
- Return type: int

```python
encoder4_motor.get_encoder_mode()
```

### `set_encoder_mode`
Set the encoder mode.

- Parameter `mode` (`int`): The mode of the encoder.

    Options:
        - `AB`: 0
        - `BA`: 1

```python
encoder4_motor.set_encoder_mode(0x00)
```

### `get_motor_speed_value`
Get the speed value of a motor.

- Parameter `pos` (`int`): The motor to get the speed value.

- Returns: The speed value.
- Return type: int

```python
encoder4_motor.get_motor_speed_value(0)
```

### `set_position_encoder_value`
Set the position encoder value of a motor.

- Parameter `pos` (`int`): The motor to set the position encoder value.
- Parameter `value` (`int`): The position encoder value.

```python
encoder4_motor.set_position_encoder_value(0, 100)
```

### `set_position_max_speed_value`
Set the maximum speed value of a motor.

- Parameter `pos` (`int`): The motor to set the maximum speed value.
- Parameter `value` (`int`): The maximum speed value.

```python
encoder4_motor.set_position_max_speed_value(0, 127)
```

### `get_position_pid_value`
Get the position PID value of a motor.

- Parameter `pos` (`int`): The motor to get the position P,I,D value.

- Returns: The position PID value.
- Return type: list[int, int, int]

```python
encoder4_motor.get_position_pid_value(0)
```

### `set_position_pid_value`
Set the position P,I,D value of a motor.

- Parameter `pos` (`int`): The motor to set the position P,I,D value.
- Parameter `p` (`int`): The P value.
- Parameter `i` (`int`): The I value.
- Parameter `d` (`int`): The D value.

```python
encoder4_motor.set_position_pid_value(0, 100, 100, 100)
```

### `get_speed_pid_value`
Get the speed PID value of a motor.

- Parameter `pos` (`int`): The motor to get the speed P,I,D value.

- Returns: The speed P,I,D value.
- Return type: list[int, int, int]

```python
encoder4_motor.get_speed_PID_value(0)
```

### `set_speed_pid_value`
Set the speed PID value of a motor.

- Parameter `pos` (`int`): The motor to set the speed PID value.
- Parameter `p` (`int`): The P value.
- Parameter `i` (`int`): The I value.
- Parameter `d` (`int`): The D value.

```python
encoder4_motor.set_speed_PID_value(0, 100, 100, 100)
```

### `set_speed_point_value`
Set the speed point value of a motor.

- Parameter `pos` (`int`): The motor to set the speed point value.
- Parameter `point` (`int`): The speed point value.

```python
encoder4_motor.set_speed_point_value(0, 127)
```

### `get_vin_current_float_value`
Get the input current value in float.

- Returns: The input current value.
- Return type: float

```python
encoder4_motor.get_vin_current_float_value()
```

### `get_vin_current_int_value`
Get the input current value in int.

- Returns: The input current value.
- Return type: int

```python
encoder4_motor.get_vin_current_int_value()
```

### `get_vin_adc_raw8_value`
Get the input voltage ADC raw value in 8-bit.

- Returns: The input voltage ADC raw value.
- Return type: int

```python
encoder4_motor.get_vin_adc_raw8_value()
```

### `get_vin_adc_raw12_value`
Get the input voltage ADC raw value in 12-bit.

- Returns: The input voltage ADC raw value.
- Return type: int

```python
encoder4_motor.get_vin_adc_raw12_value()
```

### `get_vin_voltage`
Get the input voltage value.

- Returns: The input voltage value.
- Return type: float

```python
encoder4_motor.get_vin_voltage()
```

### `get_device_spec`
Get the device specification.

- Parameter `info` (`int`): The information to get.

- Returns: The device specification(firmware version/I2C address).
- Return type: int

```python
encoder4_motor.get_device_spec(0xFE)
```

### `get_soft_start_state`
Get the soft start state of a motor.

- Parameter `motor` (`int`): The motor to get the soft start state.

- Returns: The soft start state.
- Return type: bool

```python
encoder4_motor.get_soft_start_state(0)
```

### `set_soft_start_state`
Set the soft start state of a motor.

- Parameter `motor` (`int`): The motor to set the soft start state.
- Parameter `state` (`int`): The soft start state.

    Options:
        - `True`: 1
        - `False`: 0

```python
encoder4_motor.set_soft_start_state(0, True)
```

### `set_i2c_address`
Set the I2C address of the device.

- Parameter `addr` (`int`): The I2C address to set.

```python
encoder4_motor.set_i2c_address(0x24)
```
