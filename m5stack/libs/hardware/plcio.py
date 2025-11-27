# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from driver import aw9523
import M5
import machine


def _plc_closure() -> tuple:
    aw = None
    i2c = None  # Shared I2C instance for all stamplc devices

    def _init_i2c():
        """Initialize the shared I2C instance for stamplc devices.

        :returns: The I2C instance.
        :rtype: machine.I2C
        """
        nonlocal i2c
        if i2c is not None:
            return i2c
        _board_map = {
            # boardid: (i2c, scl, sda, irq_pin)
            M5.BOARD.M5StamPLC: (1, 15, 13, 14),
        }
        i2c_id, scl, sda, irq_pin = _board_map.get(M5.getBoard(), (None, None, None, None))
        if i2c_id is None:
            raise NotImplementedError("I2C is not supported on this board")
        # Create shared I2C instance
        i2c = machine.I2C(i2c_id, scl=machine.Pin(scl), sda=machine.Pin(sda), freq=400000)
        return i2c

    def _aw9523_init():
        """Initialize AW9523 GPIO expander.

        :returns: AW9523 instance.
        :rtype: aw9523.AW9523
        """
        nonlocal aw, i2c
        if aw is not None:
            return aw
        # Ensure I2C is initialized first
        if i2c is None:
            _init_i2c()
        _board_map = {
            # boardid: irq_pin
            M5.BOARD.M5StamPLC: 14,
        }
        irq_pin = _board_map.get(M5.getBoard(), None)
        if irq_pin is None:
            raise NotImplementedError("AW9523 is not supported on this board")
        aw = aw9523.AW9523(i2c, irq_pin=irq_pin)
        return aw

    def get_i2c():
        """Get the I2C instance used by plcio.

        This function initializes the I2C if not already initialized,
        and returns the I2C instance that can be reused by other modules
        like ACStamPLC.

        :returns: The I2C instance.
        :rtype: machine.I2C
        """
        nonlocal i2c
        if i2c is None:
            _init_i2c()
        return i2c

    class DigitalInput(aw9523.Pin):
        _pin_map = {
            # input id: pin id
            1: 4,
            2: 5,
            3: 6,
            4: 7,
            5: 12,
            6: 13,
            7: 14,
            8: 15,
        }

        def __init__(self, id) -> None:
            nonlocal aw
            if aw is None:
                aw = _aw9523_init()
            pid = self._pin_map.get(id, None)
            if pid is None:
                raise ValueError("Invalid DigitalInput ID")
            super().__init__(pid)

        def get_status(self) -> bool:
            """Get the status of the digital input.

            :returns: The status of the digital input.
            :rtype: bool
            """
            return bool(self.value())

    class Relay(aw9523.Pin):
        _pin_map = {
            # relay id: pin id
            1: 0,
            2: 1,
            3: 2,
            4: 3,
        }

        def __init__(self, id) -> None:
            nonlocal aw
            if aw is None:
                aw = _aw9523_init()
            pid = self._pin_map.get(id, None)
            if pid is None:
                raise ValueError("Invalid Relay ID")
            super().__init__(pid, mode=aw9523.Pin.OUT)

        def get_status(self) -> bool:
            """Get the status of the relay.

            :returns: The status of the relay.
            :rtype: bool
            """
            return bool(self.value())

        def set_status(self, status: bool) -> None:
            """Set the status of the relay.

            :param status: The status to set.
            :type status: bool
            """
            self.value(int(status))

    return DigitalInput, Relay, get_i2c


DigitalInput, Relay, get_i2c = _plc_closure()
