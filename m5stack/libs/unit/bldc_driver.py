# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from machine import I2C
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import time
import struct

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


class BLDCDRIVERUnit:
    def __init__(
        self,
        i2c: I2C | PAHUBUnit,
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
        """! Get the current mode setting."""
        return self.i2c.readfrom_mem(self.unit_addr, MODE_REG, 1)[0]

    def set_mode(self, mode) -> None:
        """! Set the mode setting.
        mode: 0~1(open loop or close loop)
        """
        self.i2c.writeto_mem(self.unit_addr, MODE_REG, bytes([mode]))

    @property
    def get_motor_current_direction(self) -> int:
        """! Get the current direction setting."""
        return self.i2c.readfrom_mem(self.unit_addr, DIRECTION_REG, 1)[0]

    def set_direction(self, direction) -> None:
        """! Set the direction setting.
        direction: 0~1(forward~backward)
        """
        self.i2c.writeto_mem(self.unit_addr, DIRECTION_REG, bytes([direction]))

    @property
    def get_motor_current_model(self) -> int:
        """! Get the motor model setting."""
        return self.i2c.readfrom_mem(self.unit_addr, MOTOR_MODEL_REG, 1)[0]

    def set_motor_model(self, model) -> int:
        """! set the motor model setting.
        model: 0~1(low speed~high speed)
        """
        self.i2c.writeto_mem(self.unit_addr, MOTOR_MODEL_REG, bytes([model]))

    @property
    def get_motor_pole_pairs(self) -> int:
        """! Get the pole pairs setting."""
        return self.i2c.readfrom_mem(self.unit_addr, POLE_PAIRS_REG, 1)[0]

    def set_pole_pairs(self, pole) -> None:
        """! set the pole pairs setting.
        pole: 0~255
        """
        self.i2c.writeto_mem(self.unit_addr, POLE_PAIRS_REG, bytes([pole]))

    @property
    def get_motor_status(self) -> int:
        """! Set the motor status."""
        return self.i2c.readfrom_mem(self.unit_addr, MOTOR_STATUS_REG, 1)[0]

    @property
    def get_open_loop_pwm(self) -> int:
        """! Get the open loop pwm."""
        buf = self.i2c.readfrom_mem(self.unit_addr, PWM_REG, 2)
        return struct.unpack("<h", buf)[0]

    def set_open_loop_pwm(self, pwm) -> int:
        """! set the open loop pwm.
        pwm: 0~2047
        """
        self.i2c.writeto_mem(self.unit_addr, PWM_REG, struct.pack("<h", pwm))

    @property
    def get_read_back_rpm_float(self) -> float:
        """! Get the read back rpm in float."""
        buf = self.i2c.readfrom_mem(self.unit_addr, RB_RPM_FLOAT_REG, 4)
        return struct.unpack("<f", buf)[0]

    @property
    def get_read_back_rpm_int(self) -> int:
        """! Get the read back rpm in int."""
        data = self.i2c.readfrom_mem(self.unit_addr, RB_RPM_INT_REG, 4)
        return struct.unpack("<i", data)[0]

    @property
    def get_read_back_rpm_str(self) -> str:
        """! Get the read back rpm in str."""
        data = self.i2c.readfrom_mem(self.unit_addr, RB_RPM_STR_REG, 16)
        return data.replace(b"\x00", b"").decode("utf8")

    @property
    def get_read_back_freq_float(self) -> float:
        """! Get the read back frequency in float."""
        buf = self.i2c.readfrom_mem(self.unit_addr, RB_FREQ_FLOAT_REG, 4)
        return struct.unpack("<f", buf)[0]

    @property
    def get_read_back_freq_int(self) -> int:
        """! Get the read back frequency in int."""
        data = self.i2c.readfrom_mem(self.unit_addr, RB_FREQ_INT_REG, 4)
        return struct.unpack("<i", data)[0]

    @property
    def get_read_back_freq_str(self) -> str:
        """! Get the read back frequency in str."""
        data = self.i2c.readfrom_mem(self.unit_addr, RB_FREQ_STR_REG, 16)
        return data.replace(b"\x00", b"").decode("utf8")

    @property
    def get_rpm_float(self) -> float:
        """! Get the rpm in float."""
        buf = self.i2c.readfrom_mem(self.unit_addr, SET_RPM_FLOAT_REG, 4)
        return struct.unpack("<f", buf)[0]

    def set_rpm_float(self, rpm) -> None:
        """! Set the rpm in float."""
        self.i2c.writeto_mem(self.unit_addr, SET_RPM_FLOAT_REG, struct.pack("<f", rpm))

    @property
    def get_rpm_int(self) -> int:
        """! Get the rpm in int."""
        data = self.i2c.readfrom_mem(self.unit_addr, SET_RPM_INT_REG, 4)
        return struct.unpack("<i", data)[0]

    def set_rpm_int(self, pwm) -> None:
        """! Set the rpm in int."""
        self.i2c.writeto_mem(self.unit_addr, SET_RPM_INT_REG, struct.pack("<i", pwm))

    @property
    def get_pid_value(self) -> tuple:
        """! Get the pid value."""
        data = self.i2c.readfrom_mem(self.unit_addr, PID_REG, 12)
        return struct.unpack("<iii", data)

    def set_pid_value(self, p: int, i: int, d: int) -> None:
        """! set the pid value."""
        self.i2c.writeto_mem(self.unit_addr, PID_REG, struct.pack("<iii", p, i, d))

    def save_data_in_flash(self):
        """! Save motor data to flash."""
        time.sleep_ms(10)
        self.i2c.writeto_mem(self.unit_addr, FLASH_WR_BK_REG, b"\x01")
        time.sleep_ms(200)

    def get_device_spec(self, mode):
        """! Get device firmware version and i2c address.
        mode: 0xFE and 0xFF
        """
        if mode >= FW_VER_REG and mode <= I2C_ADDR_REG:
            return self.i2c.readfrom_mem(self.unit_addr, mode, 1)[0]

    def set_i2c_address(self, addr):
        """! Set i2c address.
        addr:  1 to 127
        """
        if addr >= 1 and addr <= 127:
            if addr != self.unit_addr:
                time.sleep_ms(10)
                self.i2c.writeto_mem(self.unit_addr, I2C_ADDR_REG, struct.pack("b", addr))
                self.unit_addr = addr
                time.sleep_ms(200)
