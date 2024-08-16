# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.ir.nec import NEC, NEC_8
import M5
from machine import Pin


class IR:
    _pin_map = {
        M5.BOARD.M5AtomS3: (None, 4),
        M5.BOARD.M5AtomS3Lite: (None, 4),
        M5.BOARD.M5AtomS3U: (None, 12),
        M5.BOARD.M5Capsule: (None, 4),
        M5.BOARD.M5Cardputer: (None, 44),
        M5.BOARD.M5StickCPlus: (None, 9),
        M5.BOARD.M5StickC: (None, 9),
        M5.BOARD.M5StickCPlus2: (None, 19),
        M5.BOARD.M5AtomU: (None, 12),
        M5.BOARD.M5Atom: (None, 12),
        M5.BOARD.M5AtomEcho: (None, 12),
    }

    def __init__(self) -> None:
        self._port = self._pin_map.get(M5.getBoard())
        self._transmitter = NEC(Pin(self._port[1], Pin.OUT, value=0))
        self._receiver = None

    def tx(self, cmd, data):
        self._transmitter.transmit(cmd, data)

    def rx_cb(self, cb):
        if self._port[0] is None:
            return

        if self._receiver is None:
            self._receiver = NEC_8(Pin(self._port[0], Pin.IN), cb)
        else:
            self._receiver.close()
