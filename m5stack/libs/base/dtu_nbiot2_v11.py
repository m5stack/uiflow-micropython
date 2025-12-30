# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.simcom.sim7028 import SIM7028
import sys
import machine
import time
import M5

if sys.platform != "esp32":
    from typing import Literal
    from typing import Optional


class PY32_register:

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
        tca: "PY32IOExpander",
        base_addr: int,
        invert_value: bool = False,
        read_only: bool = False,
        initial_value: Optional[int] = None,
    ) -> None:
        self._tca = tca
        self._baseaddr = base_addr
        self._invert = invert_value
        self._ro = read_only

        # theres 2 registers in a row for each setting
        if not read_only and initial_value is not None:
            self._tca._write_reg(base_addr, initial_value)
            self._tca._write_reg(base_addr + 1, initial_value)

    def __index__(self) -> int:
        """Read all 18 bits of register data and return as one integer"""
        val = self._tca._read_reg(self._baseaddr + 1)
        val <<= 8
        val |= self._tca._read_reg(self._baseaddr)
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


class PY32IOExpander:
    def __init__(self, i2c, address=0x6F):
        self._i2c = i2c
        self._address = address
        self._buf = bytearray(1)
        self.gpio_output = PY32_register(self, 0x05, initial_value=0x00)
        self.gpio_drive = PY32_register(self, 0x13, initial_value=0x00)
        self.gpio_mode = PY32_register(self, 0x03, initial_value=0x00)

    def adc_init(self, channel: Literal[1, 2, 3, 4]):
        value = self._read_reg(0x15)
        value &= 0b1111_1000
        value |= channel
        self._write_reg(0x15, value)

        value |= 1 << 6
        self._write_reg(0x15, value)

    def adc_read(self) -> int:
        timeout = 3000
        last_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), last_time) < timeout:
            if self._read_reg(0x15) & (1 << 7) == 0:
                break

        adc_raw = self._read_reg(0x16)
        adc_raw |= (self._read_reg(0x17) & 0x0F) << 8
        return adc_raw

    def adc_read_reference(self) -> int:
        adc_raw = self._read_reg(0x27)
        adc_raw |= self._read_reg(0x28) << 8
        return adc_raw

    def _set_gpio_register(self, reg_base_addr: int, pin_number: int, value: bool) -> None:
        if not 1 <= pin_number <= 14:
            raise ValueError("Pin number must be between 1 & 14")
        pin_number -= 1
        reg_base_addr += pin_number // 8
        self._set_reg_bit(reg_base_addr, pin_number % 8, value)

    def _get_gpio_register(self, reg_base_addr: int, pin_number: int) -> bool:
        if not 1 <= pin_number <= 14:
            raise ValueError("Pin number must be between 1 & 14")
        pin_number -= 1
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

    def get_firmware_version(self):
        return self._read_reg(0x02)


class AtomDTUNBIoT2V11(SIM7028):
    """Create an AtomDTUNBIoT2V11 object.

    :param machine.UART uart: The UART object to use.
    :param bool verbose: Whether to print debug information.

    UiFlow2 Code Block:

        |nbiot_init.png|

    MicroPython Code Block:

        .. code-block:: python

            from base import AtomDTUNBIoT2V11
            from hardware import UART

            uart2 = UART(2, baudrate=115200, bits=8, parity=None, stop=1, tx=22, rx=19)
            base_nbiot2v11 = AtomDTUNBIoT2V11(uart2, verbose=False)
    """

    _pin_map = {
        M5.BOARD.M5AtomEcho: (21, 25),
        M5.BOARD.M5AtomEchoS3R: (39, 38),
        M5.BOARD.M5Atom: (21, 25),
        M5.BOARD.M5AtomMatrix: (21, 25),
        M5.BOARD.M5AtomS3: (39, 38),
        M5.BOARD.M5AtomS3Lite: (39, 38),
        M5.BOARD.M5AtomS3R: (39, 38),
        M5.BOARD.M5AtomS3R_CAM: (39, 38),
    }

    def __init__(self, uart, verbose=False):
        (scl, sda) = self._pin_map.get(M5.getBoard())
        self._i2c1 = machine.I2C(1, scl=machine.Pin(scl), sda=machine.Pin(sda), freq=100000)
        print(self._i2c1.scan())
        self._ioexpander = PY32IOExpander(self._i2c1, address=0x6F)

        # power on
        self._ioexpander.gpio_drive[9] = 0  # Set GPIO9 to open-drain
        self._ioexpander.gpio_mode[9] = 1  # Set GPIO9 to output mode
        self._ioexpander.gpio_output[9] = 1  # Set GPIO9 high
        time.sleep(1)

        # reset
        self._ioexpander.gpio_drive[11] = 0  # Set GPIO11 to open-drain
        self._ioexpander.gpio_mode[11] = 1  # Set GPIO11 to output mode
        self._ioexpander.gpio_output[11] = 0  # Set GPIO11 low
        time.sleep(0.1)
        self._ioexpander.gpio_output[11] = 1  # Set GPIO11 high

        self._ioexpander.adc_init(1)

        time.sleep(3)

        SIM7028.__init__(self, uart=uart, verbose=verbose)

    def power_on(self):
        """Power on the DTU NB-IoT module.

        UiFlow2 Code Block:

            |nbiot_power_on.png|

        MicroPython Code Block:

            .. code-block:: python

                base_nbiot2v11.power_on()
        """
        self._ioexpander.gpio_output[9] = 1  # Set GPIO9 high
        time.sleep(1)
        self._ioexpander.gpio_output[11] = 0  # Set GPIO11 low
        time.sleep(0.1)
        self._ioexpander.gpio_output[11] = 1  # Set GPIO11 high

    def power_off(self):
        """Power off the DTU NB-IoT module.

        UiFlow2 Code Block:

            |nbiot_power_off.png|

        MicroPython Code Block:

            .. code-block:: python

                base_nbiot2v11.power_off()
        """
        self._ioexpander.gpio_output[9] = 0  # Set GPIO9 low

    def get_voltage(self) -> float:
        """Get the RS485 Port voltage in volts.

        UiFlow2 Code Block:

            |rs485_get_voltage.png|

        MicroPython Code Block:

            .. code-block:: python

                voltage = base_nbiot2v11.get_voltage()
                print("Voltage:", voltage)
        """
        adc_value = self._ioexpander.adc_read()
        ref_value = self._ioexpander.adc_read_reference()
        voltage = adc_value * (ref_value / 1000.0) / 4096.0 / 0.090909
        return voltage
