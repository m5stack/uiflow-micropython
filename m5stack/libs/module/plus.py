# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .mbus import i2c1


class PLUSModule:
    """! PLUS is a enhanced M5 module comes with lithium polymer battery(500mAh), gear potentiometer, IR transmitter, extend PORT B(GPIO Port), PORT C(UART Port) from M5 core and a Microphone soldering pad.

    @en Module PLUS 英文介绍
    @cn Module PLUS 中文介绍

    @color #0FE6D7
    @link https://docs.m5stack.com/en/module/plus
    @image https://static-cdn.m5stack.com/resource/docs/products/module/plus/plus_01.webp
    @category module
    """

    _PLUS_ADDR = 0x62

    def __init__(self, address: int | list | tuple = _PLUS_ADDR) -> None:
        """! Init I2C Module PLUS I2C Address.

        @param address I2C address of the PLUSModule.
        """
        self._i2c = i2c1
        self._i2c_addr = address
        if self._i2c_addr not in self._i2c.scan():
            raise Exception("PLUS Module not found in Base")
        self._encode_value = 0
        self._zero_value = 0
        self._last_value = self.get_rotary_value()
        self._last_increment_value = self._last_value
        self._zero_value = self._last_value

    def get_rotary_value(self) -> int:
        """Get the current value of the rotary.

        @return: The value of the rotary relative to the zero point.
        """
        buf = self._i2c.readfrom_mem(self._i2c_addr, self._PLUS_ADDR, 2)
        byte_value = buf[0]

        if byte_value & 0x80:
            byte_value -= 256
        self._encode_value += byte_value

        current_value = self._encode_value - self._zero_value
        self._last_value = self._encode_value
        return current_value

    def reset_rotary_value(self) -> None:
        self._zero_value = self.get_rotary_value()

    def set_rotary_value(self, value: int) -> None:
        """! Set the rotary value.

        @param value: rotary value.
        """
        self._encode_value = value

    def get_rotary_increments(self) -> int:
        """Get the increments of the rotary value since the last call of this function.

        @return: The increment value of the rotary.
        """
        current_value = self.get_rotary_value()
        increments = current_value - self._last_increment_value
        if increments != 0:
            self._last_increment_value = current_value
        return increments

    def get_button_status(self) -> bool:
        """! Get the state of a specific button.

        @return: The state of the button.
        """
        data = self._i2c.readfrom(self._PLUS_ADDR, 2)
        return bool(data[1] != 0xFF)
