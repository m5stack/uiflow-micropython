
Roller485
==========

.. include:: ../refs/unit.roller485.ref

Support the following products:

|Roller485|

Roller485 I2C Example:

    .. literalinclude:: ../../../examples/unit/roller485/roller485_i2c_fire_example.py
        :language: python
        :linenos:

Roller485 I2C UIFLOW2 Example:

    |i2c_example.png|

.. only:: builder_html

    |roller485_i2c_fire_example.m5f2|

Roller485 RS485 Example:

    .. literalinclude:: ../../../examples/unit/roller485/roller485_485_fire_example.py
        :language: python
        :linenos:

Roller485 RS485 UIFLOW2 Example:

    |rs485_example.png|

.. only:: builder_html

    |roller485_485_fire_example.m5f2|

Roller485 RS485ToI2C Example:

    .. literalinclude:: ../../../examples/unit/roller485/roller485_485toi2c_fire_example.py
        :language: python
        :linenos:

Roller485 RS485ToI2C UIFLOW2 Example:

    |rs485_i2c_example.png|

.. only:: builder_html

    |roller485_485toi2c_fire_example.m5f2|


class Roller485Unit
-------------------

Constructors
------------

.. class:: Roller485Unit(bus, address, mode)

    Initialize the Roller485Unit object based on communication mode.

    :param bus: The I2C/RS485 bus instance.
    :param address: The motor's RS485 address. Defaults to _ROLLER485_RS485_ADDR.
    :param mode: The Roller485 communication mode.

    UIFLOW2:

        |init.png|

class RollerBase
----------------

Constructors
------------

.. class:: RollerBase()


Methods
-------

.. method:: RollerBase.set_motor_output_state(ctrl) -> None

    Set the motor output state.

    :param int ctrl: Control value for the motor output.

    UIFLOW2:

        |set_motor_output_state.png|

.. method:: RollerBase.get_motor_output_state() -> bool

    Get the motor output status.

    :return: True if the motor output is active, False otherwise.

    UIFLOW2:

        |get_motor_output_state.png|

.. method:: RollerBase.set_motor_mode(mode) -> None

    Set the motor mode.

    :param int mode: The mode to set for the motor.

    UIFLOW2:

        |set_motor_mode.png|

.. method:: RollerBase.get_motor_mode() -> int

    Get the motor mode.

    :return: The current motor mode.

    UIFLOW2:

        |get_motor_mode.png|

.. method:: RollerBase.set_motor_over_range_protect_state(state) -> None

    Set the motor over range protection state.

    :param int state: Protection state value (1 to enable, 0 to disable).

    UIFLOW2:

        |set_motor_over_range_protect_state.png|

.. method:: RollerBase.get_motor_over_range_protect_state() -> bool

    Get the motor over range protection status.

    :return: True if protection is enabled, False otherwise.

    UIFLOW2:

        |get_motor_over_range_protect_state.png|

.. method:: RollerBase.remove_motor_jam_protect() -> None

    Set the motor jam release protection.


    UIFLOW2:

        |remove_motor_jam_protect.png|

.. method:: RollerBase.get_motor_status() -> int

    Get the motor status.

    :return: The current status of the motor.

    UIFLOW2:

        |get_motor_status.png|

.. method:: RollerBase.get_motor_error_code() -> int

    Get the motor error code.

    :return: The current error code of the motor.

    UIFLOW2:

        |get_motor_error_code.png|

.. method:: RollerBase.set_button_change_mode(state) -> None

    Set the button change mode.

    :param int state: Change mode state value (1 to enable, 0 to disable).

    UIFLOW2:

        |set_button_change_mode.png|

.. method:: RollerBase.get_button_change_mode() -> int

    Get the button change mode.

    :return: The current button change mode value.

    UIFLOW2:

        |get_button_change_mode.png|

.. method:: RollerBase.set_motor_jam_protect_state(state) -> None

    Set the motor jam protection enable/disable.

    :param int state: Protection state value (1 to enable, 0 to disable).

    UIFLOW2:

        |set_motor_jam_protect_state.png|

.. method:: RollerBase.get_motor_jam_protect_state() -> bool

    Get the motor jam protection status.

    :return: True if jam protection is enabled, False otherwise.

    UIFLOW2:

        |get_motor_jam_protect_state.png|

.. method:: RollerBase.set_motor_id(id) -> None

    Set the motor ID.

    :param int id: The ID to assign to the motor.

    UIFLOW2:

        |set_motor_id.png|

.. method:: RollerBase.get_motor_id() -> int

    Get the motor ID.

    :return: The current motor ID.

    UIFLOW2:

        |get_motor_id.png|

.. method:: RollerBase.set_485_baudrate(bps) -> None

    Set the 485 baudrate.

    :param int bps: Baud rate value.

    UIFLOW2:

        |set_485_baudrate.png|

.. method:: RollerBase.get_485_baudrate() -> int

    Get the 485 baudrate.

    :return: The current 485 baudrate.

    UIFLOW2:

        |get_485_baudrate.png|

.. method:: RollerBase.set_rgb_brightness(bright) -> None

    Set RGB brightness.

    :param int bright: Brightness value.

    UIFLOW2:

        |set_rgb_brightness.png|

.. method:: RollerBase.get_rgb_brightness() -> int

    Get RGB brightness.

    :return: The current RGB brightness value.

    UIFLOW2:

        |get_rgb_brightness.png|

.. method:: RollerBase.set_motor_speed(speed) -> None

    Set the motor speed and max current setting.

    :param int speed: The speed value to set.

    UIFLOW2:

        |set_motor_speed.png|

.. method:: RollerBase.get_motor_speed() -> int

    Get the motor speed and max current setting.

    :return: The current motor speed.

    UIFLOW2:

        |get_motor_speed.png|

.. method:: RollerBase.set_speed_max_current(current) -> None

    Set the motor speed and max current setting.

    :param int current: The max current value to set.

    UIFLOW2:

        |set_speed_max_current.png|

.. method:: RollerBase.get_speed_max_current() -> int

    Get the motor speed and max current setting.

    :return: The current max current setting.

    UIFLOW2:

        |get_speed_max_current.png|

.. method:: RollerBase.get_motor_speed_readback() -> float

    Get the motor speed readback.

    :return: The readback value of the motor speed.

    UIFLOW2:

        |get_motor_speed_readback.png|

.. method:: RollerBase.set_motor_speed_pid(p, i, d) -> None

    Set the motor speed PID.

    :param float p: Proportional gain.
    :param float i: Integral gain.
    :param float d: Derivative gain.

    UIFLOW2:

        |set_motor_speed_pid.png|

.. method:: RollerBase.get_motor_speed_pid() -> tuple

    Get the motor speed PID.

    :return: A tuple containing the PID values.

    UIFLOW2:

        |get_motor_speed_pid.png|

.. method:: RollerBase.set_motor_position(position) -> None

    Set the motor position and max current setting.

    :param int position: The position value to set.

    UIFLOW2:

        |set_motor_position.png|

.. method:: RollerBase.get_motor_position() -> int

    Get the motor position and max current setting.

    :return: The current motor position.

    UIFLOW2:

        |get_motor_position.png|

.. method:: RollerBase.set_position_max_current(current) -> None

    Set the motor position and max current setting.

    :param int current: The max current value to set.

    UIFLOW2:

        |set_position_max_current.png|

.. method:: RollerBase.get_position_max_current() -> int

    Get the motor position and max current setting.

    :return: The current max current setting.

    UIFLOW2:

        |get_position_max_current.png|

.. method:: RollerBase.get_motor_position_readback() -> float

    Get the motor position readback.

    :return: The readback value of the motor position.

    UIFLOW2:

        |get_motor_position_readback.png|

.. method:: RollerBase.get_motor_position_pid() -> tuple

    Get the motor position PID.

    :return: A tuple containing the PID values for position.

    UIFLOW2:

        |get_motor_position_pid.png|

.. method:: RollerBase.set_motor_position_pid(p, i, d) -> None

    Set the motor position PID.

    :param float p: Proportional gain.
    :param float i: Integral gain.
    :param float d: Derivative gain.

    UIFLOW2:

        |set_motor_position_pid.png|

.. method:: RollerBase.set_motor_max_current(current) -> None

    Set the motor max current.

    :param int current: The maximum current for the motor, multiplied by 100 before sending.

    UIFLOW2:

        |set_motor_max_current.png|

.. method:: RollerBase.get_motor_max_current() -> int

    Get the motor max current.

    :return: The motor max current, divided by 100 after reading.

    UIFLOW2:

        |get_motor_max_current.png|

.. method:: RollerBase.get_motor_current_readback() -> float

    Get the motor current readback.

    :return: The motor current readback value, divided by 100 after reading.

    UIFLOW2:

        |get_motor_current_readback.png|

.. method:: RollerBase.set_rgb_color(rgb) -> None

    Set the system RGB color.

    :param int rgb: The RGB color value, where the format is 0xRRGGBB.

    UIFLOW2:

        |set_rgb_color.png|

.. method:: RollerBase.get_rgb_color() -> tuple

    Get the system RGB color.

    :return: The RGB color as a tuple (R, G, B).

    UIFLOW2:

        |get_rgb_color.png|

.. method:: RollerBase.set_rgb_mode(mode) -> None

    Set the system RGB mode.

    :param int mode: The RGB mode value.

    UIFLOW2:

        |set_rgb_mode.png|

.. method:: RollerBase.get_rgb_mode() -> int

    Get the system RGB mode.

    :return: The current RGB mode value.

    UIFLOW2:

        |get_rgb_mode.png|

.. method:: RollerBase.get_vin_voltage() -> int

    Get the system VIN voltage.

    :return: The system VIN voltage value, multiplied by 10 after reading.

    UIFLOW2:

        |get_vin_voltage.png|

.. method:: RollerBase.get_temperature_value() -> int

    Get the system temperature.

    :return: The current system temperature value.

    UIFLOW2:

        |get_temperature_value.png|

.. method:: RollerBase.set_encoder_value(count) -> None

    Set the system encoder value.

    :param int count: The encoder count value.

    UIFLOW2:

        |set_encoder_value.png|

.. method:: RollerBase.get_encoder_value() -> int

    Get the system encoder value.

    :return: The current encoder value.

    UIFLOW2:

        |get_encoder_value.png|

.. method:: RollerBase.save_param_to_flash() -> None

    Save the motor data to flash.


    UIFLOW2:

        |save_param_to_flash.png|

.. method:: RollerBase.get_firmware_version() -> int

    Get the device firmware version.

    :return: The current firmware version.

    UIFLOW2:

        |get_firmware_version.png|

.. method:: RollerBase.set_i2c_address(addr) -> None

    Set the I2C address.

    :param int addr: The new I2C address. Must be between 0x08 and 0x77.

    UIFLOW2:

        |set_i2c_address.png|

.. method:: RollerBase.get_i2c_address() -> int

    Get the current I2C address.

    :return: The current I2C address.

    UIFLOW2:

        |get_i2c_address.png|


class RollerI2C(RollerBase)
---------------------------

Constructors
------------

.. class:: RollerI2C(i2c, address)

    Initialize the RollerI2C object.

    :param I2C|PAHUBUnit i2c: I2C bus instance or PAHUBUnit instance.
    :param int address: I2C address of the device. Defaults to _ROLLER485_I2C_ADDR.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: RollerI2C.read(register, length) -> bytes

    Read data from a specified register on the I2C device.

    :param register: The name of the register to read from.
    :param length: The number of bytes to read.
    :return: The data read from the device as a bytes object.

.. method:: RollerI2C.write(register, bytes) -> None

    Write data to a specified register on the I2C device.

    :param register: The name of the register to write to.
    :param bytes: The data to write to the register as a bytes object.


class Roller485(RollerBase)
----------------------------

Constructors
------------

.. class:: Roller485(bus, address)

    Initialize the Roller485 object.

    :param bus: The RS485 bus instance.
    :param int address: The motor's RS485 address. Defaults to _ROLLER485_RS485_ADDR.

Methods
-------

.. method:: Roller485.read(register, length) -> bytes

    Read data from a specified register via RS485.

    :param register: The name of the register to read from.
    :param length: The number of bytes to read.


.. method:: Roller485.create_frame(cmd, motor_id, *datas) -> None

    Create a command frame with the given command and motor ID.

    :param cmd: The command byte.
    :param motor_id: The ID of the motor.
    :param datas: Additional data bytes to include in the frame.

.. method:: Roller485.write(register, bytes) -> bool

    Write data to a specified register via RS485.

    :param register: The name of the register to write to.
    :param bytes: The data to write to the register as a bytes object.
    :return: The response after writing the data.

.. method:: Roller485.send_command(cmd, id, data, buf_len) -> bool

    Send a command via RS485.

    :param cmd: The command byte.
    :param id: The motor ID.
    :param data: The data to send along with the command.
    :param buf_len: The length of the buffer.


.. method:: Roller485.read_response(cmd, id) -> tuple[Literal[True], Any]

    Send a command via RS485.

    :param cmd: The command byte.
    :param id: The motor ID.
    :return: A tuple (success, response). Success is True if the response is valid, and response is the data read.

.. method:: Roller485._crc8(buffer) -> int

    Calculate CRC8 checksum.

    :param buffer: The data buffer to compute the checksum for.
    :return: The computed CRC8 value.


class Roller485ToI2CBus(RollerBase)
-----------------------------------

Constructors
------------

.. class:: Roller485ToI2CBus(bus, address, mode)

    Initialize the Roller485ToI2CBus object.

    :param bus: The RS485 bus instance.
    :param address: The motor's RS485 address. Defaults to _ROLLER485_RS485_ADDR.

Methods
-------

.. method:: Roller485ToI2CBus.readfrom_mem(addr, mem_addr, nbytes) -> bytes

    Read data from a specific register of the I2C slave device.

    :param addr: The I2C slave address to read from.
    :param mem_addr: Memory register address.
    :param nbytes: The number of bytes to read.
    :return: The data read from the register.
    :throws Exception: If the read operation fails.

.. method:: Roller485ToI2CBus.readfrom_mem_into(addr, mem_addr, buf)

    Read data from a specific register of the I2C slave device.

    :param addr: The I2C slave address to read from.
    :param mem_addr: Memory register address.
    :param buf: Buffer to store the data.

.. method:: Roller485ToI2CBus.writeto_mem(addr, mem_addr, buf) -> Literal[True]

    Write data to a specific register of the I2C slave device.

    :param addr: The I2C slave address to write to.
    :param mem_addr: Memory register address.
    :param buf: The data bytes to write.
    :return: True if the write operation is successful.
    :throws Exception: If the write operation fails.

.. method:: Roller485ToI2CBus.readfrom(addr, nbytes) -> bytes

    Read data from the I2C slave device via RS485.

    :param addr: The I2C slave address to read from.
    :param nbytes: The number of bytes to read.
    :return: The data read from the I2C slave.
    :throws Exception: If the read operation fails.

.. method:: Roller485ToI2CBus.readfrom_into(addr, buf)

    Read data from the I2C slave device via RS485.

    :param addr: I2C device address.
    :param buf: Buffer to store the data.

.. method:: Roller485ToI2CBus.writeto(addr, buf, stop) -> Literal[True]

    Write data to the I2C slave device via RS485.

    :param addr: The I2C slave address to write to.
    :param buf: The data bytes to write.
    :param stop: Whether to send a stop bit after writing.
    :return: True if the write operation is successful.
    :throws Exception: If the write operation fails.


.. method:: Roller485ToI2CBus.scan(addr, buf, stop) -> List

    Scan for I2C devices on the bus.

    :return: A list of addresses of the found I2C devices.