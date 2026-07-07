# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


_i2c = None
_aw9523 = None


def _get_i2c():
    global _i2c
    if _i2c is not None:
        return _i2c

    import M5
    import machine

    board_map = {
        # boardid: (i2c, scl, sda)
        M5.BOARD.M5StamPLC: (1, 15, 13),
    }
    i2c_id, scl, sda = board_map.get(M5.getBoard(), (None, None, None))
    if i2c_id is None:
        raise NotImplementedError("I2C is not supported on this board")
    _i2c = machine.I2C(i2c_id, scl=machine.Pin(scl), sda=machine.Pin(sda), freq=400000)
    return _i2c


def get_i2c():
    """Get the shared I2C bus used by StamPLC peripherals."""
    return _get_i2c()


def _get_aw9523():
    global _aw9523
    if _aw9523 is not None:
        return _aw9523

    import M5
    from driver import aw9523

    board_map = {
        # boardid: irq_pin
        M5.BOARD.M5StamPLC: 14,
    }
    irq_pin = board_map.get(M5.getBoard(), None)
    if irq_pin is None:
        raise NotImplementedError("AW9523 is not supported on this board")
    _aw9523 = aw9523.AW9523(_get_i2c(), irq_pin=irq_pin)
    return _aw9523


def _new_aw9523_pin(pin_id: int, mode=None):
    from driver import aw9523

    _get_aw9523()
    if mode is None:
        return aw9523.Pin(pin_id)
    return aw9523.Pin(pin_id, mode=mode)


class _RelayChannel:
    def __init__(self, pin_id: int) -> None:
        from driver import aw9523

        self._pin = _new_aw9523_pin(pin_id, mode=aw9523.Pin.OUT)

    def on(self) -> None:
        self._pin.value(True)

    def off(self) -> None:
        self._pin.value(False)

    def toggle(self) -> None:
        self._pin.value(not bool(self._pin.value()))

    def value(self, state=None):
        if state is None:
            return bool(self._pin.value())
        self._pin.value(bool(state))


class _RelayBank:
    _PIN_MAP = {
        1: 0,
        2: 1,
        3: 2,
        4: 3,
    }

    def __init__(self) -> None:
        self._relays = tuple(_RelayChannel(self._PIN_MAP[channel]) for channel in range(1, 5))
        for relay in self._relays:
            relay.off()

    def _relay(self, channel):
        channel = int(channel)
        if channel < 1 or channel > len(self._relays):
            raise ValueError("Invalid relay channel")
        return self._relays[channel - 1]

    def __getitem__(self, channel):
        """Get one relay by channel, 1-4."""
        return self._relay(channel)

    def set(self, channel: int, state: bool) -> None:
        self._relay(channel).value(state)

    def get(self, channel: int) -> bool:
        return self._relay(channel).value()


class _InputBank:
    _PIN_MAP = {
        1: 4,
        2: 5,
        3: 6,
        4: 7,
        5: 12,
        6: 13,
        7: 14,
        8: 15,
    }

    def __init__(self) -> None:
        from driver import aw9523

        self.IRQ_FALLING = aw9523.Pin.IRQ_FALLING
        self.IRQ_RISING = aw9523.Pin.IRQ_RISING
        self._inputs = tuple(_new_aw9523_pin(self._PIN_MAP[channel]) for channel in range(1, 9))
        for channel, pin in enumerate(self._inputs, 1):
            pin.channel = channel

    def _input(self, channel):
        channel = int(channel)
        if channel < 1 or channel > len(self._inputs):
            raise ValueError("Invalid input channel")
        return self._inputs[channel - 1]

    def __getitem__(self, channel):
        """Get one input pin by channel, 1-8."""
        return self._input(channel)


class _PI4IOE5V6408:
    PI4IO_REG_IO_DIR = 0x03
    PI4IO_REG_OUT_SET = 0x05
    PI4IO_REG_OUT_H_IM = 0x07
    PI4IO_REG_PULL_EN = 0x0B
    PI4IO_REG_PULL_SEL = 0x0D

    def __init__(self, i2c=None, addr=0x43) -> None:
        self.i2c = _get_i2c() if i2c is None else i2c
        self.addr = addr

    def write_reg(self, reg: int, value: int) -> None:
        self.i2c.writeto_mem(self.addr, reg, bytearray([value & 0xFF]))

    def read_reg(self, reg: int) -> int:
        return self.i2c.readfrom_mem(self.addr, reg, 1)[0]

    def update_reg(self, reg: int, set_mask: int = 0, clear_mask: int = 0) -> None:
        value = self.read_reg(reg)
        value |= set_mask
        value &= ~clear_mask
        self.write_reg(reg, value)


class _LEDChannel:
    def __init__(self, bank, pin: int) -> None:
        self._bank = bank
        self._pin = pin

    def on(self) -> None:
        self.value(True)

    def off(self) -> None:
        self.value(False)

    def toggle(self) -> None:
        self.value(not self.value())

    def value(self, state=None):
        if state is None:
            return self._bank._get_pin(self._pin)
        self._bank._set_pin(self._pin, bool(state))


class _LEDBank(_PI4IOE5V6408):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

    _PIN_MAP = {
        RED: 6,
        GREEN: 5,
        BLUE: 4,
        "r": 6,
        "g": 5,
        "b": 4,
    }

    def __init__(self, i2c=None, addr=0x43) -> None:
        super().__init__(i2c=i2c, addr=addr)
        self._pin_mask = (1 << 6) | (1 << 5) | (1 << 4)
        self.update_reg(self.PI4IO_REG_IO_DIR, set_mask=self._pin_mask)
        self.update_reg(self.PI4IO_REG_OUT_H_IM, clear_mask=self._pin_mask)
        self.update_reg(self.PI4IO_REG_PULL_SEL, set_mask=self._pin_mask)
        self.update_reg(self.PI4IO_REG_PULL_EN, set_mask=self._pin_mask)
        # RGB LED is active-low, so HIGH means off.
        self.update_reg(self.PI4IO_REG_OUT_SET, set_mask=self._pin_mask)
        self.red = _LEDChannel(self, self._PIN_MAP[self.RED])
        self.green = _LEDChannel(self, self._PIN_MAP[self.GREEN])
        self.blue = _LEDChannel(self, self._PIN_MAP[self.BLUE])

    def _pin(self, color) -> int:
        if isinstance(color, str):
            pin = self._PIN_MAP.get(color.lower())
            if pin is not None:
                return pin
        else:
            color = int(color)
            if color in (4, 5, 6):
                return color
        raise ValueError("Invalid LED color")

    def _set_pin(self, pin: int, state: bool) -> None:
        pin_mask = 1 << pin
        if state:
            self.update_reg(self.PI4IO_REG_OUT_SET, clear_mask=pin_mask)
        else:
            self.update_reg(self.PI4IO_REG_OUT_SET, set_mask=pin_mask)

    def _get_pin(self, pin: int) -> bool:
        return not bool(self.read_reg(self.PI4IO_REG_OUT_SET) & (1 << pin))

    def set(self, color, state: bool) -> None:
        """Set an RGB LED color.

        :param color: ``red``, ``green``, ``blue`` or PI4IOE P4/P5/P6.
        :param bool state: True to turn on, False to turn off.
        """
        self._set_pin(self._pin(color), state)

    def get(self, color) -> bool:
        """Get an RGB LED color state."""
        return self._get_pin(self._pin(color))


class StamPLC:
    """StamPLC board IO helper.

    ``relay`` controls the four relay outputs, ``input`` reads the eight digital
    inputs, and ``led`` controls the RGB LED on PI4IOE5V6408 P6/P5/P4.
    """

    def __init__(self, i2c=None, led_addr=0x43) -> None:
        self.relay = _RelayBank()
        self.input = _InputBank()
        self.led = _LEDBank(i2c=i2c, addr=led_addr)
