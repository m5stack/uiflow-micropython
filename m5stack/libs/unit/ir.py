# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from driver.ir.nec import NEC, NEC_8
import machine


class IRUnit:
    # def __new__(cls, port, proto):
    #     if proto.upper() == "NEC":
    #         return NEC(Pin(port[1], Pin.IN))

    def __init__(self, port) -> None:
        (self._rx_pin, self._tx_pin) = port
        self._transmitter = NEC(machine.Pin(self._tx_pin, machine.Pin.OUT, value=0))
        self._receiver = None

    def tx(self, cmd, data):
        self._transmitter.transmit(cmd, data)

    def rx_cb(self, cb):
        if self._receiver:
            self._receiver.close()
        self._receiver = NEC_8(machine.Pin(self._rx_pin, machine.Pin.IN), cb)
