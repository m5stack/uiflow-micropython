# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import time
import struct
import sys

if sys.platform != "esp32":
    from typing import Union

BLDC_I2C_ADDR = 0x65

MODE_REG = 0x00
DIRECTION_REG = 0x60
MOTOR_MODEL_REG = 0x70
POLE_PAIRS_REG = 0x71
MOTOR_STATUS_REG = 0x80
PWM_REG = 0x10
RB_RPM_FLOAT_REG = 0x20
RB_RPM_INT_REG = 0x90
RB_RPM_STR_REG = 0xB0
RB_FREQ_FLOAT_REG = 0x30
RB_FREQ_INT_REG = 0xA0
RB_FREQ_STR_REG = 0xC0
SET_RPM_FLOAT_REG = 0x40
SET_RPM_INT_REG = 0xD0
PID_REG = 0x50
FLASH_WR_BK_REG = 0xF0
FW_VER_REG = 0xFE
I2C_ADDR_REG = 0xFF


class BLDCDriverUnit:
    """Create an BLDCDriverUnit object.

    :param i2c: I2C port.
    :type i2c: machine.I2C | PAHUBUnit
    :param address: BLDCDriverUnit Slave Address.
    :type address: int | list | tuple

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import BLDCDriverUnit

            unit_bldcdriver_0 = BLDCDriverUnit(i2c0, 0x65)
    """

    def __init__(
        self,
        i2c: Union[machine.I2C, PAHUBUnit],
        address: int | list | tuple = BLDC_I2C_ADDR,
    ) -> None:
        """Initialize the bldc unit."""
        self.i2c = i2c
        if address >= 1 and address <= 127:
            self.unit_addr = address
        self._available()

    def _available(self):
        """! Check if sensor is available on the I2C bus."""
        if self.unit_addr not in self.i2c.scan():
            raise UnitError("BLDC Unit not found in Grove")

    @property
    def get_current_mode(self) -> int:
        """Get the current mode setting.

        :returns: current mode.
        :rtype: int

        UiFlow2 Code Block:

            |get_current_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.get_current_mode()
        """
        return self.i2c.readfrom_mem(self.unit_addr, MODE_REG, 1)[0]

    def set_mode(self, mode: int) -> None:
        """Set the mode setting.

        :param: int mode: 0 mean open loop, 1 mean close loop.

        UiFlow2 Code Block:

            |set_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.set_mode(mode)
        """
        self.i2c.writeto_mem(self.unit_addr, MODE_REG, bytes([mode]))

    @property
    def get_motor_current_direction(self) -> int:
        """Get the current direction setting.

        :returns: current direction.
        :rtype: int

        UiFlow2 Code Block:

            |get_motor_current_direction.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.get_motor_current_direction()
        """
        return self.i2c.readfrom_mem(self.unit_addr, DIRECTION_REG, 1)[0]

    def set_direction(self, direction) -> None:
        """Set the direction.

        :param int model: 0 forward, 1 backward.

        UiFlow2 Code Block:

            |set_direction.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.set_direction()
        """
        self.i2c.writeto_mem(self.unit_addr, DIRECTION_REG, bytes([direction]))

    @property
    def get_motor_current_model(self) -> int:
        """Get the motor current model setting.

        :returns: motor current model.
        :rtype: int

        UiFlow2 Code Block:

            |get_motor_current_model.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.get_motor_current_model()
        """
        return self.i2c.readfrom_mem(self.unit_addr, MOTOR_MODEL_REG, 1)[0]

    def set_motor_model(self, model: int) -> int:
        """Set the motor model setting.

        :param int model: 0 mean low speed, 1 mean high speed.

        UiFlow2 Code Block:

            |set_motor_model.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.set_motor_model(model)
        """
        self.i2c.writeto_mem(self.unit_addr, MOTOR_MODEL_REG, bytes([model]))

    @property
    def get_motor_pole_pairs(self) -> int:
        """Get the pole pairs setting.

        :returns: motor pole pairs.
        :rtype: int

        UiFlow2 Code Block:

            |get_motor_pole_pairs.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.get_motor_pole_pairs()
        """
        return self.i2c.readfrom_mem(self.unit_addr, POLE_PAIRS_REG, 1)[0]

    def set_pole_pairs(self, pole: int) -> None:
        """Set pole pairs.

        :param int pole: pole pairs, range: 0~255.

        UiFlow2 Code Block:

            |set_pole_pairs.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.set_pole_pairs(pole)
        """
        self.i2c.writeto_mem(self.unit_addr, POLE_PAIRS_REG, bytes([pole]))

    @property
    def get_motor_status(self) -> int:
        """Get motor status.

        :returns: motor status.
        :rtype: int

        UiFlow2 Code Block:

            |get_motor_status.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.get_motor_status()
        """
        return self.i2c.readfrom_mem(self.unit_addr, MOTOR_STATUS_REG, 1)[0]

    @property
    def get_open_loop_pwm(self) -> int:
        """Get the open loop pwm.

        :returns: open loop pwm.
        :rtype: int

        UiFlow2 Code Block:

            |get_open_loop_pwm.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.get_open_loop_pwm()
        """
        buf = self.i2c.readfrom_mem(self.unit_addr, PWM_REG, 2)
        return struct.unpack("<h", buf)[0]

    def set_open_loop_pwm(self, pwm: int) -> int:
        """Set the open loop pwm.

        :param int pwm:  open loop pwm., range: 0~2047.

        UiFlow2 Code Block:

            |set_open_loop_pwm.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.set_open_loop_pwm(pwm)
        """
        self.i2c.writeto_mem(self.unit_addr, PWM_REG, struct.pack("<h", pwm))

    @property
    def get_read_back_rpm_float(self) -> float:
        """Get the read back rpm in float.

        :returns: read back rpm.
        :rtype: float

        UiFlow2 Code Block:

            |get_read_back_rpm_float.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.get_read_back_rpm_float()
        """
        buf = self.i2c.readfrom_mem(self.unit_addr, RB_RPM_FLOAT_REG, 4)
        return struct.unpack("<f", buf)[0]

    @property
    def get_read_back_rpm_int(self) -> int:
        """Get the read back rpm in int.

        :returns: read back rpm.
        :rtype: int

        UiFlow2 Code Block:

            |get_read_back_rpm_int.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.get_read_back_rpm_int()
        """
        data = self.i2c.readfrom_mem(self.unit_addr, RB_RPM_INT_REG, 4)
        return struct.unpack("<i", data)[0]

    @property
    def get_read_back_rpm_str(self) -> str:
        """Get the read back rpm in str.

        :returns: read back rpm.
        :rtype: str

        UiFlow2 Code Block:

            |get_read_back_rpm_str.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.get_read_back_rpm_str()
        """
        data = self.i2c.readfrom_mem(self.unit_addr, RB_RPM_STR_REG, 16)
        return data.replace(b"\x00", b"").decode("utf8")

    @property
    def get_read_back_freq_float(self) -> float:
        """Get the read back frequency in float.

        :returns: read back frequency.
        :rtype: float

        UiFlow2 Code Block:

            |get_read_back_freq_float.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.get_read_back_freq_float()
        """
        buf = self.i2c.readfrom_mem(self.unit_addr, RB_FREQ_FLOAT_REG, 4)
        return struct.unpack("<f", buf)[0]

    @property
    def get_read_back_freq_int(self) -> int:
        """Get the read back frequency in int.

        :returns: read back frequency.
        :rtype: int

        UiFlow2 Code Block:

            |get_read_back_freq_int.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.get_read_back_freq_int()
        """
        data = self.i2c.readfrom_mem(self.unit_addr, RB_FREQ_INT_REG, 4)
        return struct.unpack("<i", data)[0]

    @property
    def get_read_back_freq_str(self) -> str:
        """Get the read back frequency in str.

        :returns: read back frequency.
        :rtype: str

        UiFlow2 Code Block:

            |get_read_back_freq_str.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.get_read_back_freq_str()
        """
        data = self.i2c.readfrom_mem(self.unit_addr, RB_FREQ_STR_REG, 16)
        return data.replace(b"\x00", b"").decode("utf8")

    @property
    def get_rpm_float(self) -> float:
        """Get the rpm in float.

        :returns: rpm.
        :rtype: float

        UiFlow2 Code Block:

            |get_rpm_float.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.get_rpm_float()
        """
        buf = self.i2c.readfrom_mem(self.unit_addr, SET_RPM_FLOAT_REG, 4)
        return struct.unpack("<f", buf)[0]

    def set_rpm_float(self, rpm: float) -> None:
        """Set the rpm in float.

        :param float rpm: Revolutions per minute.

        UiFlow2 Code Block:

            |set_rpm_float.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.set_rpm_float(rpm)
        """
        self.i2c.writeto_mem(self.unit_addr, SET_RPM_FLOAT_REG, struct.pack("<f", rpm))

    @property
    def get_rpm_int(self) -> int:
        """Get the rpm in int.

        :returns: Revolutions per minute.
        :rtype: int

        UiFlow2 Code Block:

            |get_rpm_int.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.get_rpm_int()
        """
        data = self.i2c.readfrom_mem(self.unit_addr, SET_RPM_INT_REG, 4)
        return struct.unpack("<i", data)[0]

    def set_rpm_int(self, pwm) -> None:
        """Set the rpm in int.

        :param int rpm: Revolutions per minute.

        UiFlow2 Code Block:

            |set_rpm_int.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.set_rpm_int(rpm)
        """
        self.i2c.writeto_mem(self.unit_addr, SET_RPM_INT_REG, struct.pack("<i", pwm))

    @property
    def get_pid_value(self) -> tuple:
        """Get the PID value.

        This method retrieves the PID values from the specified register and returns them as a tuple.

        :returns: A tuple containing the PID values (proportional, integral, derivative).
        :rtype: tuple[int, int, int]

        UiFlow2 Code Block:

            |get_pid_value.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.get_pid_value()
        """
        data = self.i2c.readfrom_mem(self.unit_addr, PID_REG, 12)
        return struct.unpack("<iii", data)

    def set_pid_value(self, p: int, i: int, d: int) -> None:
        """! Set the PID values (Proportional, Integral, Derivative).

        This method sets the PID values to the specified register, which will control the motor's PID behavior.

        :param int p: The proportional value.
        :param int i: The integral value.
        :param int d: The derivative value.

        UiFlow2 Code Block:

            |set_pid_value.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.set_pid_value(p, i, d)
        """
        self.i2c.writeto_mem(self.unit_addr, PID_REG, struct.pack("<iii", p, i, d))

    def save_data_in_flash(self) -> None:
        """Save motor data to flash.

        UiFlow2 Code Block:

            |save_data_in_flash.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_bldcdriver_0.save_data_in_flash()
        """
        time.sleep_ms(10)
        self.i2c.writeto_mem(self.unit_addr, FLASH_WR_BK_REG, b"\x01")
        time.sleep_ms(200)

    def get_device_spec(self, mode: int) -> None:
        """Get device firmware version and I2C address.

        This method retrieves either the firmware version or the I2C address of the device based on the provided mode.

        :param int mode: The mode to determine what information to fetch.
            - `0xFE`: Retrieve firmware version.
            - `0xFF`: Retrieve I2C address.

        UiFlow2 Code Block:

            |get_device_spec.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_device.get_device_spec(mode)
        """
        if mode >= FW_VER_REG and mode <= I2C_ADDR_REG:
            return self.i2c.readfrom_mem(self.unit_addr, mode, 1)[0]

    def set_i2c_address(self, addr: int) -> None:
        """Set the I2C address.

        :param int addr: The new I2C address, range: 1~127.

        UiFlow2 Code Block:

            |set_i2c_address.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_device.set_i2c_address(addr)
        """
        if addr >= 1 and addr <= 127:
            if addr != self.unit_addr:
                time.sleep_ms(10)
                self.i2c.writeto_mem(self.unit_addr, I2C_ADDR_REG, struct.pack("b", addr))
                self.unit_addr = addr
                time.sleep_ms(200)
