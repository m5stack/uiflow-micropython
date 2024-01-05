from machine import I2C
from micropython import const
import sys

if sys.platform != "esp32":
    from typing import Literal


_REG_MODE_CH_1 = const(0x00)
_REG_OUTPUT_REG_CH_1 = const(0x10)
_REG_INPUT_REG_CH_1 = const(0x20)
_REG_ANALOG_INPUT_8B_REG_CH_1 = const(0x30)
_REG_ANALOG_INPUT_12B_REG_CH_1 = const(0x40)
_REG_SERVO_ANGLE_8B_REG_CH_1 = const(0x50)
_REG_SERVO_PULSE_16B_REG_CH_1 = const(0x60)
_REG_RGB_24B_REG_CH_1 = const(0x70)
_REG_FW_VERSION = const(0xFE)
_REG_ADDR_CONFIG = const(0xFF)

_DEFAULT_ADDRESS = const(0x45)


class Pin:
    IN = 0x01
    OUT = 0x00

    def __init__(self, port, id, mode: int = IN, value=None) -> None:
        self._port = port
        self._id = id
        self._mode = mode
        self._value = value
        self._port.set_config_mode(self._id, self._mode)
        if value is not None:
            self._port.digit_write(self._id, value)

    def init(self, mode: int = -1, value=None):
        self._port.set_config_mode(self._id, mode)
        if value is not None:
            self._port.write_output_pin(self._id, value)

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
            return self._port.read_input_pin(self._id)
        elif len(args) == 1:
            self._port.write_output_pin(self._id, args[0])

    def __call__(self, *args):
        """Pin objects are callable. The call method provides a (fast) shortcut
        to set and get the value of the pin. It is equivalent to Pin.value([x]).
        See Pin.value() for more details.
        """
        if len(args) == 0:
            return self._port.read_input_pin(self._id)
        elif len(args) == 1:
            self._port.write_output_pin(self._id, args[0])

    def on(self):
        self._port.write_output_pin(self._id, 1)

    def off(self):
        self._port.write_output_pin(self._id, 0)


class EXTIO2Unit:
    IN = const(0)
    OUT = const(1)
    ANALOG = const(2)
    SERVO = const(3)
    NEOPIXEL = const(4)

    def __init__(self, i2c: I2C, address: int = _DEFAULT_ADDRESS) -> None:
        self._i2c = i2c
        self._addr = address
        self._BUFFER = memoryview(bytearray(3))

    def set_config_mode(self, id: int, mode: Literal[0, 1, 2, 3, 4]) -> None:
        self._write_u8(_REG_MODE_CH_1 + id, mode)

    def write_output_pin(self, id: int, value: Literal[0, 1]) -> None:
        self._write_u8(_REG_OUTPUT_REG_CH_1 + id, value)

    def write_servo_angle(self, id: int, angle: int) -> None:
        self._write_u8(_REG_SERVO_ANGLE_8B_REG_CH_1 + id, angle)

    def write_servo_pluse(self, id: int, pluse: int) -> None:
        self._write_u16(_REG_SERVO_PULSE_16B_REG_CH_1 + (id * 2), pluse & 0xFF, pluse >> 8)

    def write_rgb_led(self, id: int, value) -> None:
        r = (value >> 16) & 0xFF
        g = (value >> 8) & 0xFF
        b = value & 0xFF
        self._write_u24(_REG_RGB_24B_REG_CH_1 + (id * 3), r, g, b)

    def set_address(self, address: int) -> None:
        self._write_u8(_REG_ADDR_CONFIG, address & 0xFF)
        self._addr = address

    def get_config_mode(self, id: int) -> None:
        return self._read_u8(_REG_MODE_CH_1 + id)

    def read_input_pin(self, id: int) -> int:
        return self._read_u8(_REG_INPUT_REG_CH_1 + id)

    def read_adc8_pin(self, id: int) -> int:
        return self._read_u8(_REG_ANALOG_INPUT_8B_REG_CH_1 + id)

    def read_adc12_pin(self, id: int) -> int:
        return self._read_u16(_REG_ANALOG_INPUT_12B_REG_CH_1 + (id * 2))

    def read_servo_angle(self, id: int) -> int:
        return self._read_u8(_REG_SERVO_ANGLE_8B_REG_CH_1 + id)

    def read_servo_pulse(self, id: int) -> int:
        return self._read_u16(_REG_SERVO_PULSE_16B_REG_CH_1 + (id * 2))

    def read_rgb_led(self, id: int) -> int:
        return self._read_u24(_REG_RGB_24B_REG_CH_1 + (id * 3))

    def read_fw_version(self) -> int:
        return self._read_u8(_REG_FW_VERSION)

    def get_address(self) -> int:
        return self._read_u8(_REG_ADDR_CONFIG)

    def Pin(self, id, mode: int = IN, value=None):
        return Pin(self, id, mode, value)

    def _write_u8(self, reg: int, val: int) -> None:
        buf = self._BUFFER[0:1]
        buf[0] = val & 0xFF
        self._i2c.writeto_mem(self._addr, reg & 0xFF, buf)

    def _write_u16(self, reg: int, *vals) -> None:
        buf = self._BUFFER[0:2]
        buf[0] = vals[0] & 0xFF
        buf[1] = vals[1] & 0xFF
        self._i2c.writeto_mem(self._addr, reg & 0xFF, buf)

    def _write_u24(self, reg: int, *vals) -> None:
        buf = self._BUFFER[0:3]
        buf[0] = vals[0] & 0xFF
        buf[1] = vals[1] & 0xFF
        buf[2] = vals[2] & 0xFF
        self._i2c.writeto_mem(self._addr, reg & 0xFF, buf)

    def _read_u8(self, reg: int) -> int:
        buf = self._BUFFER[0:1]
        buf[0] = reg & 0xFF
        self._i2c.writeto(self._addr, buf)
        self._i2c.readfrom_into(self._addr, buf)
        return buf[0]

    def _read_u16(self, reg: int) -> int:
        buf = self._BUFFER[0:1]
        buf[0] = reg & 0xFF
        self._i2c.writeto(self._addr, buf)
        buf = self._BUFFER[0:2]
        self._i2c.readfrom_into(self._addr, buf)
        return buf[0] | (buf[1] << 8)

    def _read_u24(self, reg: int) -> int:
        buf = self._BUFFER[0:1]
        buf[0] = reg & 0xFF
        self._i2c.writeto(self._addr, buf)
        buf = self._BUFFER[0:3]
        self._i2c.readfrom_into(self._addr, buf)
        return buf[0] << 16 | (buf[1] << 8) | buf[2]
