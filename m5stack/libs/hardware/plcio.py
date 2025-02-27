# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver import aw9523
import M5
import machine


def _plc_closure():
    aw = None

    def _aw9523_init():
        _board_map = {
            # boardid: (i2c, scl, sda, irq_pin)
            M5.BOARD.M5StampPLC: (1, 15, 13, 14),
        }
        i2c, scl, sda, irq_pin = _board_map.get(M5.getBoard(), (None, None, None, None))
        if i2c is None:
            raise NotImplementedError("AW9523 is not supported on this board")
        i2c = machine.I2C(i2c, scl=machine.Pin(scl), sda=machine.Pin(sda))
        return aw9523.AW9523(i2c, irq_pin=irq_pin)

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
            return bool(self.value())

    return DigitalInput, Relay


DigitalInput, Relay = _plc_closure()
