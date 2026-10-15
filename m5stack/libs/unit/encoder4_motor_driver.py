# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct
import time
from micropython import const

from .unit_helper import UnitError


_DEFAULT_ADDRESS = const(0x24)

_REG_PWM_DUTY = const(0x20)
_REG_ENCODER_COUNT = const(0x30)
_REG_MOTOR_SPEED = const(0x40)
_REG_MOTOR_CONFIG = const(0x50)
_REG_INPUT_CURRENT = const(0x90)
_REG_INPUT_VOLTAGE_ADC = const(0xB0)
_REG_INPUT_VOLTAGE_MV = const(0xB2)
_REG_RGB_COLOR = const(0xC0)
_REG_RGB_BRIGHTNESS = const(0xC4)
_REG_ENCODER_MODE = const(0xD0)
_REG_SOFT_START = const(0xD1)
_REG_UID = const(0xE0)
_REG_FIRMWARE_VERSION = const(0xFE)
_REG_I2C_ADDRESS = const(0xFF)

_POSITION_PID_OFFSET = const(0x01)
_POSITION_TARGET_OFFSET = const(0x04)
_POSITION_SPEED_LIMIT_OFFSET = const(0x08)
_SPEED_PID_OFFSET = const(0x09)
_SPEED_TARGET_OFFSET = const(0x0C)


def _validate_int(name, value, minimum, maximum):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError("{} must be int".format(name))
    if value < minimum or value > maximum:
        raise ValueError("{} must be {}~{}".format(name, minimum, maximum))
    return value


def _validate_number(name, value, minimum, maximum):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError("{} must be int or float".format(name))
    if value < minimum or value > maximum:
        raise ValueError("{} must be {}~{}".format(name, minimum, maximum))
    return value


class Encoder4MotorDriverUnit:
    """Control the Unit 4EncoderMotor Driver over I2C.

    The Unit supports four motor channels with open-loop PWM, position and speed
    control, encoder feedback, soft start and stop, RGB LED control, and input
    power monitoring. The object borrows the supplied I2C bus and does not
    deinitialize it. If the configured address is not found, check the Unit's
    Grove connection, power supply, and I2C address.

    :param I2C | PAHUBUnit i2c: Initialized I2C bus or compatible PAHUB port.
    :param int address: 7-bit I2C address in the range 0x08~0x77. Defaults to 0x24.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hardware import I2C, Pin
            from unit import Encoder4MotorDriverUnit

            i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
            unit_4enc_motor_driver = Encoder4MotorDriverUnit(i2c0, 0x24)

    Motor channel constants:

    * ``MOTOR_ALL = -1``: apply a setter or action to all four motors in order.
    * ``MOTOR_1 = 0``, ``MOTOR_2 = 1``, ``MOTOR_3 = 2``, ``MOTOR_4 = 3``:
      select one motor. Reading methods accept one channel in the range 0~3.

    Control mode constants:

    * ``MODE_OPEN_LOOP = 0``: open-loop PWM control.
    * ``MODE_POSITION = 1``: position control.
    * ``MODE_SPEED = 2``: speed control.

    Encoder phase constants:

    * ``ENCODER_MODE_AB = 0``: AB phase order.
    * ``ENCODER_MODE_BA = 1``: BA phase order.

    Speed samples and closed-loop speed targets use the device's native values
    in the range -127~127, without a documented RPM conversion. Position speed
    limits use the native range 0~127. Soft start and stop gradually changes PWM
    output to reduce mechanical shock when starting, stopping, or changing speed.
    """

    MOTOR_ALL = const(-1)
    MOTOR_1 = const(0)
    MOTOR_2 = const(1)
    MOTOR_3 = const(2)
    MOTOR_4 = const(3)

    MODE_OPEN_LOOP = const(0)
    MODE_POSITION = const(1)
    MODE_SPEED = const(2)

    ENCODER_MODE_AB = const(0)
    ENCODER_MODE_BA = const(1)

    def __init__(self, i2c, address=_DEFAULT_ADDRESS):
        self._i2c = i2c
        self._address = address
        if self._address not in self._i2c.scan():
            raise UnitError(
                "Please check the Unit 4EncoderMotor Driver connection "
                "(I2C address: 0x{:02X}).".format(address)
            )

    @staticmethod
    def _validate_channel(channel, allow_all=False):
        return _validate_int("channel", channel, -1 if allow_all else 0, 3)

    @staticmethod
    def _validate_mode(mode):
        return _validate_int("mode", mode, 0, 2)

    @staticmethod
    def _validate_pid(kp, ki, kd):
        return (
            _validate_int("kp", kp, 0, 255),
            _validate_int("ki", ki, 0, 255),
            _validate_int("kd", kd, 0, 255),
        )

    @staticmethod
    def _motor_config_register(channel, offset=0):
        return _REG_MOTOR_CONFIG + channel * 0x10 + offset

    def _read(self, register, length):
        return self._i2c.readfrom_mem(self._address, register, length)

    def _write(self, register, data):
        self._i2c.writeto_mem(self._address, register, data)

    def _wait_for_address(self, address):
        for _ in range(20):
            try:
                if address in self._i2c.scan():
                    return
            except OSError:
                pass
            time.sleep_ms(50)
        raise OSError(
            "Unit 4EncoderMotor Driver did not respond at 0x{:02X} after restart".format(address)
        )

    def _set_pid(self, channel, offset, kp, ki, kd):
        channel = self._validate_channel(channel, allow_all=True)
        kp, ki, kd = self._validate_pid(kp, ki, kd)
        data = bytes((kp, ki, kd))
        if channel == self.MOTOR_ALL:
            for motor in range(4):
                self._write(self._motor_config_register(motor, offset), data)
        else:
            self._write(self._motor_config_register(channel, offset), data)

    def _get_pid(self, channel, offset):
        channel = self._validate_channel(channel)
        return tuple(self._read(self._motor_config_register(channel, offset), 3))

    def set_motor_mode(self, channel, mode):
        """Set one motor control mode.

        Args:
            channel (int): Motor channel index. Range: 0~3, or ``MOTOR_ALL`` for all motors.
            mode (int): One of ``MODE_OPEN_LOOP``, ``MODE_POSITION``, or
                ``MODE_SPEED``.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_motor_mode.png|

            |motor_mode_option.png|
        """
        channel = self._validate_channel(channel, allow_all=True)
        mode = self._validate_mode(mode)
        if channel == self.MOTOR_ALL:
            for motor in range(4):
                self._write(self._motor_config_register(motor), bytes((mode,)))
        else:
            self._write(self._motor_config_register(channel), bytes((mode,)))

    def get_motor_mode(self, channel):
        """Get one motor control mode.

        Args:
            channel (int): Motor channel index. Range: 0~3.

        Returns:
            int: Current mode. Range: 0~2.

        UiFlow2 Code Block:

            |get_motor_mode.png|
        """
        channel = self._validate_channel(channel)
        return self._read(self._motor_config_register(channel), 1)[0]

    def set_motor_pwm_duty(self, channel, percent):
        """Set open-loop PWM duty and direction for one motor.

        Args:
            channel (int): Motor channel index. Range: 0~3, or ``MOTOR_ALL`` for all motors.
            percent (int or float): Signed PWM duty. Unit: percent. Range:
                -100~100. The sign selects direction and 0 stops output.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_motor_pwm_duty.png|
        """
        channel = self._validate_channel(channel, allow_all=True)
        percent = _validate_number("percent", percent, -100, 100)
        raw = int(round(percent * 127 / 100))
        data = struct.pack("<b", raw)
        if channel == self.MOTOR_ALL:
            for motor in range(4):
                self._write(_REG_PWM_DUTY + motor, data)
        else:
            self._write(_REG_PWM_DUTY + channel, data)

    def get_motor_pwm_duty(self, channel):
        """Get the commanded open-loop PWM duty for one motor.

        Args:
            channel (int): Motor channel index. Range: 0~3.

        Returns:
            int: Signed commanded PWM duty. Unit: percent. Range: -100~100.

        UiFlow2 Code Block:

            |get_motor_pwm_duty.png|
        """
        channel = self._validate_channel(channel)
        raw = struct.unpack("<b", self._read(_REG_PWM_DUTY + channel, 1))[0]
        return int(round(raw * 100 / 127))

    def read_motor_speed(self, channel):
        """Read the live native speed sample for one motor.

        Args:
            channel (int): Motor channel index. Range: 0~3.

        Returns:
            int: Signed device-native speed sample. Range: -127~127. The
            firmware updates this value every 20 ms. It is not RPM and has no
            verified physical-unit conversion.

        UiFlow2 Code Block:

            |read_motor_speed.png|
        """
        channel = self._validate_channel(channel)
        return struct.unpack("<b", self._read(_REG_MOTOR_SPEED + channel, 1))[0]

    def stop_motor(self, channel):
        """Stop one motor and leave it in open-loop mode.

        PWM is cleared before the mode changes so a previous position or speed
        target cannot resume when open-loop mode becomes active.

        Args:
            channel (int): Motor channel index. Range: 0~3, or ``MOTOR_ALL`` for all motors.

        Returns:
            None.

        UiFlow2 Code Block:

            |stop_motor.png|
        """
        channel = self._validate_channel(channel, allow_all=True)
        self.set_motor_pwm_duty(channel, 0)
        self.set_motor_mode(channel, self.MODE_OPEN_LOOP)

    def enable_soft_start(self, channel):
        """Enable soft start and stop for one motor in open-loop mode.

        The shared setting is retained in the Unit's flash. Repeating the call
        with the channel already enabled does not change the stored value.

        Args:
            channel (int): Motor channel index. Range: 0~3, or ``MOTOR_ALL`` for all motors.

        Returns:
            None.

        UiFlow2 Code Block:

            |enable_soft_start.png|
        """
        channel = self._validate_channel(channel, allow_all=True)
        mask = 0x0F if channel == self.MOTOR_ALL else (1 << channel)
        value = self._read(_REG_SOFT_START, 1)[0] | mask
        self._write(_REG_SOFT_START, bytes((value,)))

    def disable_soft_start(self, channel):
        """Disable soft start and stop for one motor in open-loop mode.

        The shared setting is retained in the Unit's flash. Repeating the call
        with the channel already disabled does not change the stored value.

        Args:
            channel (int): Motor channel index. Range: 0~3, or ``MOTOR_ALL`` for all motors.

        Returns:
            None.

        UiFlow2 Code Block:

            |disable_soft_start.png|
        """
        channel = self._validate_channel(channel, allow_all=True)
        mask = 0x0F if channel == self.MOTOR_ALL else (1 << channel)
        value = self._read(_REG_SOFT_START, 1)[0] & ~mask
        self._write(_REG_SOFT_START, bytes((value,)))

    def is_soft_start_enabled(self, channel):
        """Return whether soft start and stop is enabled for one motor.

        Args:
            channel (int): Motor channel index. Range: 0~3.

        Returns:
            bool: ``True`` when soft start and stop is enabled.

        UiFlow2 Code Block:

            |is_soft_start_enabled.png|
        """
        channel = self._validate_channel(channel)
        return bool(self._read(_REG_SOFT_START, 1)[0] & (1 << channel))

    def read_encoder_count(self, channel):
        """Read one motor encoder count without clearing it.

        Args:
            channel (int): Motor channel index. Range: 0~3.

        Returns:
            int: Signed encoder count. Range: -2147483648~2147483647.

        UiFlow2 Code Block:

            |read_encoder_count.png|
        """
        channel = self._validate_channel(channel)
        return struct.unpack("<i", self._read(_REG_ENCODER_COUNT + channel * 4, 4))[0]

    def set_encoder_count(self, channel, count):
        """Set one motor encoder count.

        Args:
            channel (int): Motor channel index. Range: 0~3, or ``MOTOR_ALL`` for all motors.
            count (int): Signed encoder count. Range:
                -2147483648~2147483647.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_encoder_count.png|
        """
        channel = self._validate_channel(channel, allow_all=True)
        count = _validate_int("count", count, -2147483648, 2147483647)
        data = struct.pack("<i", count)
        if channel == self.MOTOR_ALL:
            for motor in range(4):
                self._write(_REG_ENCODER_COUNT + motor * 4, data)
        else:
            self._write(_REG_ENCODER_COUNT + channel * 4, data)

    def clear_encoder_count(self, channel):
        """Clear one motor encoder count to zero.

        Args:
            channel (int): Motor channel index. Range: 0~3.

        Returns:
            None.

        UiFlow2 Code Block:

            |clear_encoder_count.png|
        """
        self.set_encoder_count(channel, 0)

    def set_encoder_mode(self, mode):
        """Set the global encoder phase order.

        A changed value is retained in the Unit's flash and immediately
        restarts the Unit. The call waits for the current I2C address to become
        available again. Avoid unnecessary calls to limit flash writes.

        Args:
            mode (int): ``ENCODER_MODE_AB`` or ``ENCODER_MODE_BA``.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_encoder_mode.png|

            |encoder_mode_option.png|
        """
        mode = _validate_int("mode", mode, 0, 1)
        if mode == self.get_encoder_mode():
            return
        self._write(_REG_ENCODER_MODE, bytes((mode,)))
        time.sleep_ms(300)
        self._wait_for_address(self._address)

    def get_encoder_mode(self):
        """Get the global encoder phase order.

        Returns:
            int: ``ENCODER_MODE_AB`` or ``ENCODER_MODE_BA``.

        UiFlow2 Code Block:

            |get_encoder_mode.png|
        """
        return self._read(_REG_ENCODER_MODE, 1)[0]

    def set_position_pid(self, channel, kp, ki, kd):
        """Set position-loop PID coefficients for one motor.

        Args:
            channel (int): Motor channel index. Range: 0~3, or ``MOTOR_ALL`` for all motors.
            kp (int): Native proportional coefficient. Range: 0~255.
            ki (int): Native integral coefficient. Range: 0~255.
            kd (int): Native derivative coefficient. Range: 0~255.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_position_pid.png|
        """
        self._set_pid(channel, _POSITION_PID_OFFSET, kp, ki, kd)

    def get_position_pid(self, channel):
        """Get position-loop PID coefficients for one motor.

        Args:
            channel (int): Motor channel index. Range: 0~3.

        Returns:
            tuple: ``(kp, ki, kd)``. Each native coefficient is 0~255.

        UiFlow2 Code Block:

            |get_position_pid.png|
        """
        return self._get_pid(channel, _POSITION_PID_OFFSET)

    def set_position_target_count(self, channel, count):
        """Set the position-loop target in encoder counts.

        Args:
            channel (int): Motor channel index. Range: 0~3, or ``MOTOR_ALL`` for all motors.
            count (int): Signed target. Unit: encoder counts. Range:
                -2147483648~2147483647.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_position_target_count.png|
        """
        channel = self._validate_channel(channel, allow_all=True)
        count = _validate_int("count", count, -2147483648, 2147483647)
        data = struct.pack("<i", count)
        if channel == self.MOTOR_ALL:
            for motor in range(4):
                self._write(self._motor_config_register(motor, _POSITION_TARGET_OFFSET), data)
        else:
            self._write(self._motor_config_register(channel, _POSITION_TARGET_OFFSET), data)

    def get_position_target_count(self, channel):
        """Get the configured position-loop target in encoder counts.

        Args:
            channel (int): Motor channel index. Range: 0~3.

        Returns:
            int: Signed target. Unit: encoder counts. Range:
            -2147483648~2147483647.

        UiFlow2 Code Block:

            |get_position_target_count.png|
        """
        channel = self._validate_channel(channel)
        return struct.unpack(
            "<i",
            self._read(self._motor_config_register(channel, _POSITION_TARGET_OFFSET), 4),
        )[0]

    def set_position_speed_limit(self, channel, speed_limit):
        """Set the native position-loop speed limit.

        Args:
            channel (int): Motor channel index. Range: 0~3, or ``MOTOR_ALL`` for all motors.
            speed_limit (int): Unsigned device-native speed limit. Range: 0~127.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_position_speed_limit.png|
        """
        channel = self._validate_channel(channel, allow_all=True)
        speed_limit = _validate_int("speed_limit", speed_limit, 0, 127)
        data = bytes((speed_limit,))
        if channel == self.MOTOR_ALL:
            for motor in range(4):
                self._write(self._motor_config_register(motor, _POSITION_SPEED_LIMIT_OFFSET), data)
        else:
            self._write(self._motor_config_register(channel, _POSITION_SPEED_LIMIT_OFFSET), data)

    def get_position_speed_limit(self, channel):
        """Get the native position-loop speed limit.

        Args:
            channel (int): Motor channel index. Range: 0~3.

        Returns:
            int: Unsigned, dimensionless device level. Range: 0~127. This
            value is not RPM.

        UiFlow2 Code Block:

            |get_position_speed_limit.png|
        """
        channel = self._validate_channel(channel)
        return self._read(self._motor_config_register(channel, _POSITION_SPEED_LIMIT_OFFSET), 1)[0]

    def set_speed_pid(self, channel, kp, ki, kd):
        """Set speed-loop PID coefficients for one motor.

        Args:
            channel (int): Motor channel index. Range: 0~3, or ``MOTOR_ALL`` for all motors.
            kp (int): Native proportional coefficient. Range: 0~255.
            ki (int): Native integral coefficient. Range: 0~255.
            kd (int): Native derivative coefficient. Range: 0~255.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_speed_pid.png|
        """
        self._set_pid(channel, _SPEED_PID_OFFSET, kp, ki, kd)

    def get_speed_pid(self, channel):
        """Get speed-loop PID coefficients for one motor.

        Args:
            channel (int): Motor channel index. Range: 0~3.

        Returns:
            tuple: ``(kp, ki, kd)``. Each native coefficient is 0~255.

        UiFlow2 Code Block:

            |get_speed_pid.png|
        """
        return self._get_pid(channel, _SPEED_PID_OFFSET)

    def set_speed_target(self, channel, speed):
        """Set the native closed-loop speed target for one motor.

        Args:
            channel (int): Motor channel index. Range: 0~3, or ``MOTOR_ALL`` for all motors.
            speed (int): Signed device-native speed target. Range: -127~127.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_speed_target.png|
        """
        channel = self._validate_channel(channel, allow_all=True)
        speed = _validate_int("speed", speed, -127, 127)
        data = struct.pack("<b", speed)
        if channel == self.MOTOR_ALL:
            for motor in range(4):
                self._write(self._motor_config_register(motor, _SPEED_TARGET_OFFSET), data)
        else:
            self._write(self._motor_config_register(channel, _SPEED_TARGET_OFFSET), data)

    def get_speed_target(self, channel):
        """Get the configured closed-loop speed target.

        Args:
            channel (int): Motor channel index. Range: 0~3.

        Returns:
            int: Signed device-native speed target. Range: -127~127.

        UiFlow2 Code Block:

            |get_speed_target.png|
        """
        channel = self._validate_channel(channel)
        return struct.unpack(
            "<b",
            self._read(self._motor_config_register(channel, _SPEED_TARGET_OFFSET), 1),
        )[0]

    def set_rgb_color(self, color):
        """Set the onboard RGB LED color.

        Args:
            color (int): RGB888 color in ``0xRRGGBB`` format. Range:
                0x000000~0xFFFFFF.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_rgb_color.png|
        """
        color = _validate_int("color", color, 0, 0xFFFFFF)
        self._write(
            _REG_RGB_COLOR,
            bytes((color & 0xFF, (color >> 8) & 0xFF, (color >> 16) & 0xFF)),
        )

    def get_rgb_color(self):
        """Get the onboard RGB LED color.

        Returns:
            int: RGB888 color in ``0xRRGGBB`` format. Range:
            0x000000~0xFFFFFF.

        UiFlow2 Code Block:

            |get_rgb_color.png|
        """
        blue, green, red = self._read(_REG_RGB_COLOR, 3)
        return (red << 16) | (green << 8) | blue

    def set_rgb_brightness(self, percent):
        """Set the onboard RGB LED brightness.

        Args:
            percent (int or float): Brightness. Unit: percent. Range: 0~100.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_rgb_brightness.png|
        """
        percent = _validate_number("percent", percent, 0, 100)
        raw = int(round(percent * 255 / 100))
        self._write(_REG_RGB_BRIGHTNESS, bytes((raw,)))

    def get_rgb_brightness(self):
        """Get the onboard RGB LED brightness.

        Returns:
            int: Brightness. Unit: percent. Range: 0~100.

        UiFlow2 Code Block:

            |get_rgb_brightness.png|
        """
        raw = self._read(_REG_RGB_BRIGHTNESS, 1)[0]
        return int(round(raw * 100 / 255))

    def read_input_voltage(self):
        """Read the motor supply input voltage.

        Returns:
            float: Input voltage. Unit: V. Range depends on the hardware supply.

        UiFlow2 Code Block:

            |read_input_voltage.png|
        """
        voltage_mv = struct.unpack("<H", self._read(_REG_INPUT_VOLTAGE_MV, 2))[0]
        return voltage_mv / 1000.0

    def read_input_voltage_adc(self):
        """Read the raw 12-bit motor-supply voltage ADC sample.

        Returns:
            int: Raw ADC sample. Range: 0~4095. This is not a voltage unit;
            use ``read_input_voltage()`` for volts.

        UiFlow2 Code Block:

            |read_input_voltage_adc.png|
        """
        return struct.unpack("<H", self._read(_REG_INPUT_VOLTAGE_ADC, 2))[0] & 0x0FFF

    def read_input_current(self):
        """Read the total motor supply input current.

        Returns:
            float: Input current. Unit: A. Range depends on the connected load.

        UiFlow2 Code Block:

            |read_input_current.png|
        """
        return struct.unpack("<f", self._read(_REG_INPUT_CURRENT, 4))[0]

    def get_firmware_version(self):
        """Get the Unit firmware version register value.

        Returns:
            int: Firmware version value. Range: 0~255.

        UiFlow2 Code Block:

            |get_firmware_version.png|
        """
        return self._read(_REG_FIRMWARE_VERSION, 1)[0]

    def get_uid(self):
        """Get the device's 12-byte STM32 unique identifier.

        Returns:
            bytes: Device UID with exactly 12 bytes in protocol order.

        UiFlow2 Code Block:

            |get_uid.png|
        """
        return self._read(_REG_UID, 12)

    def get_i2c_address(self):
        """Get the Unit I2C address from the device.

        Returns:
            int: 7-bit I2C address. Range: 0x08~0x77 for public API use.

        UiFlow2 Code Block:

            |get_i2c_address.png|
        """
        return self._read(_REG_I2C_ADDRESS, 1)[0]

    def set_i2c_address(self, address):
        """Set the Unit I2C address and switch this object to it.

        A changed address is retained in the Unit's flash and immediately
        restarts the Unit. The call waits at least 300 ms, then polls the new
        address before updating this object. Avoid unnecessary calls to limit
        flash writes.

        Args:
            address (int): New 7-bit I2C address. Range: 0x08~0x77.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_i2c_address.png|
        """
        address = _validate_int("address", address, 0x08, 0x77)
        if address == self._address:
            return

        old_address = self._address
        self._write(_REG_I2C_ADDRESS, bytes((address,)))
        time.sleep_ms(300)
        try:
            self._wait_for_address(address)
        except OSError:
            raise OSError(
                "Unit 4EncoderMotor Driver did not respond at new address "
                "0x{:02X}; object remains at 0x{:02X}".format(address, old_address)
            )
        self._address = address
