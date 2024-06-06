# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from .unit_helper import UnitError
import time
import machine


class ACSSRI2CUnit:
    def __init__(self, i2c, address=0x50) -> None:
        self._i2c = i2c
        self._address = address
        if self._address not in self._i2c.scan():
            raise UnitError("AC/DCSSR unit not found in Grove")

    def on(self):
        self._i2c.writeto_mem(self._address, 0x00, bytes([1]))

    def off(self):
        self._i2c.writeto_mem(self._address, 0x00, bytes([0]))

    def value(self, *args):
        """This method allows to set and get the value of the pin, depending on
        whether the argument x is supplied or not.

        If the argument is omitted then this method gets the digital logic level
        of the pin, returning 0 or 1 corresponding to low and high voltage
        signals respectively. The behaviour of this method depends on the mode
        of the pin:

            ``Pin.IN`` - The method returns the actual input value currently
            present on the pin.

            ``Pin.OUT`` - The behaviour and return value of the method is undefined.

        If the argument is supplied then this method sets the digital logic
        level of the pin. The argument x can be anything that converts to a
        boolean. If it converts to True, the pin is set to state ‘1’, otherwise
        it is set to state ‘0’. The behaviour of this method depends on the mode
        of the pin:

            ``Pin.IN`` - The value is stored in the output buffer for the pin.
            The pin state does not change, it remains in the high-impedance state.
            The stored value will become active on the pin as soon as it is
            changed to Pin.OUT or Pin.OPEN_DRAIN mode.

            ``Pin.OUT`` - The output buffer is set to the given value immediately.

        When setting the value this method returns None.
        """
        if len(args) == 0:
            return self._i2c.readfrom_mem(self._address, 0x00, 1)[0]
        elif len(args) == 1:
            self._i2c.writeto_mem(self._address, 0x00, bytes([args[0]]))

    def __call__(self, *args):
        """Pin objects are callable. The call method provides a (fast) shortcut
        to set and get the value of the pin. It is equivalent to Pin.value([x]).
        See Pin.value() for more details.
        """
        if len(args) == 0:
            return self._i2c.readfrom_mem(self._address, 0x00, 1)[0]
        elif len(args) == 1:
            self._i2c.writeto_mem(self._address, 0x00, bytes([args[0]]))

    def fill_color(self, rgb: int = 0) -> None:
        self._i2c.writeto_mem(self._address, 0x10, rgb.to_bytes(3, "big"))

    def get_firmware_version(self) -> int:
        return self._i2c.readfrom_mem(self._address, 0xFE, 1)[0]

    def set_address(self, new_address):
        self._i2c.writeto_mem(self._address, 0x20, bytes([new_address]))
        self._address = new_address
        time.sleep(5)


class ACSSRModbusUnit:
    def __init__(self, bus, address=0x04) -> None:
        self._modbus = bus
        self._address = address
        if self.get_firmware_version() != 1:
            raise UnitError("AC/DCSSR unit not found in modbus")

    def on(self):
        self._modbus.write_single_coil(self._address, 0x0000, True)

    def off(self):
        self._modbus.write_single_coil(self._address, 0x0000, False)

    def value(self, *args):
        """This method allows to set and get the value of the pin, depending on
        whether the argument x is supplied or not.

        If the argument is omitted then this method gets the digital logic level
        of the pin, returning 0 or 1 corresponding to low and high voltage
        signals respectively. The behaviour of this method depends on the mode
        of the pin:

            ``Pin.IN`` - The method returns the actual input value currently
            present on the pin.

            ``Pin.OUT`` - The behaviour and return value of the method is undefined.

        If the argument is supplied then this method sets the digital logic
        level of the pin. The argument x can be anything that converts to a
        boolean. If it converts to True, the pin is set to state ‘1’, otherwise
        it is set to state ‘0’. The behaviour of this method depends on the mode
        of the pin:

            ``Pin.IN`` - The value is stored in the output buffer for the pin.
            The pin state does not change, it remains in the high-impedance state.
            The stored value will become active on the pin as soon as it is
            changed to Pin.OUT or Pin.OPEN_DRAIN mode.

            ``Pin.OUT`` - The output buffer is set to the given value immediately.

        When setting the value this method returns None.
        """
        if len(args) == 0:
            return self._modbus.read_coils(self._address, 0x0000, 1)[0]
        elif len(args) == 1:
            self._modbus.write_single_coil(self._address, 0x0000, args[0])

    def __call__(self, *args):
        """Pin objects are callable. The call method provides a (fast) shortcut
        to set and get the value of the pin. It is equivalent to Pin.value([x]).
        See Pin.value() for more details.
        """
        if len(args) == 0:
            return self._modbus.read_coils(self._address, 0x0000, 1)[0]
        elif len(args) == 1:
            self._modbus.write_single_coil(self._address, 0x0000, args[0])

    def fill_color(self, rgb: int = 0) -> None:
        rgb565 = ((rgb >> 19) << 11) | (((rgb >> 10) & 0x3F) << 5) | (rgb & 0x1F)
        self._modbus.write_single_register(self._address, 0, rgb565)

    def get_firmware_version(self) -> int | None:
        resp = self._modbus.read_holding_registers(self._address, 0x0001, 1)
        return resp[0] if resp else None

    def set_address(self, new_address):
        self._modbus.write_single_register(self._address, 0x0002, new_address)


class ACSSRUnit:
    def __new__(cls, bus, address=0x50) -> None:
        if isinstance(bus, machine.I2C):
            return ACSSRI2CUnit(bus, address)
        if hasattr(bus, "read_coils"):
            return ACSSRModbusUnit(bus, address)


DCSSRUnit = ACSSRUnit
