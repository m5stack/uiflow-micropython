from machine import I2C
import time
import micropython

try:
    from micropython import const
except ImportError:

    def const(expr):
        return expr


try:
    from typing_extensions import Literal
except ImportError:
    pass

_REGISTER_INPUT = const(0x00)
_REGISTER_OUTPUT = const(0x01)
_REGISTER_POLARITY_INVERSION = const(0x02)
_REGISTER_CONFIG = const(0x03)

_PCA9554_DEFAULT_ADDRESS = const(0x27)


class Pin:
    IN = 0x01
    OUT = 0x00

    def __init__(self, port, id, mode: int = IN, value=None) -> None:
        self._port = port
        self._id = id
        self._mode = mode
        self._value = value
        self._port.set_pin_mode(self._id, self._mode)
        if value is not None:
            self._port.digit_write(self._id, value)

    def init(self, mode: int = -1, value=None):
        self._port.set_pin_mode(self._id, mode)
        if value is not None:
            self._port.digit_write(self._id, value)

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
            return self._port.digit_read(self._id)
        elif len(args) == 1:
            self._port.digit_write(self._id, args[0])

    def __call__(self, *args):
        """Pin objects are callable. The call method provides a (fast) shortcut
        to set and get the value of the pin. It is equivalent to Pin.value([x]).
        See Pin.value() for more details.
        """
        if len(args) == 0:
            return self._port.digit_read(self._id)
        elif len(args) == 1:
            self._port.digit_write(self._id, args[0])

    def on(self):
        self._port.digit_write(self._id, 1)

    def off(self):
        self._port.digit_write(self._id, 0)


class PCA9554:
    IN = 0x01
    OUT = 0x00

    def __init__(self, i2c: I2C, address: int = _PCA9554_DEFAULT_ADDRESS) -> None:
        self._i2c = i2c
        self._addr = address
        self._BUFFER = memoryview(bytearray(3))

    def set_port_mode(self, mode: Literal[0x00, 0x01]) -> None:
        self._write_u8(_REGISTER_CONFIG, 0xFF if mode == 0x01 else 0x00)

    def set_pin_mode(self, id: int, mode: Literal[0x00, 0x01]) -> None:
        config = self._read_u8(_REGISTER_CONFIG)
        config &= ~(1 << id)
        config |= mode << id
        self._write_u8(_REGISTER_CONFIG, config)

    def digit_write_port(self, value: int) -> None:
        self._write_u8(_REGISTER_OUTPUT, value)

    def digit_write(self, id: int, value: int) -> None:
        out = self._read_u8(_REGISTER_OUTPUT)
        out &= ~(1 << id)
        out |= value << id
        self._write_u8(_REGISTER_OUTPUT, out)

    def digit_read_port(self) -> int:
        return self._read_u8(_REGISTER_INPUT)

    def digit_read(self, id) -> int:
        input = self._read_u8(_REGISTER_INPUT)
        return 1 if (input & (1 << id)) else 0

    def _read_u8(self, reg: int) -> int:
        buf = self._BUFFER[0:1]
        self._i2c.readfrom_mem_into(self._addr, reg & 0xFF, buf)
        return buf[0]

    def _write_u8(self, reg: int, val: int) -> None:
        buf = self._BUFFER[0:1]
        buf[0] = val & 0xFF
        self._i2c.writeto_mem(self._addr, reg & 0xFF, buf)

    def Pin(self, id, mode: int = IN, value=None):
        return Pin(self, id, mode, value)
