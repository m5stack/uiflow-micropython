
ODrive Module
============

.. include:: ../refs/module.odrive.ref

ODrive is a high-performance servo motor drive module launched by M5Stack, based on the open source motion control solution ODrive.

Support the following products:

|ODriveModule|

Micropython Example::

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


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |core_odrive_example.m5f2|


class ODriveModule
------------------

Constructors
------------

.. class:: ODriveModule(id, port)

    Initialize the ODriveModule.

    :param int id: 
    :param  port: 

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ODriveModule.set_position(position, velocity_feedforward, current_feedforward)

    Set the target position with optional feedforward values.

    :param  position: The target position in counts or radians, depending on the configuration.
    :param float velocity_feedforward: The feedforward velocity in counts/s or radians/s to assist the controller.
    :param float current_feedforward: The feedforward current in amperes to assist the controller.

    UIFLOW2:

        |set_position.png|

.. method:: ODriveModule.set_velocity(velocity, current_feedforward)

    Set the target velocity with optional current feedforward.

    :param  velocity: The target velocity in counts/s or radians/s.
    :param float current_feedforward: The feedforward current in amperes to assist the controller.

    UIFLOW2:

        |set_velocity.png|

.. method:: ODriveModule.set_current(current)

    Set the target current.

    :param  current: The target current in amperes for torque control.

    UIFLOW2:

        |set_current.png|

.. method:: ODriveModule.set_gain(pos_gain, vel_gain, vel_integrator_gain)


    :param  pos_gain: 
    :param  vel_gain: 
    :param  vel_integrator_gain: 

    UIFLOW2:

        |set_gain.png|

.. method:: ODriveModule.set_control_mode(mode)

    Set the control mode of the controller.

    :param  mode: The control mode.

    UIFLOW2:

        |set_control_mode.png|

.. method:: ODriveModule.set_control_input_pos(pos)

    Set the control input position for the controller.

    :param  pos: The desired input position in counts or radians for position control.

    UIFLOW2:

        |set_control_input_pos.png|

.. method:: ODriveModule.trapezoidal_move(position)

    Perform a trapezoidal move to the given position.

    :param  position: The target position in counts or radians to move to using a trapezoidal velocity profile.

    UIFLOW2:

        |trapezoidal_move.png|

.. method:: ODriveModule.run_state(requested_state, timeout)

    Run the axis to the requested state within a timeout period.

    :param  requested_state: The desired axis state to transition to, using the AXIS_STATE_* constants.
    :param  timeout: Timeout in milliseconds to wait for the axis to reach the requested state.

    UIFLOW2:

        |run_state.png|

.. method:: ODriveModule.get_velocity()

    Get the estimated velocity of the motor.

    :return (float): The estimated velocity in counts/s or radians/s.

    UIFLOW2:

        |get_velocity.png|

.. method:: ODriveModule.get_vbus_voltage()

    Get the measured bus voltage.

    :return (float): The bus voltage in volts.

    UIFLOW2:

        |get_vbus_voltage.png|

.. method:: ODriveModule.get_phase_current()

    Get the measured phase current of the motor.

    :return (float): The phase current in amperes.

    UIFLOW2:

        |get_phase_current.png|

.. method:: ODriveModule.get_bus_current()

    Get the bus current drawn by the motor.

    :return (float): The bus current in amperes.

    UIFLOW2:

        |get_bus_current.png|

.. method:: ODriveModule.get_encoder_shadow_count()

    Get the encoder&#x27;s shadow count, which is an internal counter.

    :return (int): The shadow count as an integer value.

    UIFLOW2:

        |get_encoder_shadow_count.png|

.. method:: ODriveModule.get_encoder_pos_estimate()

    Get the estimated position from the encoder.

    :return (float): The estimated position in counts or radians.

    UIFLOW2:

        |get_encoder_pos_estimate.png|

.. method:: ODriveModule.get_motor_temp()

    Get the temperature of the motor thermistor.

    :return (float): The motor temperature in degrees Celsius.

    UIFLOW2:

        |get_motor_temp.png|

.. method:: ODriveModule.erase_config()

    Erase the current configuration settings.


    UIFLOW2:

        |erase_config.png|

.. method:: ODriveModule.save_config()

    Save the current configuration to non-volatile memory.


    UIFLOW2:

        |save_config.png|

.. method:: ODriveModule.reboot()

    Reboot the ODrive device.


    UIFLOW2:

        |reboot.png|

.. method:: ODriveModule.set_default_config()

    Set the default configuration parameters.


    UIFLOW2:

        |set_default_config.png|

.. method:: ODriveModule.check_error()

    Check for any errors in the system components.


    UIFLOW2:

        |check_error.png|

.. method:: ODriveModule.read_flush()

    Flush the UART read buffer to clear any residual data.


    UIFLOW2:

        |read_flush.png|

.. method:: ODriveModule.read_string()

    Read a string terminated by a newline character from the device.

    :return (str): The string read from the device, excluding the newline character.

    UIFLOW2:

        |read_string.png|

.. method:: ODriveModule.read_float()

    Read a floating-point value from the device.

    :return (float): The float value read from the device; returns 0.0 if parsing fails.

    UIFLOW2:

        |read_float.png|

.. method:: ODriveModule.read_int()

    Read an integer value from the device.

    :return (int): The integer value read from the device; returns 0 if parsing fails.

    UIFLOW2:

        |read_int.png|

.. method:: ODriveModule.write_to_device(data)

    Write a command string to the device via UART.

    :param  data: The command string to send to the device, ending with a newline character.

    UIFLOW2:

        |write_to_device.png|

.. method:: ODriveModule.write_config(config, value)

    Write a configuration parameter to the device.

    :param  config: The configuration key as a string, e.g., &#x27;axis0.controller.config.pos_gain&#x27;.
    :param  value: The value to set for the configuration parameter; can be a float or integer.

    UIFLOW2:

        |write_config.png|

.. method:: ODriveModule.read_config_int(config)

    Read an integer configuration parameter from the device.

    :return (int): The integer value of the specified configuration parameter; returns 0 if parsing fails.
    :param  config: The configuration key as a string, e.g., &#x27;axis0.encoder.error&#x27;.

    UIFLOW2:

        |read_config_int.png|

.. method:: ODriveModule.read_config_float(config)

    Read a floating-point configuration parameter from the device.

    :return (float): The float value of the specified configuration parameter; returns 0.0 if parsing fails.
    :param  config: The configuration key as a string, e.g., &#x27;axis0.motor_thermistor.temperature&#x27;.

    UIFLOW2:

        |read_config_float.png|



Constants
---------

.. data:: ODriveModule.AXIS_STATE_UNDEFINED
.. data:: ODriveModule.AXIS_STATE_IDLE
.. data:: ODriveModule.AXIS_STATE_STARTUP_SEQUENCE
.. data:: ODriveModule.AXIS_STATE_FULL_CALIBRATION_SEQUENCE
.. data:: ODriveModule.AXIS_STATE_MOTOR_CALIBRATION
.. data:: ODriveModule.AXIS_STATE_SENSORLESS_CONTROL
.. data:: ODriveModule.AXIS_STATE_ENCODER_INDEX_SEARCH
.. data:: ODriveModule.AXIS_STATE_ENCODER_OFFSET_CALIBRATION
.. data:: ODriveModule.AXIS_STATE_CLOSED_LOOP_CONTROL

    Axis states

    
.. data:: ODriveModule.CONTROL_MODE_VOLTAGE_CONTROL
.. data:: ODriveModule.CONTROL_MODE_TORQUE_CONTROL
.. data:: ODriveModule.CONTROL_MODE_VELOCITY_CONTROL
.. data:: ODriveModule.CONTROL_MODE_POSITION_CONTROL

    Control modes

    
