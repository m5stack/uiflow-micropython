# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from unit.unit_helper import UnitError
import machine
import time

MQ_ADDR = 0x11


class MQUnit:
    """Create a MQUnit object.

    :param I2C i2c: The I2C bus the MQ Unit is connected to.
    :param int address: The I2C address of the device. Default is 0x11.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hardware import I2C
            from unit import MQUnit

            i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
            tof_0 = MQUnit(i2c0)
    """

    MQ_CFG_REG = 0x0
    MQ_LED_CFG_REG = 0x01
    MQ_HEAT_CFG_REG = 0x10
    MQ_ADC_8BIT_REG = 0x20
    MQ_ADC_12BIT_REG = 0x30
    MQ_VALID_REG = 0x40
    MQ_INTERNAL_NTC_8BIT_ADC_REG = 0x50
    MQ_INTERNAL_NTC_12BIT_ADC_REG = 0x60
    MQ_NTC_RES_REG = 0x70
    MQ_VOLTAGE_REG = 0x80
    MQ_FW_VER_REG = 0xFE
    MQ_I2C_ADDR_REG = 0xFF

    def __init__(self, i2c: machine.I2C, address: int = MQ_ADDR):
        self._i2c = i2c
        self._i2c_addr = address
        self._available()
        self.set_led_status(1)

    def _available(self):
        if self._i2c_addr not in self._i2c.scan():
            raise UnitError("MQ unit maybe not connect")

    def set_mq_mode(self, mode: int = 1):
        """Set the working mode of the MQ sensor.

        :param int mode: Working mode value.

        Option:
            - 0 : Measurement off
            - 1 : Continuous heating mode
            - 2 : Pin Level Switching Mode

        UiFlow2 Code Block:

            |set_mq_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                mq_0.set_mq_mode(1)
        """
        self._i2c.writeto_mem(self._i2c_addr, self.MQ_CFG_REG, bytes([mode]))

    def get_mq_mode(self):
        """Get the current working mode of the MQ sensor.

        :returns: Current working mode value.
        :rtype: int

        UiFlow2 Code Block:

            |get_mq_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                mode = mq_0.get_mq_mode()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self.MQ_CFG_REG, 1)[0]

    def set_led_status(self, status: int):
        """Set the LED status.

        :param int status: When the LED is set to on, it lights up when a valid tag is detected, and the brightness is proportional to the ADC value, and it turns off when no tag is detected.

        MicroPython Code Block:

            .. code-block:: python

                mq_0.set_led_status(1)
        """
        self._i2c.writeto_mem(self._i2c_addr, self.MQ_LED_CFG_REG, bytes([status]))

    def get_led_status(self):
        """Get the LED status.

        :returns: True if LED status is on, False otherwise.
        :rtype: bool

        MicroPython Code Block:

            .. code-block:: python

                led_on = mq_0.get_led_status()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self.MQ_LED_CFG_REG, 1)[0] == 1

    def set_heat_time(self, high_level_time: int = 30, low_level_time: int = 5):
        """Set heater high and low level time.

        :param int high_level_time: Time for high heating level.
        :param int low_level_time: Time for low heating level.

        UiFlow2 Code Block:

            |set_heat_time.png|

        MicroPython Code Block:

            .. code-block:: python

                mq_0.set_heat_time(30, 5)
        """
        self._i2c.writeto_mem(
            self._i2c_addr, self.MQ_HEAT_CFG_REG, bytes([high_level_time, low_level_time])
        )

    def get_heat_time(self):
        """Get heater high and low level time.

        :returns: [high_level_time, low_level_time]
        :rtype: [int, int]

        MicroPython Code Block:

            .. code-block:: python

                times = mq_0.get_heat_time()
        """
        return list(self._i2c.readfrom_mem(self._i2c_addr, self.MQ_HEAT_CFG_REG, 2))

    def get_adc_value(self, precision):
        """Get ADC value.

        :param int precision: 0 for 8-bit, 1 for 12-bit.
        :returns: ADC value.
        :rtype: int

        UiFlow2 Code Block:

            |get_adc_value.png|

        MicroPython Code Block:

            .. code-block:: python

                value = mq_0.get_adc_value(1)
        """
        if precision == 0:
            return self._i2c.readfrom_mem(self._i2c_addr, self.MQ_ADC_8BIT_REG, 1)[0]
        elif precision == 1:
            buf = self._i2c.readfrom_mem(self._i2c_addr, self.MQ_ADC_12BIT_REG, 2)
            return buf[1] << 8 | buf[0]

    def get_valid_tags(self):
        """Check if valid tags are detected.

        :returns: True if valid tags detected, False otherwise.
        :rtype: bool

        UiFlow2 Code Block:

            |get_valid_tags.png|

        MicroPython Code Block:

            .. code-block:: python

                valid = mq_0.get_valid_tags()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self.MQ_VALID_REG, 1)[0] == 1

    def get_ntc_adc_value(self, precision):
        """Get internal NTC ADC value.

        :param int precision: 0 for 8-bit, 1 for 12-bit.
        :returns: NTC ADC value.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                ntc = mq_0.get_ntc_adc_value(1)
        """
        if precision == 0:
            return self._i2c.readfrom_mem(self._i2c_addr, self.MQ_INTERNAL_NTC_8BIT_ADC_REG, 1)[0]
        elif precision == 1:
            buf = self._i2c.readfrom_mem(self._i2c_addr, self.MQ_INTERNAL_NTC_12BIT_ADC_REG, 2)
            return buf[1] << 8 | buf[0]

    def get_ntc_res_value(self):
        """Get internal NTC resistance value.

        :returns: Resistance value.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                res = mq_0.get_ntc_res_value()
        """
        buf = self._i2c.readfrom_mem(self._i2c_addr, self.MQ_NTC_RES_REG, 2)
        return buf[1] << 8 | buf[0]

    def get_voltage(self, channle: int):
        """Get voltage value from a specific channel.

        :param int channle: Channel number.
        :returns: Voltage value.
        :rtype: int

        MicroPython Code Block:

            .. code-block:: python

                voltage = mq_0.get_voltage(0)
        """
        buf = self._i2c.readfrom_mem(self._i2c_addr, self.MQ_VOLTAGE_REG + channle * 2, 2)
        return buf[1] << 8 | buf[0]

    def get_firmware_version(self) -> int:
        """Get firmware version.

        :returns: Firmware version.
        :rtype: int

        UiFlow2 Code Block:

            |get_firmware_version.png|

        MicroPython Code Block:

            .. code-block:: python

                ver = mq_0.get_firmware_version()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self.MQ_FW_VER_REG, 1)[0]

    def get_i2c_address(self) -> int:
        """Get current I2C address.

        :returns: MQ Unit I2C address, Default is 0x11.
        :rtype: int

        UiFlow2 Code Block:

            |get_i2c_address.png|

        MicroPython Code Block:

            .. code-block:: python

                addr = mq_0.get_i2c_address()
        """
        return self._i2c.readfrom_mem(self._i2c_addr, self.MQ_I2C_ADDR_REG, 1)[0]

    def set_i2c_address(self, addr: int):
        """Set new I2C address.

        :param int addr: New I2C address (0x08~0x77).

        UiFlow2 Code Block:

            |set_i2c_address.png|

        MicroPython Code Block:

            .. code-block:: python

                mq_0.set_i2c_address(0x3A)
        """
        if addr >= 0x08 and addr <= 0x77:
            if addr != self._i2c_addr:
                time.sleep_ms(2)
                self._i2c.writeto_mem(self._i2c_addr, self.MQ_I2C_ADDR_REG, bytearray([addr]))
                self._i2c_addr = addr
                time.sleep_ms(200)
        else:
            raise ValueError("I2C address error, range:0x08~0x77")
