# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


class ACStamPLC:
    """ACStamPLC with relay and RGB LED control via PI4IOE I2C GPIO expander.
    """
    # PI4IOE register addresses
    PI4IO_REG_IO_DIR = 0x03    # I/O direction register (0=input, 1=output)
    PI4IO_REG_OUT_SET = 0x05   # Output port register
    PI4IO_REG_OUT_H_IM = 0x07  # Output high-impedance register
    PI4IO_REG_PULL_EN = 0x0B   # Pull-up/pull-down enable register
    PI4IO_REG_PULL_SEL = 0x0D  # Pull-up/pull-down selection register (0=down, 1=up)
    # Pin definitions
    PIN_RELAY = 2  # P2 -> REL_EN
    PIN_LED_R = 5  # P5 -> LEDR
    PIN_LED_G = 6  # P6 -> LEDG
    PIN_LED_B = 7  # P7 -> LEDB

    def __init__(self, i2c=None, addr=0x44):
        """Initialize ACStamPLC

        @param i2c I2C instance. If None, will try to get from hardware.plcio
        @param addr PI4IOE I2C address, default is 0x44
        """     
        if i2c is None:
            plcio = __import__("hardware.plcio", None, None, True, 0)
            self.i2c = plcio.get_i2c()
        else:
            self.i2c = i2c
        self.addr = addr

        self.output_mask = (
            (1 << self.PIN_RELAY)
            | (1 << self.PIN_LED_R)
            | (1 << self.PIN_LED_G)
            | (1 << self.PIN_LED_B)
        )
        self.write_reg(self.PI4IO_REG_IO_DIR, self.output_mask)
        # Disable high-impedance mode for output pins
        self.write_reg(self.PI4IO_REG_OUT_H_IM, 0x00)
        # Enable pull-up for output pins (optional, for better signal stability)
        self.write_reg(self.PI4IO_REG_PULL_SEL, self.output_mask)
        self.write_reg(self.PI4IO_REG_PULL_EN, self.output_mask)
        # Initialize all outputs to LOW (relay off, LEDs off)
        self.write_reg(self.PI4IO_REG_OUT_SET, 0x00)

    def write_reg(self, reg, value):
        """Write a value to PI4IOE register
        :param reg Register address
        :param value Value to write (0-255)
        """
        self.i2c.writeto_mem(self.addr, reg, bytearray([value]))

    def read_reg(self, reg) -> int:
        """Read a register from PI4IOE
        :param reg Register address
        :return Register value (0-255)
        """
        return self.i2c.readfrom_mem(self.addr, reg, 1)[0]

    def _set_pin(self, pin: int, state: bool):
        """Set a single pin state
        :param pin Pin number (0-7)
        :param state True for HIGH, False for LOW
        """
        current = self.read_reg(self.PI4IO_REG_OUT_SET)
        if state:
            current |= 1 << pin
        else:
            current &= ~(1 << pin)
        self.write_reg(self.PI4IO_REG_OUT_SET, current)

    def set_relay(self, state: bool) -> None:
        """Set relay state
        :param bool state: True to turn on, False to turn off
        """
        self._set_pin(self.PIN_RELAY, state)

    def set_red_led(self, state: bool) -> None:
        """Set red LED state
        :param bool state: True to turn on, False to turn off
        """
        self._set_pin(self.PIN_LED_R, not state)

    def set_green_led(self, state: bool) -> None:
        """Set green LED state
        :param bool state: True to turn on, False to turn off
        """
        self._set_pin(self.PIN_LED_G, not state)

    def set_blue_led(self, state: bool):
        """Set blue LED state
        :param bool state: True to turn on, False to turn off
        """
        self._set_pin(self.PIN_LED_B, not state)

