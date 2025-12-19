# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 ladyada for Adafruit Industries
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import sys
import micropython

if sys.platform != "esp32":
    from typing import Optional


class RWBit:
    """
    Single bit register that is readable and writeable.

    Values are `bool`

    :param int register_address: The register address to read the bit from
    :param int bit: The bit index within the byte at ``register_address``
    :param int register_width: The number of bytes in the register. Defaults to 1.
    :param bool lsb_first: Is the first byte we read from I2C the LSB? Defaults to true

    """

    def __init__(
        self,
        register_address: int,
        bit: int,
        register_width: int = 1,
        lsb_first: bool = True,
    ) -> None:
        self.bit_mask = 1 << (bit % 8)  # the bitmask *within* the byte!
        self.buffer = bytearray(register_width)
        self.register_address = register_address
        if lsb_first:
            self.byte = bit // 8  # the byte number within the buffer
        else:
            self.byte = register_width - (bit // 8)  # the byte number within the buffer

    def __get__(
        self,
        obj,
        objtype=None,
    ) -> bool:
        i2c = obj.i2c if hasattr(obj, "i2c") else obj._i2c
        address = obj._address if hasattr(obj, "_address") else obj.address
        if i2c is None or address is None:
            raise RuntimeError("I2C device not initialized or address not set")
        i2c.readfrom_mem_into(address, self.register_address, self.buffer)
        return bool(self.buffer[self.byte] & self.bit_mask)

    def __set__(self, obj, value: bool) -> None:
        i2c = obj.i2c if hasattr(obj, "i2c") else obj._i2c
        address = obj._address if hasattr(obj, "_address") else obj.address
        if i2c and address:
            i2c.readfrom_mem_into(address, self.register_address, self.buffer)
            if value:
                self.buffer[self.byte] |= self.bit_mask
            else:
                self.buffer[self.byte] &= ~self.bit_mask
            i2c.writeto_mem(address, self.register_address, self.buffer)


class ROBit(RWBit):
    """Single bit register that is read only. Subclass of `RWBit`.

    Values are `bool`

    :param int register_address: The register address to read the bit from
    :param type bit: The bit index within the byte at ``register_address``
    :param int register_width: The number of bytes in the register. Defaults to 1.

    """

    def __set__(self, obj, value: bool) -> None:
        raise AttributeError()


class RWBits:
    """
    Multibit register (less than a full byte) that is readable and writeable.
    This must be within a byte register.

    Values are `int` between 0 and 2 ** ``num_bits`` - 1.

    :param int num_bits: The number of bits in the field.
    :param int register_address: The register address to read the bit from
    :param int lowest_bit: The lowest bits index within the byte at ``register_address``
    :param int register_width: The number of bytes in the register. Defaults to 1.
    :param bool lsb_first: Is the first byte we read from I2C the LSB? Defaults to true
    :param bool signed: If True, the value is a "two's complement" signed value.
                        If False, it is unsigned.
    """

    def __init__(
        self,
        num_bits: int,
        register_address: int,
        lowest_bit: int,
        register_width: int = 1,
        lsb_first: bool = True,
        signed: bool = False,
    ) -> None:
        self.bit_mask = ((1 << num_bits) - 1) << lowest_bit
        # print("bitmask: ",hex(self.bit_mask))
        if self.bit_mask >= 1 << (register_width * 8):
            raise ValueError("Cannot have more bits than register size")
        self.lowest_bit = lowest_bit
        self.register_address = register_address
        self.buffer = bytearray(register_width)
        self.lsb_first = lsb_first
        self.sign_bit = (1 << (num_bits - 1)) if signed else 0

    def __get__(self, obj, objtype=None) -> int:
        i2c = obj.i2c if hasattr(obj, "i2c") else obj._i2c
        address = obj._address if hasattr(obj, "_address") else obj.address
        if i2c is None or address is None:
            raise RuntimeError("I2C device not initialized or address not set")
        i2c.readfrom_mem_into(address, self.register_address, self.buffer)
        # read the number of bytes into a single variable
        reg = 0
        order = None
        if not self.lsb_first:
            order = range(len(self.buffer))
        else:
            order = range(len(self.buffer) - 1, -1, -1)
        for i in order:
            reg = (reg << 8) | self.buffer[i]
        reg = (reg & self.bit_mask) >> self.lowest_bit
        # If the value is signed and negative, convert it
        if reg & self.sign_bit:
            reg -= 2 * self.sign_bit
        return reg

    def __set__(self, obj, value: int) -> None:
        value <<= self.lowest_bit  # shift the value over to the right spot
        i2c = obj.i2c if hasattr(obj, "i2c") else obj._i2c
        address = obj._address if hasattr(obj, "_address") else obj.address
        if i2c and address:
            reg = 0
            order = range(len(self.buffer), 0, -1)
            if not self.lsb_first:
                order = range(1, len(self.buffer))
            for i in order:
                reg = (reg << 8) | self.buffer[i]
            # print("old reg: ", hex(reg))
            reg &= ~self.bit_mask  # mask off the bits we're about to change
            reg |= value  # then or in our new value
            # print("new reg: ", hex(reg))
            for i in reversed(order):
                self.buffer[i] = reg & 0xFF
                reg >>= 8
            i2c.writeto_mem(address, self.register_address, self.buffer)


class ROBits(RWBits):
    """
    Multibit register (less than a full byte) that is read-only. This must be
    within a byte register.

    Values are `int` between 0 and 2 ** ``num_bits`` - 1.

    :param int num_bits: The number of bits in the field.
    :param int register_address: The register address to read the bit from
    :param type lowest_bit: The lowest bits index within the byte at ``register_address``
    :param int register_width: The number of bytes in the register. Defaults to 1.
    """

    def __set__(self, obj, value: int) -> None:
        raise AttributeError()


class TCA8418_register:
    """A class for interacting with the TCA8418 registers

    :param TCA8418 tca: The associated TCA8418 object
    :param int base_addr: The base address for this register
    :param bool invert_value: Whether the value given should be interpreted as inverted
        (True -> False), default is False (inputs are as-is, not inverted)
    :param bool read_only: Whether the register is read-only or read/write, default
        is False (register is read/write)
    :param int|None initial_value: An initial value to provide to the register, default
        is ``None`` (no default is provided)
    """

    def __init__(
        self,
        tca: "TCA8418",
        base_addr: int,
        invert_value: bool = False,
        read_only: bool = False,
        initial_value: Optional[int] = None,
    ) -> None:
        self._tca = tca
        self._baseaddr = base_addr
        self._invert = invert_value
        self._ro = read_only

        # theres 3 registers in a row for each setting
        if not read_only and initial_value is not None:
            self._tca._write_reg(base_addr, initial_value)
            self._tca._write_reg(base_addr + 1, initial_value)
            self._tca._write_reg(base_addr + 2, initial_value)

    def __index__(self) -> int:
        """Read all 18 bits of register data and return as one integer"""
        val = self._tca._read_reg(self._baseaddr + 2)
        val <<= 8
        val |= self._tca._read_reg(self._baseaddr + 1)
        val <<= 8
        val |= self._tca._read_reg(self._baseaddr)
        val &= 0x3FFFF
        return val

    def __getitem__(self, pin_number: int) -> bool:
        """Read the single bit at 'pin_number' offset"""
        value = self._tca._get_gpio_register(self._baseaddr, pin_number)
        if self._invert:
            value = not value
        return value

    def __setitem__(self, pin_number: int, value: bool) -> None:
        """Set a single bit at 'pin_number' offset to 'value'"""
        if self._ro:
            raise NotImplementedError("Read only register")
        if self._invert:
            value = not value
        self._tca._set_gpio_register(self._baseaddr, pin_number, value)


class TCA8418:
    _TCA8418_REG_CONFIG = micropython.const(0x01)
    _TCA8418_REG_INTSTAT = micropython.const(0x02)
    _TCA8418_REG_KEYLCKEC = micropython.const(0x03)
    _TCA8418_REG_KEYEVENT = micropython.const(0x04)

    _TCA8418_REG_GPIODATSTAT1 = micropython.const(0x14)
    _TCA8418_REG_GPIODATOUT1 = micropython.const(0x17)
    _TCA8418_REG_INTEN1 = micropython.const(0x1A)
    _TCA8418_REG_KPGPIO1 = micropython.const(0x1D)
    _TCA8418_REG_GPIOINTSTAT1 = micropython.const(0x11)
    _TCA8418_REG_GPIOINTSTAT2 = micropython.const(0x12)
    _TCA8418_REG_GPIOINTSTAT3 = micropython.const(0x13)

    _TCA8418_REG_EVTMODE1 = micropython.const(0x20)
    _TCA8418_REG_GPIODIR1 = micropython.const(0x23)
    _TCA8418_REG_INTLVL1 = micropython.const(0x26)
    _TCA8418_REG_DEBOUNCEDIS1 = micropython.const(0x29)
    _TCA8418_REG_GPIOPULL1 = micropython.const(0x2C)

    R0 = 0
    R1 = 1
    R2 = 2
    R3 = 3
    R4 = 4
    R5 = 5
    R6 = 6
    R7 = 7
    C0 = 8
    C1 = 9
    C2 = 10
    C3 = 11
    C4 = 12
    C5 = 13
    C6 = 14
    C7 = 15
    C8 = 16
    C9 = 17

    events_count = ROBits(4, _TCA8418_REG_KEYLCKEC, 0)
    cad_int = RWBit(_TCA8418_REG_INTSTAT, 4)
    overflow_int = RWBit(_TCA8418_REG_INTSTAT, 3)
    keylock_int = RWBit(_TCA8418_REG_INTSTAT, 2)
    gpi_int = RWBit(_TCA8418_REG_INTSTAT, 1)
    key_int = RWBit(_TCA8418_REG_INTSTAT, 0)

    gpi_event_while_locked = RWBit(_TCA8418_REG_CONFIG, 6)
    overflow_mode = RWBit(_TCA8418_REG_CONFIG, 5)
    int_retrigger = RWBit(_TCA8418_REG_CONFIG, 4)
    overflow_intenable = RWBit(_TCA8418_REG_CONFIG, 3)
    keylock_intenable = RWBit(_TCA8418_REG_CONFIG, 2)
    GPI_intenable = RWBit(_TCA8418_REG_CONFIG, 1)
    key_intenable = RWBit(_TCA8418_REG_CONFIG, 0)

    def __init__(self, i2c, address=0x34):
        self._i2c = i2c
        self._address = address
        self._buf = bytearray(1)

        # disable all interrupt
        self.enable_int = TCA8418_register(self, self._TCA8418_REG_INTEN1, initial_value=0)
        self.gpio_int_status = TCA8418_register(
            self, self._TCA8418_REG_GPIOINTSTAT1, read_only=True
        )
        _ = self.gpio_int_status  # read to clear
        self.gpio_int_status = TCA8418_register(
            self, self._TCA8418_REG_GPIOINTSTAT2, read_only=True
        )
        _ = self.gpio_int_status  # read to clear
        self.gpio_int_status = TCA8418_register(
            self, self._TCA8418_REG_GPIOINTSTAT3, read_only=True
        )
        _ = self.gpio_int_status  # read to clear

        # set all pins to inputs
        self.gpio_direction = TCA8418_register(self, self._TCA8418_REG_GPIODIR1, initial_value=0)
        # set all pins to GPIO
        self.gpio_mode = TCA8418_register(
            self, self._TCA8418_REG_KPGPIO1, invert_value=True, initial_value=0
        )
        self.keypad_mode = TCA8418_register(self, self._TCA8418_REG_KPGPIO1)
        # set all pins low output
        self.output_value = TCA8418_register(self, self._TCA8418_REG_GPIODATOUT1, initial_value=0)
        self.input_value = TCA8418_register(self, self._TCA8418_REG_GPIODATSTAT1, read_only=True)
        # enable all pullups
        self.pullup = TCA8418_register(
            self, self._TCA8418_REG_GPIOPULL1, invert_value=True, initial_value=0
        )
        # enable all debounce
        self.debounce = TCA8418_register(
            self, self._TCA8418_REG_DEBOUNCEDIS1, invert_value=True, initial_value=0
        )
        # default int on falling
        self.int_on_rising = TCA8418_register(self, self._TCA8418_REG_INTLVL1, initial_value=0)

        # default no gpio in event queue
        self.event_mode_fifo = TCA8418_register(self, self._TCA8418_REG_EVTMODE1, initial_value=0)

        # read in event queue
        # print(self.events_count, "events")
        while self.events_count:
            _ = self.next_event  # read and toss

        # reset interrutps
        self._write_reg(self._TCA8418_REG_INTSTAT, 0x1F)
        self.gpi_int = False

    @property
    def next_event(self) -> int:
        """The next key event"""
        return self._read_reg(self._TCA8418_REG_KEYEVENT)

    def _set_gpio_register(self, reg_base_addr: int, pin_number: int, value: bool) -> None:
        if not 0 <= pin_number <= 17:
            raise ValueError("Pin number must be between 0 & 17")
        reg_base_addr += pin_number // 8
        self._set_reg_bit(reg_base_addr, pin_number % 8, value)

    def _get_gpio_register(self, reg_base_addr: int, pin_number: int) -> bool:
        if not 0 <= pin_number <= 17:
            raise ValueError("Pin number must be between 0 & 17")
        reg_base_addr += pin_number // 8
        return self._get_reg_bit(reg_base_addr, pin_number % 8)

    # register helpers

    def _set_reg_bit(self, addr: int, bitoffset: int, value: bool) -> None:
        temp = self._read_reg(addr)
        if value:
            temp |= 1 << bitoffset
        else:
            temp &= ~(1 << bitoffset)
        self._write_reg(addr, temp)

    def _get_reg_bit(self, addr: int, bitoffset: int) -> bool:
        temp = self._read_reg(addr)
        return bool(temp & (1 << bitoffset))

    def _read_reg(self, addr: int) -> int:
        self._i2c.readfrom_mem_into(self._address, addr, self._buf)
        # print("readfrom_mem_into reg:", hex(addr), "val:", hex(self._buf[0]))
        return self._buf[0]

    def _write_reg(self, addr: int, val: int) -> None:
        # print("writeto_mem reg:", hex(addr), "val:", hex(val))
        self._buf[0] = val & 0xFF
        self._i2c.writeto_mem(self._address, addr, self._buf)
