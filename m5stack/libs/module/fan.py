# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from module.mbus import i2c1
import struct
import time


class FanModule:
    _FAN_ADDR = 0x18

    _FAN_STATE_CTR_REG = 0x00
    _FAN_PWM_FREQ_REG = 0x10
    _FAN_PWM_DUTY_CYCLE_REG = 0x20
    _FAN_RPM_REG = 0x30
    _FAN_SIGNAL_FREQ_REG = 0x40
    _FAN_FLASH_REG = 0xF0
    _FAN_FW_VERSION_REG = 0xFE
    _FAN_I2C_ADDR_REG = 0xFF

    """Create an FanModule object.

    :param int address: The I2C address of the device. Default is 0x53.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import FanModule

            fan_v11_0 = FanModule(address=0x18)
    """

    def __init__(self, address: int | list | tuple = _FAN_ADDR) -> None:
        self._i2c = i2c1
        self._i2c_addr = address
        if self._i2c_addr not in self._i2c.scan():
            raise Exception("FanModule not found in Base")

    def set_fan_state(self, state: bool):
        """Set the fan state to on or off.

        :param bool state: The state of the fan.

        UiFlow2 Code Block:

            |set_fan_state.png|

        MicroPython Code Block:

            .. code-block:: python

                fan_v11_0.set_fan_state(True)
        """
        self._i2c.writeto_mem(self._i2c_addr, self._FAN_STATE_CTR_REG, bytes([state]))

    def get_fan_state(self) -> bool:
        """Get current fan state.

        :returns: The current fan state.
        :rtype: bool

        UiFlow2 Code Block:

            |get_fan_state.png|

        MicroPython Code Block:

            .. code-block:: python

                fan_v11_0.get_fan_state()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self._FAN_STATE_CTR_REG, 1)[0] == 1

    def set_pwm_frequency(self, freq: int = 2) -> None:
        """Set the PWM frequency of the fan.

        :param int freq: The PWM frequency of the fan.

        UiFlow2 Code Block:

            |set_pwm_frequency.png|

        MicroPython Code Block:

            .. code-block:: python

                fan_v11_0.set_pwm_frequency(2)
        """
        self._i2c.writeto_mem(self._i2c_addr, self._FAN_PWM_FREQ_REG, bytes([freq]))

    def get_pwm_frequency(self) -> int:
        """Get current PWM frequency.

        :returns: The current PWM frequency.
        :rtype: int

        UiFlow2 Code Block:

            |get_pwm_frequency.png|

        MicroPython Code Block:

            .. code-block:: python

                fan_v11_0.get_pwm_frequency()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self._FAN_PWM_FREQ_REG, 1)[0]

    def set_pwm_duty_cycle(self, duty_cycle: int) -> None:
        """Set the PWM duty cycle of the fan.

        :param int duty_cycle: The PWM duty cycle of the fan.

        UiFlow2 Code Block:

            |set_pwm_duty_cycle.png|

        MicroPython Code Block:

            .. code-block:: python

                fan_v11_0.set_pwm_duty_cycle(50)
        """
        if not (0 <= duty_cycle <= 100):
            raise ValueError("Duty cycle error, range is 0~100")
        self._i2c.writeto_mem(self._i2c_addr, self._FAN_PWM_DUTY_CYCLE_REG, bytes([duty_cycle]))

    def get_pwm_duty_cycle(self) -> int:
        """Get current PWM duty cycle.

        :returns: The current PWM duty cycle.
        :rtype: int

        UiFlow2 Code Block:

            |get_pwm_duty_cycle.png|

        MicroPython Code Block:

            .. code-block:: python

                fan_v11_0.get_pwm_duty_cycle()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self._FAN_PWM_DUTY_CYCLE_REG, 1)[0]

    def get_fan_rpm(self) -> int:
        """Get current fan RPM.

        :returns: The current fan RPM.
        :rtype: int

        UiFlow2 Code Block:

            |get_fan_rpm.png|

        MicroPython Code Block:

            .. code-block:: python

                fan_v11_0.get_fan_rpm()
        """
        return struct.unpack("<H", self._i2c.readfrom_mem(self._i2c_addr, self._FAN_RPM_REG, 2))[0]

    def get_single_frequency(self) -> int:
        """Get current single frequency.

        :returns: The current single frequency.
        :rtype: int

        UiFlow2 Code Block:

            |get_single_frequency.png|

        MicroPython Code Block:

            .. code-block:: python

                fan_v11_0.get_single_frequency()
        """
        return struct.unpack(
            "<H", self._i2c.readfrom_mem(self._i2c_addr, self._FAN_SIGNAL_FREQ_REG, 2)
        )[0]

    def write_flash(self) -> None:
        """Save the current configuration(fan status, PWM frequency, and PWM duty cycle) to the flash.

        UiFlow2 Code Block:

            |write_flash.png|

        MicroPython Code Block:

            .. code-block:: python

                fan_v11_0.write_flash()
        """
        self._i2c.writeto_mem(self._i2c_addr, self._FAN_FLASH_REG, bytes([True]))

    def get_firmware_version(self) -> int:
        """Get current firmware version.

        :returns: The current firmware version.
        :rtype: int

        UiFlow2 Code Block:

            |get_firmware_version.png|

        MicroPython Code Block:

            .. code-block:: python

                fan_v11_0.get_firmware_version()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self._FAN_FW_VERSION_REG, 1)[0]

    def get_i2c_address(self) -> int:
        """Get current I2C address.

        :returns: The current I2C address.
        :rtype: int

        UiFlow2 Code Block:

            |get_i2c_address.png|

        MicroPython Code Block:

            .. code-block:: python

                fan_v11_0.get_i2c_address()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self._FAN_I2C_ADDR_REG, 1)[0]

    def set_i2c_address(self, addr: int) -> None:
        """Set the I2C address of the fan.

        :param int addr: The I2C address of the fan.

        UiFlow2 Code Block:

            |set_i2c_address.png|

        MicroPython Code Block:

            .. code-block:: python

                fan_v11_0.set_i2c_address(0x18)
        """
        if addr >= 0x08 and addr <= 0x77:
            if addr != self._i2c_addr:
                time.sleep_ms(2)
                self._i2c.writeto_mem(self._i2c_addr, self._FAN_I2C_ADDR_REG, bytearray([addr]))
                self._i2c_addr = addr
                time.sleep_ms(200)
        else:
            raise ValueError("I2C address error, range:0x08~0x78")
