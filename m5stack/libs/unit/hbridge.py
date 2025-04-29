# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import machine
import struct
from .pahub import PAHUBUnit
from .unit_helper import UnitError
import sys

if sys.platform != "esp32":
    from typing import Union

HBRIDGE_ADDR = 0x20

DIRECTION_REG = 0x00
PWM8BIT_REG = 0x01
PWM16BIT_REG = 0x02
PWMFREQ_REG = 0x04
ADC8BIT_REG = 0x10
ADC16BIT_REG = 0x20
VIN_CURRENT_REG = 0x30
I2C_ADDR_REG = 0xFF
FW_VER_REG = 0xFE


class HbridgeUnit:
    """Create an HbridgeUnit object.

    :param i2c: I2C port.
    :type i2c: machine.I2C | PAHUBUnit
    :param address: HbridgeUnit Slave Address.
    :type address: int | list | tuple

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import HbridgeUnit

            unit_hbridge_0 = HbridgeUnit(i2c0, 0x20)
    """

    def __init__(
        self,
        i2c: Union[machine.I2C, PAHUBUnit],
        address: int | list | tuple = HBRIDGE_ADDR,
    ):
        self.hbridge_i2c = i2c
        self.init_i2c_address(address)

    def init_i2c_address(self, slave_addr: int = HBRIDGE_ADDR) -> None:
        if slave_addr >= 0x20 and slave_addr <= 0x2F:
            self.i2c_addr = slave_addr
        if self.i2c_addr not in self.hbridge_i2c.scan():
            raise UnitError("Hbridge unit maybe not connect")

    def get_driver_config(self, reg: int = 0) -> int:
        """Get driver config.

        :param int reg:

        :returns: driver config.
        :rtype: int

        UiFlow2 Code Block:

            |get_driver_config.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_hbridge_0.get_driver_config(reg)
        """
        leng = 1
        if reg > 1:
            leng = 2
            buf = self.read_reg(reg, leng)
            return struct.unpack("<H", buf)[0]
        else:
            return self.read_reg(reg, leng)[0]

    def set_direction(self, dir: int = 0) -> None:
        """Set direction

        This method controls the motor's movement direction or stops it.

        :param int dir: Direction control parameter:
            - 0: Stop
            - 1: Forward
            - 2: Reverse

        UiFlow2 Code Block:

            |set_direction.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_hbridge_0.set_direction(dir)
        """
        self.write_mem_list(DIRECTION_REG, [dir])

    def set_8bit_pwm(self, duty: int = 0) -> None:
        """Set 8-bit pwm duty cycle

        :param int duty: PWM duty, range: 0~255

        UiFlow2 Code Block:

            |set_8bit_pwm.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_hbridge_0.set_8bit_pwm(duty)
        """
        self.write_mem_list(PWM8BIT_REG, [duty])

    def set_16bit_pwm(self, duty: int = 0) -> None:
        """Set 16-bit pwm duty cycle

        :param int duty: pwm duty, range: 0~65535

        UiFlow2 Code Block:

            |set_16bit_pwm.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_hbridge_0.set_16bit_pwm(duty)
        """
        self.write_mem_list(PWM16BIT_REG, [(duty & 0xFF), ((duty >> 8) & 0xFF)])

    def set_percentage_pwm(self, duty: int = 0, res: int = 8) -> None:
        """Set the PWM output based on percentage.

        :param int duty: PWM duty cycle as a percentage (0 to 100).
        :param int res: PWM resolution (8 or 16 bits), default is 8.

        UiFlow2 Code Block:

            |set_percentage_pwm.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_hbridge_0.set_percentage_pwm(duty, reg)
        """
        duty = max(min(duty, 100), 0)
        if res == 8:
            duty = self.map(duty, 0, 100, 0, 255)
        else:
            duty = self.map(duty, 0, 100, 0, 65535)
        self.write_mem_list(PWM8BIT_REG, [duty])

    def set_pwm_freq(self, freq: int = 0) -> None:
        """Set PWM frequency.

        :param int freq: The PWM frequnecy.

        UiFlow2 Code Block:

            |set_pwm_freq.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_hbridge_0.set_pwm_freq(freq)
        """
        freq = max(min(freq, 10000), 100)
        self.write_mem_list(PWMFREQ_REG, [(freq & 0xFF), ((freq >> 8) & 0xFF)])

    def get_adc_value(self, raw: int = 0, res: int = 8) -> None:
        """Get ADC value.

        This method retrieves the ADC value based on the specified resolution.
        It supports both 8-bit and 16-bit ADC resolutions. If `raw` is set to `1`,
        the raw ADC value is returned. Otherwise, the corresponding voltage is
        calculated and returned.

        :param int raw: If 1, returns the raw ADC value. If 0, returns the voltage
                        (calculated based on ADC value).
        :param int res: ADC resolution (8 or 16 bits). Default is 8 bits.

        :returns: The raw ADC value or the calculated voltage, depending on `raw`.
        :rtype: float or int

        UiFlow2 Code Block:

            |get_adc_value.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_hbridge_0.get_adc_value(raw, res)
        """
        leng = 1
        if res > 8:
            leng = 2
            buf = self.read_reg(ADC16BIT_REG, leng)
            val = struct.unpack("<H", buf)[0]
            res = 4095
        else:
            val = self.read_reg(ADC8BIT_REG, leng)[0]
            res = 255
        if raw:
            return val
        else:
            val = (3.3 / res) * val * 11
            return round(val, 2)

    #############################support v1.1################################
    def get_vin_current(self) -> float:
        """Get the input voltage current (unit: A).

        :returns: The input voltage current value.
        :rtype: float

        UiFlow2 Code Block:

            |get_vin_current.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_hbridge_0.get_vin_current()
        """
        buf = self.read_reg(VIN_CURRENT_REG, 4)
        return struct.unpack("<f", buf)[0]

    #############################support v1.1################################
    def get_device_status(self, mode: int) -> int:
        """Get device status.

        get firmware version and i2c address.

        :param int mode: 0xFE and 0xFF

        UiFlow2 Code Block:

            |get_device_status.png|

        MicroPython Code Block:

            .. code-block:: python

                unit_hbridge_0.get_device_status(mode)
        """
        if mode >= FW_VER_REG and mode <= I2C_ADDR_REG:
            return self.read_reg(mode, 1)[0]

    def write_mem_list(self, reg, data):
        buf = bytearray(data)
        self.hbridge_i2c.writeto_mem(self.i2c_addr, reg, buf)

    def read_reg(self, reg, num):
        return self.hbridge_i2c.readfrom_mem(self.i2c_addr, reg, num)

    def map(self, x, in_min, in_max, out_min, out_max):
        return round((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def deinit(self):
        pass
