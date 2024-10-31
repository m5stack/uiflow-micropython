
RollerCAN
==========

.. include:: ../refs/unit.rollercan.ref

Support the following products:

|RollerCAN|

RollerCAN I2C Example:

    .. literalinclude:: ../../../examples/unit/rollercan/rollercan_i2c_fire_example.py
        :language: python
        :linenos:

RollerCAN I2C UIFLOW2 Example:

    |i2c_example.png|

.. only:: builder_html

    |rollercan_i2c_fire_example.m5f2|

RollerCAN CAN Example:

    .. literalinclude:: ../../../examples/unit/rollercan/rollercan_485_fire_example.py
        :language: python
        :linenos:

RollerCAN CAN UIFLOW2 Example:

    |rs485_example.png|

.. only:: builder_html

    |rollercan_485_fire_example.m5f2|

RollerCAN CANToI2C Example:

    .. literalinclude:: ../../../examples/unit/rollercan/rollercan_485toi2c_fire_example.py
        :language: python
        :linenos:

RollerCAN CANToI2C UIFLOW2 Example:

    |rs485_i2c_example.png|

.. only:: builder_html

    |rollercan_485toi2c_fire_example.m5f2|


class RollerCANUnit
-------------------

Constructors
------------

.. class:: RollerCANUnit(bus, address, mode)

    Initialize the RollerCANUnit object based on communication mode.

    :param bus: The I2C/CAN bus instance.
    :param address: The motor's CAN address. Defaults to _ROLLERCAN_CAN_ADDR.
    :param mode: The RollerCAN communication mode.

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


class RollerCAN(RollerBase)
----------------------------

Constructors
------------

.. class:: RollerCAN(bus, address, mode)

    Initialize the RollerCAN object.

    :param bus: The CAN bus instance.
    :param address: The motor's CAN address. Defaults to _ROLLERCAN_CAN_ADDR.
    :param mode: Optional mode for setting specific operational mode.

Methods
-------

.. method:: RollerCAN.create_frame(register, option, data, is_read)

    Create a CAN frame for sending commands.

    :param register: The register for command identification.
    :param option: Command option to specify the data.
    :param data: Data payload for the frame.
    :param is_read: Whether this frame is for a read command.

.. method:: RollerCAN.read(register, length)

    Send a read command to a specific register.

    :param register: The register address to read from.
    :param length: Length of data to read.

.. method:: RollerCAN.i2c_read(register, length)

    Read data from an I2C slave via CAN.

    :param register: The I2C register address to read from.
    :param length: Number of bytes to read.

.. method:: RollerCAN.i2c_write(register, data, stop)

    Write data to an I2C slave via CAN.

    :param register: The I2C register address to write to.
    :param data: The data to write.
    :param stop: Whether to end the transaction with a stop condition.

.. method:: RollerCAN.write(register, data)

    Write data to a specific register.

    :param register: The register address to write to.
    :param data: Data payload to send to the register.

.. method:: RollerCAN.read_response()

    Read the response data from the CAN bus.


class RollerCANToI2CBus(RollerBase)
-----------------------------------

Constructors
------------

.. class:: RollerCANToI2CBus(bus, address, mode)

    Initialize RollerCANToI2CBus object with CAN bus and address.

    :param bus: The CAN bus instance.
    :param address: The I2C device address, default is _ROLLERCAN_I2C_ADDR.
    :param mode: Optional mode for setting specific operational mode.

Methods
-------

.. method:: RollerCANToI2CBus.readfrom_mem(addr, mem_addr, nbytes) -> bytes

    Read data from an I2C memory register.

    :param int addr: I2C device address.
    :param int mem_addr: Memory register address.
    :param int nbytes: Number of bytes to read.

.. method:: RollerCANToI2CBus.readfrom_mem_into(addr, mem_addr, buf) -> None

    Read data from an I2C memory register and store it in the provided buffer.

    :param int addr: I2C device address.
    :param int mem_addr: Memory register address.
    :param bytearray buf: Buffer to store the data.

.. method:: RollerCANToI2CBus.writeto_mem(addr, mem_addr, buf)

    Write data to an I2C memory register.

    :param int addr: I2C device address.
    :param int mem_addr: Memory register address.
    :param bytearray buf: Data to write.

.. method:: RollerCANToI2CBus.readfrom(addr, nbytes) -> bytes

    Read data from an I2C device.

    :param int addr: I2C device address.
    :param int nbytes: Number of bytes to read.

.. method:: RollerCANToI2CBus.readfrom_into(addr, buf) -> None

    Read data from an I2C device and store it in the provided buffer.

    :param int addr: I2C device address.
    :param bytearray buf: Buffer to store the data.

.. method:: RollerCANToI2CBus.writeto(addr, buf, stop)

    Write data to an I2C device in chunks.

    :param int addr: I2C device address.
    :param bytes|bytearray buf: Data to write.
    :param bool stop: Whether to end the transaction with a stop condition.

.. method:: RollerCANToI2CBus.scan() -> list

    Scan for I2C devices on the bus.