
# ODrive Module

ODrive is a high-performance servo motor drive module launched by M5Stack, based on the open source motion control solution ODrive.

Support the following products:

ODriveModule

Micropython Example:
```python
import os, sys, io
import M5
from M5 import *
from module import ODriveModule
drive = ODriveModule(port=(13,5))
drive.get_vbus_voltage()
drive.set_velocity(10)
drive.set_current(5)
drive.set_control_mode(ODriveModule.CONTROL_MODE_POSITION_CONTROL)
drive.set_position(1000)
```

## class ODriveModule

## Constructors

### `class ODriveModule(id, port)`

    Initialize the ODriveModule.

    - Parameter `id` (`int`):
    - Parameter `port`:

## Methods

### `ODriveModule.set_position(position, velocity_feedforward, current_feedforward)`

    Set the target position with optional feedforward values.

    - Parameter `position`: The target position in counts or radians, depending on the configuration.
    - Parameter `velocity_feedforward` (`float`): The feedforward velocity in counts/s or radians/s to assist the controller.
    - Parameter `current_feedforward` (`float`): The feedforward current in amperes to assist the controller.

### `ODriveModule.set_velocity(velocity, current_feedforward)`

    Set the target velocity with optional current feedforward.

    - Parameter `velocity`: The target velocity in counts/s or radians/s.
    - Parameter `current_feedforward` (`float`): The feedforward current in amperes to assist the controller.

### `ODriveModule.set_current(current)`

    Set the target current.

    - Parameter `current`: The target current in amperes for torque control.

### `ODriveModule.set_gain(pos_gain, vel_gain, vel_integrator_gain)`

    - Parameter `pos_gain`:
    - Parameter `vel_gain`:
    - Parameter `vel_integrator_gain`:

### `ODriveModule.set_control_mode(mode)`

    Set the control mode of the controller.

    - Parameter `mode`: The control mode.

### `ODriveModule.set_control_input_pos(pos)`

    Set the control input position for the controller.

    - Parameter `pos`: The desired input position in counts or radians for position control.

### `ODriveModule.trapezoidal_move(position)`

    Perform a trapezoidal move to the given position.

    - Parameter `position`: The target position in counts or radians to move to using a trapezoidal velocity profile.

### `ODriveModule.run_state(requested_state, timeout)`

    Run the axis to the requested state within a timeout period.

    - Parameter `requested_state`: The desired axis state to transition to, using the AXIS_STATE_* constants.
    - Parameter `timeout`: Timeout in milliseconds to wait for the axis to reach the requested state.

### `ODriveModule.get_velocity()`

    Get the estimated velocity of the motor.

### `ODriveModule.get_vbus_voltage()`

    Get the measured bus voltage.

### `ODriveModule.get_phase_current()`

    Get the measured phase current of the motor.

### `ODriveModule.get_bus_current()`

    Get the bus current drawn by the motor.

### `ODriveModule.get_encoder_shadow_count()`

    Get the encoder&#x27;s shadow count, which is an internal counter.

### `ODriveModule.get_encoder_pos_estimate()`

    Get the estimated position from the encoder.

### `ODriveModule.get_motor_temp()`

    Get the temperature of the motor thermistor.

### `ODriveModule.erase_config()`

    Erase the current configuration settings.

### `ODriveModule.save_config()`

    Save the current configuration to non-volatile memory.

### `ODriveModule.reboot()`

    Reboot the ODrive device.

### `ODriveModule.set_default_config()`

    Set the default configuration parameters.

### `ODriveModule.check_error()`

    Check for any errors in the system components.

### `ODriveModule.read_flush()`

    Flush the UART read buffer to clear any residual data.

### `ODriveModule.read_string()`

    Read a string terminated by a newline character from the device.

### `ODriveModule.read_float()`

    Read a floating-point value from the device.

### `ODriveModule.read_int()`

    Read an integer value from the device.

### `ODriveModule.write_to_device(data)`

    Write a command string to the device via UART.

    - Parameter `data`: The command string to send to the device, ending with a newline character.

### `ODriveModule.write_config(config, value)`

    Write a configuration parameter to the device.

    - Parameter `config`: The configuration key as a string, e.g., &#x27;axis0.controller.config.pos_gain&#x27;.
    - Parameter `value`: The value to set for the configuration parameter; can be a float or integer.

### `ODriveModule.read_config_int(config)`

    Read an integer configuration parameter from the device.

    - Parameter `config`: The configuration key as a string, e.g., &#x27;axis0.encoder.error&#x27;.

### `ODriveModule.read_config_float(config)`

    Read a floating-point configuration parameter from the device.

    - Parameter `config`: The configuration key as a string, e.g., &#x27;axis0.motor_thermistor.temperature&#x27;.

## Constants

### `ODriveModule.AXIS_STATE_UNDEFINED`
### `ODriveModule.AXIS_STATE_IDLE`
### `ODriveModule.AXIS_STATE_STARTUP_SEQUENCE`
### `ODriveModule.AXIS_STATE_FULL_CALIBRATION_SEQUENCE`
### `ODriveModule.AXIS_STATE_MOTOR_CALIBRATION`
### `ODriveModule.AXIS_STATE_SENSORLESS_CONTROL`
### `ODriveModule.AXIS_STATE_ENCODER_INDEX_SEARCH`
### `ODriveModule.AXIS_STATE_ENCODER_OFFSET_CALIBRATION`
### `ODriveModule.AXIS_STATE_CLOSED_LOOP_CONTROL`

    Axis states

### `ODriveModule.CONTROL_MODE_VOLTAGE_CONTROL`
### `ODriveModule.CONTROL_MODE_TORQUE_CONTROL`
### `ODriveModule.CONTROL_MODE_VELOCITY_CONTROL`
### `ODriveModule.CONTROL_MODE_POSITION_CONTROL`

    Control modes
