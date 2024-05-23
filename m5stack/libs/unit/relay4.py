# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
"""
@File    :   relay4.py
@Time    :   2024/5/7
@Author  :   TONG YIHAN
@E-mail  :   icyqwq@gmail.com
@License :   (C)Copyright 2015-2024, M5STACK
"""

# Import necessary libraries
from machine import I2C
import struct
import time


class Relay4Unit:
    """! 4-Relay unit is an integrated 4-way relay module which can be controlled by I2C protocol.

    @en 4-Relay unit is an integrated 4-way relay module which can be controlled by I2C protocol. The maximum control voltage of each relay is AC-250V/DC-28V, the rated current is 10A and the instantaneous current can hold up to 16A. Each relay can be controlled independently, each on it's own. Each relay has status (LED) indictor as well to show the state of the relay at any given time.
    @cn 4-Relay unit是一个集成的4路继电器模块，可以通过I2C协议进行控制。每个继电器的最大控制电压为AC-250V/DC-28V，额定电流为10A，瞬时电流可达16A。每个继电器可以独立控制，每个继电器都有状态（LED）指示灯，以显示继电器在任何给定时间的状态。

    @color #0FE6D7
    @link https://docs.m5stack.com/en/unit/4relay
    @image https://static-cdn.m5stack.com/resource/docs/products/unit/4relay/4relay_01.webp
    @category unit

    @example
        import time
        from hardware import *
        from unit import Relay4Unit
        i2c = I2C(1, scl=33, sda=32)
        relay = Relay4Unit(i2c)
        for i in range(1, 5):
            relay.set_relay_state(i, 1)
            relay.set_led_state(i, 1)
            time.sleep(1)
            relay.set_relay_state(i, 0)
            relay.set_led_state(i, 0)
            time.sleep(1)

    """

    MODE_CTRL_REG = 0x10
    RELAY_CTRL_REG = 0x11

    ASYNC_MODE = 0
    SYNC_MODE = 1

    def __init__(self, i2c: I2C, address: int | list | tuple = 0x26) -> None:
        """! Initialize the Servo8.

        @param i2c I2C port to use.
        @param address I2C address of the servo8.
        """
        self.i2c = i2c
        self.addr = address
        self._available()

    def _available(self) -> None:
        """! Check if sensor is available on the I2C bus.

        Raises:
            Exception: If the sensor is not found.
        """
        if self.addr not in self.i2c.scan():
            raise Exception("Servo8 Hat not found, please check your connection.")

    def set_mode(self, mode: int) -> None:
        """! Set the mode of the relay.

        @en %1 Set the mode of the relay to %2.
        @cn %1 将继电器的模式设置为%2。

        @param mode [field_dropdown] The mode of the relay
               @options {
                       [async, Relay4Unit.ASYNC_MODE]
                    [sync, Relay4Unit.SYNC_MODE]
               }
        """
        self._write_reg_data(self.MODE_CTRL_REG, [mode])

    def get_mode(self) -> int:
        """! Get the mode of the relay.

        @en %1 Get the mode of the relay.
        @cn %1 获取继电器的模式。
        @return: The mode of the relay.
        """
        return self._read_reg_data(self.MODE_CTRL_REG, 1)[0]

    def get_led_state(self, n: int) -> int:
        """! Get the state of the LED.

        @en %1 Get the state of the LED %2.
        @cn %1 获取LED %2 的状态。
        @return: The state of the LED.
        """
        if n < 1 or n > 4:
            raise ValueError("The led number must be between 1 and 4.")
        return (self._read_reg_data(self.RELAY_CTRL_REG, 1)[0] >> (n + 3)) & 0x01

    def set_led_state(self, n: int, state: int) -> None:
        """! Set the state of the LED.

        @en %1 Set the state of the LED %2 to %3.
        @cn %1 设置LED %2 的状态为 %3。

        @param n The number of the LED.
        @param state The state of the LED.
        """
        if n < 1 or n > 4:
            raise ValueError("The led number must be between 1 and 4.")
            return
        if state:
            state = 1
        else:
            state = 0
        reg = self._read_reg_data(self.RELAY_CTRL_REG, 1)[0]
        if state:
            reg |= 1 << (n + 3)
        else:
            reg &= ~(1 << (n + 3))
        self._write_reg_data(self.RELAY_CTRL_REG, [reg])

    def get_relay_state(self, n: int) -> int:
        """! Get the state of the relay.

        @en %1 Get the state of the relay %2.
        @cn %1 获取继电器 %2 的状态。
        @return: The state of the relay.
        """
        if n < 1 or n > 4:
            raise ValueError("The relay number must be between 1 and 4.")
        n -= 1
        return (self._read_reg_data(self.RELAY_CTRL_REG, 1)[0] >> n) & 0x01

    def set_relay_state(self, n: int, state: int) -> None:
        """! Set the state of the relay.

        @en %1 Set the state of the relay %2 to %3.
        @cn %1 设置继电器 %2 的状态为 %3。

        @param n The number of the relay.
        @param state [field_switch] The state of the relay.
        """
        if n < 1 or n > 4:
            raise ValueError("The relay number must be between 1 and 4.")
        n -= 1
        if state:
            state = 1
        else:
            state = 0
        reg = self._read_reg_data(self.RELAY_CTRL_REG, 1)[0]
        if state:
            reg |= 1 << n
        else:
            reg &= ~(1 << n)
        self._write_reg_data(self.RELAY_CTRL_REG, [reg])

    def set_relay_all(self, state: int) -> None:
        """! Set the state of all the relay.

        @en %1 Set the state of all the relay to %2.
        @cn %1 将所有继电器的状态设置为%2。

        @param state [field_switch] The state of the relay.
        """
        if state:
            state = 0xFF
        else:
            state = 0x00
        self._write_reg_data(self.RELAY_CTRL_REG, [state])

    def _read_reg_data(self, reg: int = 0, num: int = 0) -> bytearray:
        buf = bytearray(1)
        buf[0] = reg
        time.sleep_ms(1)
        self.i2c.writeto(self.addr, buf)
        buf = bytearray(num)
        self.i2c.readfrom_into(self.addr, buf)
        return buf

    def _write_reg_data(self, reg, byte_lst):
        buf = bytearray(1 + len(byte_lst))
        buf[0] = reg
        buf[1:] = bytes(byte_lst)
        time.sleep_ms(1)
        self.i2c.writeto(self.addr, buf)
