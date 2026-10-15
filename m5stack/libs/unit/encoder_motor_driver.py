# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import struct
import time
from micropython import const

from .unit_helper import UnitError


_DEFAULT_ADDRESS = const(0x2F)

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
_REG_MOTOR_SLEEP = const(0xD2)
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


class EncoderMotorDriverUnit:
    """Control the Unit EncoderMotor Driver over I2C.

    The Unit supports signed open-loop PWM, position and speed control, encoder
    feedback, motor sleep, soft start and stop, RGB LED control, and input power
    monitoring. The object borrows the supplied I2C bus and does not deinitialize
    it. If the configured address is not found, check the Unit's Grove connection,
    power supply, and I2C address.

    :param I2C | PAHUBUnit i2c: Initialized I2C bus or compatible PAHUB port.
    :param int address: 7-bit I2C address in the range 0x08~0x77. Defaults to 0x2F.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hardware import I2C, Pin
            from unit import EncoderMotorDriverUnit

            i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
            encodermotordriver_0 = EncoderMotorDriverUnit(i2c0, 0x2F)

    Control mode constants:

    * ``MODE_OPEN_LOOP = 0``: open-loop PWM control.
    * ``MODE_POSITION = 1``: position control.
    * ``MODE_SPEED = 2``: speed control.

    Encoder phase constants:

    * ``ENCODER_MODE_AB = 0``: AB phase order.
    * ``ENCODER_MODE_BA = 1``: BA phase order.
    """

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
                "Please check the Unit EncoderMotor Driver connection "
                "(I2C address: 0x{:02X}).".format(address)
            )

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
        raise OSError("Unit EncoderMotor Driver did not respond at 0x{:02X}".format(address))

    def _set_pid(self, offset, kp, ki, kd):
        kp, ki, kd = self._validate_pid(kp, ki, kd)
        self._write(_REG_MOTOR_CONFIG + offset, bytes((kp, ki, kd)))

    def _get_pid(self, offset):
        return tuple(self._read(_REG_MOTOR_CONFIG + offset, 3))

    def set_motor_mode(self, mode):
        """Set the motor control mode.

        Args:
            mode (int): One of ``MODE_OPEN_LOOP``, ``MODE_POSITION``, or
                ``MODE_SPEED``.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_motor_mode.png|

            |motor_mode_option.png|
        """
        mode = self._validate_mode(mode)
        self._write(_REG_MOTOR_CONFIG, bytes((mode,)))

    def get_motor_mode(self):
        """Get the current motor control mode.

        Returns:
            int: Current mode. Range: 0~2.

        UiFlow2 Code Block:

            |get_motor_mode.png|
        """
        return self._read(_REG_MOTOR_CONFIG, 1)[0]

    def set_motor_pwm_duty(self, percent):
        """Set the signed open-loop motor PWM duty.

        Args:
            percent (int or float): Signed duty. Unit: percent. Range:
                -100~100. The sign selects the direction.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_motor_pwm_duty.png|
        """
        percent = _validate_number("percent", percent, -100, 100)
        raw = int(round(percent * 127 / 100))
        self._write(_REG_PWM_DUTY, struct.pack("<b", raw))

    def get_motor_pwm_duty(self):
        """Get the motor PWM value as a signed percentage.

        In open-loop mode this is the commanded PWM duty. In a closed-loop
        mode the firmware may update the register with its live motor output.

        Returns:
            int: Signed PWM duty. Unit: percent. Range: -100~100.

        UiFlow2 Code Block:

            |get_motor_pwm_duty.png|
        """
        raw = struct.unpack("<b", self._read(_REG_PWM_DUTY, 1))[0]
        return int(round(raw * 100 / 127))

    def read_motor_speed(self):
        """Read the live device-native motor speed sample.

        Returns:
            int: Signed native speed sample. Range: -127~127. The firmware
            updates this value every 20 ms. It is not RPM and has no verified
            physical-unit conversion.

        UiFlow2 Code Block:

            |read_motor_speed.png|
        """
        return struct.unpack("<b", self._read(_REG_MOTOR_SPEED, 1))[0]

    def stop_motor(self):
        """Stop the motor and leave it in open-loop mode.

        The method clears PWM before and after changing the mode so a previous
        closed-loop output cannot remain active after the mode transition.

        Returns:
            None.

        UiFlow2 Code Block:

            |stop_motor.png|
        """
        self.set_motor_pwm_duty(0)
        self.set_motor_mode(self.MODE_OPEN_LOOP)
        self.set_motor_pwm_duty(0)

    def read_encoder_count(self):
        """Read the current encoder count without clearing it.

        Returns:
            int: Signed encoder count. Range: -2147483648~2147483647.

        UiFlow2 Code Block:

            |read_encoder_count.png|
        """
        return struct.unpack("<i", self._read(_REG_ENCODER_COUNT, 4))[0]

    def set_encoder_count(self, count):
        """Set the current encoder count.

        Args:
            count (int): Signed encoder count. Range:
                -2147483648~2147483647.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_encoder_count.png|
        """
        count = _validate_int("count", count, -2147483648, 2147483647)
        self._write(_REG_ENCODER_COUNT, struct.pack("<i", count))

    def clear_encoder_count(self):
        """Clear the encoder count to zero.

        Returns:
            None.

        UiFlow2 Code Block:

            |clear_encoder_count.png|
        """
        self.set_encoder_count(0)

    def set_encoder_mode(self, mode):
        """Set the encoder AB or BA phase order.

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
        """Get the encoder phase order.

        Returns:
            int: ``ENCODER_MODE_AB`` or ``ENCODER_MODE_BA``.

        UiFlow2 Code Block:

            |get_encoder_mode.png|
        """
        return self._read(_REG_ENCODER_MODE, 1)[0]

    def set_position_pid(self, kp, ki, kd):
        """Set the position-loop PID coefficients.

        Args:
            kp (int): Native proportional coefficient. Range: 0~255.
            ki (int): Native integral coefficient. Range: 0~255.
            kd (int): Native derivative coefficient. Range: 0~255.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_position_pid.png|
        """
        self._set_pid(_POSITION_PID_OFFSET, kp, ki, kd)

    def get_position_pid(self):
        """Get the position-loop PID coefficients.

        Returns:
            tuple: ``(kp, ki, kd)``. Each native coefficient is 0~255.

        UiFlow2 Code Block:

            |get_position_pid.png|
        """
        return self._get_pid(_POSITION_PID_OFFSET)

    def set_position_target_count(self, count):
        """Set the position-loop target in encoder counts.

        Args:
            count (int): Signed target. Unit: encoder counts. Range:
                -2147483648~2147483647.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_position_target_count.png|
        """
        count = _validate_int("count", count, -2147483648, 2147483647)
        self._write(
            _REG_MOTOR_CONFIG + _POSITION_TARGET_OFFSET,
            struct.pack("<i", count),
        )

    def get_position_target_count(self):
        """Get the configured position-loop target in encoder counts.

        Returns:
            int: Signed target. Unit: encoder counts. Range:
            -2147483648~2147483647.

        UiFlow2 Code Block:

            |get_position_target_count.png|
        """
        return struct.unpack("<i", self._read(_REG_MOTOR_CONFIG + _POSITION_TARGET_OFFSET, 4))[0]

    def set_position_speed_limit(self, speed_limit):
        """Set the native position-loop maximum speed.

        The position controller uses the absolute value of this speed limit.
        The value is a device-native setting without a documented RPM conversion.

        Args:
            speed_limit (int): Signed device-native speed limit. Range:
                -127~127.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_position_speed_limit.png|
        """
        speed_limit = _validate_int("speed_limit", speed_limit, -127, 127)
        self._write(
            _REG_MOTOR_CONFIG + _POSITION_SPEED_LIMIT_OFFSET,
            struct.pack("<b", speed_limit),
        )

    def get_position_speed_limit(self):
        """Get the native position-loop maximum speed.

        Returns:
            int: Signed, dimensionless device value. Range: -127~127. This
            value is not RPM.

        UiFlow2 Code Block:

            |get_position_speed_limit.png|
        """
        return struct.unpack(
            "<b", self._read(_REG_MOTOR_CONFIG + _POSITION_SPEED_LIMIT_OFFSET, 1)
        )[0]

    def set_speed_pid(self, kp, ki, kd):
        """Set the speed-loop PID coefficients.

        Args:
            kp (int): Native proportional coefficient. Range: 0~255.
            ki (int): Native integral coefficient. Range: 0~255.
            kd (int): Native derivative coefficient. Range: 0~255.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_speed_pid.png|
        """
        self._set_pid(_SPEED_PID_OFFSET, kp, ki, kd)

    def get_speed_pid(self):
        """Get the speed-loop PID coefficients.

        Returns:
            tuple: ``(kp, ki, kd)``. Each native coefficient is 0~255.

        UiFlow2 Code Block:

            |get_speed_pid.png|
        """
        return self._get_pid(_SPEED_PID_OFFSET)

    def set_speed_target(self, speed):
        """Set the native closed-loop speed target.

        Args:
            speed (int): Signed, dimensionless target. Range: -127~127. The
                value is not RPM.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_speed_target.png|
        """
        speed = _validate_int("speed", speed, -127, 127)
        self._write(
            _REG_MOTOR_CONFIG + _SPEED_TARGET_OFFSET,
            struct.pack("<b", speed),
        )

    def get_speed_target(self):
        """Get the configured closed-loop speed target.

        Returns:
            int: Signed, dimensionless target. Range: -127~127. This value is
            not RPM.

        UiFlow2 Code Block:

            |get_speed_target.png|
        """
        return struct.unpack("<b", self._read(_REG_MOTOR_CONFIG + _SPEED_TARGET_OFFSET, 1))[0]

    def enable_soft_start(self):
        """Enable soft start and stop in open-loop mode.

        The setting is retained in the Unit's flash. Repeating the call while
        already enabled avoids another write.

        Returns:
            None.

        UiFlow2 Code Block:

            |enable_soft_start.png|
        """
        if not self.is_soft_start_enabled():
            self._write(_REG_SOFT_START, b"\x01")

    def disable_soft_start(self):
        """Disable soft start and stop in open-loop mode.

        The setting is retained in the Unit's flash. Repeating the call while
        already disabled avoids another write.

        Returns:
            None.

        UiFlow2 Code Block:

            |disable_soft_start.png|
        """
        if self.is_soft_start_enabled():
            self._write(_REG_SOFT_START, b"\x00")

    def is_soft_start_enabled(self):
        """Return whether soft start and stop is enabled.

        Returns:
            bool: ``True`` when soft start and stop is enabled.

        UiFlow2 Code Block:

            |is_soft_start_enabled.png|
        """
        return bool(self._read(_REG_SOFT_START, 1)[0])

    def enable_motor(self):
        """Set Motor nSleep to run and enable the motor driver.

        Returns:
            None.

        UiFlow2 Code Block:

            |enable_motor.png|
        """
        if not self.is_motor_enabled():
            self._write(_REG_MOTOR_SLEEP, b"\x01")

    def disable_motor(self):
        """Set Motor nSleep to sleep and disable the motor driver.

        Returns:
            None.

        UiFlow2 Code Block:

            |disable_motor.png|
        """
        if self.is_motor_enabled():
            self._write(_REG_MOTOR_SLEEP, b"\x00")

    def is_motor_enabled(self):
        """Return whether Motor nSleep is in the run state.

        Returns:
            bool: ``True`` when the motor driver is enabled.

        UiFlow2 Code Block:

            |is_motor_enabled.png|
        """
        return bool(self._read(_REG_MOTOR_SLEEP, 1)[0])

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
        """Read the motor-supply input voltage.

        Returns:
            float: Input voltage. Unit: V. Range depends on the supply.

        UiFlow2 Code Block:

            |read_input_voltage.png|
        """
        voltage_mv = struct.unpack("<H", self._read(_REG_INPUT_VOLTAGE_MV, 2))[0]
        return voltage_mv / 1000.0

    def read_input_voltage_adc(self):
        """Read the raw 12-bit motor-supply voltage ADC sample.

        Returns:
            int: Raw ADC sample. Range: 0~4095. Use
            ``read_input_voltage()`` for volts.

        UiFlow2 Code Block:

            |read_input_voltage_adc.png|
        """
        return struct.unpack("<H", self._read(_REG_INPUT_VOLTAGE_ADC, 2))[0] & 0x0FFF

    def read_input_current(self):
        """Read the motor-supply input current.

        Returns:
            float: Input current. Unit: A. Range depends on the load.

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
            int: 7-bit I2C address. Range: 0x08~0x77.

        UiFlow2 Code Block:

            |get_i2c_address.png|
        """
        return self._read(_REG_I2C_ADDRESS, 1)[0]

    def set_i2c_address(self, address):
        """Set the Unit I2C address and switch this object to it.

        A changed address is retained in the Unit's flash. The protocol states
        that the Unit restarts and requires about 300 ms before responding at
        the new address. This method waits and polls before updating the
        object's address. Avoid unnecessary calls to limit flash writes.

        Args:
            address (int): New 7-bit I2C address. Range: 0x08~0x77.

        Returns:
            None.

        UiFlow2 Code Block:

            |set_i2c_address.png|
        """
        address = _validate_int("address", address, 0x08, 0x77)
        if address == self.get_i2c_address():
            self._address = address
            return

        old_address = self._address
        self._write(_REG_I2C_ADDRESS, bytes((address,)))
        time.sleep_ms(300)
        try:
            self._wait_for_address(address)
        except OSError:
            raise OSError(
                "Unit EncoderMotor Driver did not respond at new address "
                "0x{:02X}; object remains at 0x{:02X}".format(address, old_address)
            )
        self._address = address
