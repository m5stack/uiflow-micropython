# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import machine
import micropython


def _aw9523_closure() -> tuple:  # noqa: C901
    aw = None

    class _AW9523:
        """Micropython driver for AW9523 GPIO expander.

        :param I2C i2c: The AW9523 is connected to the i2c bus.
        :param int address: The i2c address of the AW9523. Default is 0x59.
        :param int irq_pin: The pin number of the interrupt pin. Default is None.
        """

        AW9523_REG_CHIPID = 0x10  #    ///< Register for hardcode chip ID
        AW9523_REG_SOFTRESET = 0x7F  #  ///< Register for soft resetting
        AW9523_REG_INPUT0 = 0x00  #   ///< Register for reading input values
        AW9523_REG_OUTPUT0 = 0x02  #   ///< Register for writing output values
        AW9523_REG_CONFIG0 = 0x04  #   ///< Register for configuring direction
        AW9523_REG_INTENABLE0 = 0x06  # ///< Register for enabling interrupt
        AW9523_REG_GCR = 0x11  # ///< Register for general configuration
        AW9523_REG_LEDMODE = 0x12  # ///< Register for configuring const current

        def __new__(cls, *args, **kwargs) -> "_AW9523":
            nonlocal aw
            if aw is None:
                aw = super().__new__(cls)
                aw._initialized = False
            return aw

        def __init__(self, i2c, address: int = 0x59, irq_pin=None) -> None:
            self._i2c = i2c
            self._address = address
            if self._initialized:
                return

            uid = self._i2c.readfrom_mem(self._address, 0x10, 1)[0]
            if uid != 0x23:
                raise ValueError("AW9523 not found")

            self._i2c.writeto_mem(self._address, self.AW9523_REG_CONFIG0, b"\xff\xff")  # all input
            self._reg_bit_on(self.AW9523_REG_GCR, 4)  # pull up mode
            self._i2c.writeto_mem(
                self._address, self.AW9523_REG_INTENABLE0, b"\xff\xff"
            )  # no interrupt

            # clear PI4IOE5V6408 interrupt
            try:
                self._i2c.readfrom_mem(0x43, 0x13, 1)
            except OSError:
                pass

            if irq_pin is not None:
                # print("irq pin", irq_pin)
                self._irq = machine.Pin(irq_pin, machine.Pin.IN, machine.Pin.PULL_UP)
                self._irq.irq(self._irq_pin_handler, machine.Pin.IRQ_FALLING)

            self._pin_table = [None for _ in range(16)]
            self._last_input_states = [0 for _ in range(16)]
            self._initialized = True

        def apply(self, pin) -> None:
            """Apply a pin to the pin table.

            :param Pin pin: The pin to be applied. The pin is an instance of Pin.
            """
            self._pin_table[pin._id] = pin

        def unapply(self, pin) -> None:
            """Remove a pin from the pin table.

            :param Pin pin: The pin to be removed. The pin is an instance of Pin.
            """
            self._pin_table[pin._id] = None

        def pin_irq_enable(self, pid: int, en: bool) -> None:
            """enable or disable interrupt for a pin.

            :param int pid: The pin number. The pin number is 0-15.
            :param bool en: True for enable, False for disable.
            """
            register = self.AW9523_REG_INTENABLE0 + (pid >> 3)  # 8 bits per register
            if en:
                self._reg_bit_off(register, pid % 8)
            else:
                self._reg_bit_on(register, pid % 8)

        def _irq_pin_handler(self, pin: machine.Pin) -> None:
            """The interrupt handler for the interrupt pin.

            :param Pin pin: The interrupt pin. The pin is an instance of Pin.
            """
            # print("irq_handler")
            # clear interrupt
            # self._i2c.readfrom_mem(0x43, 0x13, 1)  # clear PI4IOE5V6408 interrupt
            self._i2c.readfrom_mem(self._address, self.AW9523_REG_INPUT0, 2)

            # higl level interrupt
            for i in range(16):
                if self._pin_table[i] is not None:
                    p = self._pin_table[i]
                    cur_value = p()
                    if p._mode != p.IN:
                        continue
                    if cur_value == self._last_input_states[i]:
                        continue

                    # rising or falling
                    trigger = (
                        p.IRQ_RISING if cur_value > self._last_input_states[i] else p.IRQ_FALLING
                    )
                    # trigger
                    if p.handler[trigger] is not None:
                        micropython.schedule(p.handler[trigger], p)

                    self._last_input_states[i] = cur_value

        def _reg_bit_on(self, reg: int, bit: int) -> None:
            """Turn on a bit in a register.

            :param int reg: The register address.
            :param int bit: The bit number to turn on. The bit number is 0-7.
            """
            # print("reg_bit_on", reg, bit)
            value = self._i2c.readfrom_mem(self._address, reg, 1)[0]
            self._i2c.writeto_mem(self._address, reg, bytes([value | 1 << bit]))

        def _reg_bit_off(self, reg: int, bit: int) -> None:
            """Turn off a bit in a register.

            :param int reg: The register address.
            :param int bit: The bit number to turn off. The bit number is 0-7.
            """
            # print("reg_bit_off", reg, bit)
            value = self._i2c.readfrom_mem(self._address, reg, 1)[0]
            self._i2c.writeto_mem(self._address, reg, bytes([value & ~(1 << bit)]))

        def set_pin_mode(self, pid: int, mode: int) -> None:
            """Set the mode of a pin.

            :param int pid: The pin number. The pin number is 0-15.
            :param int mode: The mode of the pin, machine.Pin.IN or machine.Pin.OUT.
            """
            register = self.AW9523_REG_CONFIG0 + (pid >> 3)
            if mode == machine.Pin.IN:
                self._reg_bit_on(register, pid % 8)  # input
            else:
                self._reg_bit_off(register, pid % 8)  # output

        def get_output_state(self, pid: int) -> int:
            """Get the output state of a pin.

            :param int pid: The pin number. The pin number is 0-15.
            :return: The output state of the pin. 1 for high, 0 for low.
            :rtype: int
            """
            register = self.AW9523_REG_OUTPUT0 + (pid >> 3)
            value = self._i2c.readfrom_mem(self._address, register, 1)[0]
            return value >> (pid % 8) & 0x01

        def set_output_state(self, pid: int, state: int) -> None:
            """Set the output state of a pin.

            :param int pid: The pin number. The pin number is 0-15.
            :param int state: The output state of the pin. 1 for high, 0 for low
            """
            register = self.AW9523_REG_OUTPUT0 + (pid >> 3)
            if state:
                self._reg_bit_on(register, pid % 8)  # high
            else:
                self._reg_bit_off(register, pid % 8)  # low

        def get_input_state(self, pid: int) -> int:
            """Get the input state of a pin.

            :param int pid: The pin number. The pin number is 0-15.
            :return: The input state of the pin. 1 for high, 0 for low.
            :rtype: int
            """
            register = self.AW9523_REG_INPUT0 + (pid >> 3)
            value = self._i2c.readfrom_mem(self._address, register, 1)[0]
            return value >> (pid % 8) & 0x01

    class _Pin:
        """The Pin class for AW9523 GPIO expander.

        :param int id: The pin number. The pin number is 0-15.
        :param int mode: The mode of the pin, machine.Pin.IN or machine.Pin.OUT. Default is machine.Pin.IN.
        :param int value: The initial value of the pin. Default is None.
        """

        IN = machine.Pin.IN
        OUT = machine.Pin.OUT

        IRQ_FALLING = machine.Pin.IRQ_FALLING
        IRQ_RISING = machine.Pin.IRQ_RISING

        def __init__(self, id, mode: int = IN, value=None) -> None:
            nonlocal aw
            if aw is None:
                raise ValueError("AW9523 not initialized")
            self._aw = aw
            self._id = id
            self._mode = mode
            self._aw.set_pin_mode(self._id, self._mode)
            if value is not None:
                self._aw.set_output_state(self._id, value)
            self._aw.apply(self)
            self.handler = {self.IRQ_FALLING: None, self.IRQ_RISING: None}

        def init(self, mode: int = -1, value=None) -> None:
            """Re-initialise the pin using the given parameters.

            :param int mode: The mode of the pin, machine.Pin.IN or machine.Pin.OUT. Default is machine.Pin.IN.
            :param int value: The initial value of the pin. Default is None.
            """
            self._aw.set_pin_mode(self._id, mode)
            if value is not None:
                self._aw.set_output_state(self._id, value)

        def value(self, *args):
            """
            This method allows to set and get the value of the pin, depending on whether
            the argument ``args`` is supplied or not.

            If the argument is omitted then this method gets the digital logic level of
            the pin, returning 0 or 1 corresponding to low and high voltage signals
            respectively.  The behaviour of this method depends on the mode of the pin:

            - ``Pin.IN`` - The method returns the actual input value currently present
                on the pin.
            - ``Pin.OUT`` - The behaviour and return value of the method is undefined.

            If the argument is supplied then this method sets the digital logic level of
            the pin.  The argument ``args`` can be anything that converts to a boolean.
            If it converts to ``True``, the pin is set to state '1', otherwise it is set
            to state '0'.  The behaviour of this method depends on the mode of the pin:

            - ``Pin.IN`` - The value is stored in the output buffer for the pin.  The
                pin state does not change, it remains in the high-impedance state.  The
                stored value will become active on the pin as soon as it is changed to
                ``Pin.OUT`` or ``Pin.OPEN_DRAIN`` mode.
            - ``Pin.OUT`` - The output buffer is set to the given value immediately.

            When setting the value this method returns ``None``.
            """
            return self.__call__(*args)

        def __call__(self, *args):
            """
            This method allows to set and get the value of the pin, depending on whether
            the argument ``args`` is supplied or not.

            If the argument is omitted then this method gets the digital logic level of
            the pin, returning 0 or 1 corresponding to low and high voltage signals
            respectively.  The behaviour of this method depends on the mode of the pin:

            - ``Pin.IN`` - The method returns the actual input value currently present
                on the pin.
            - ``Pin.OUT`` - The behaviour and return value of the method is undefined.

            If the argument is supplied then this method sets the digital logic level of
            the pin.  The argument ``args`` can be anything that converts to a boolean.
            If it converts to ``True``, the pin is set to state '1', otherwise it is set
            to state '0'.  The behaviour of this method depends on the mode of the pin:

            - ``Pin.IN`` - The value is stored in the output buffer for the pin.  The
                pin state does not change, it remains in the high-impedance state.  The
                stored value will become active on the pin as soon as it is changed to
                ``Pin.OUT`` or ``Pin.OPEN_DRAIN`` mode.
            - ``Pin.OUT`` - The output buffer is set to the given value immediately.

            When setting the value this method returns ``None``.
            """
            if len(args) == 0:
                if self._mode == self.IN:
                    return self._aw.get_input_state(self._id)
                else:
                    return self._aw.get_output_state(self._id)
            elif len(args) == 1:
                self._aw.set_output_state(self._id, args[0])

        def on(self) -> None:
            """Set pin to "1" output level."""
            self._aw.set_output_state(self._id, 1)

        def off(self) -> None:
            """Set pin to "0" output level."""
            self._aw.set_output_state(self._id, 0)

        def irq(self, handler=None, trigger=IRQ_FALLING | IRQ_RISING) -> None:
            """Enable interrupt for the pin.

            :param function handler: The interrupt handler function.
            :param int trigger: The interrupt trigger mode, machine.Pin.IRQ_FALLING or machine.Pin.IRQ_RISING.
            """
            self._aw.pin_irq_enable(self._id, True)
            self.handler[trigger] = handler

        def __del__(self) -> None:
            """De-initialise the pin."""
            self._aw.unapply(self)

        def deinit(self) -> None:
            """De-initialise the pin."""
            self._aw.unapply(self)

    return _AW9523, _Pin


AW9523, Pin = _aw9523_closure()
