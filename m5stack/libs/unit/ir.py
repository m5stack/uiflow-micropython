# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from driver.ir.nec import NEC as NEC_TX, NEC_8 as NEC_8_RX, NEC_16 as NEC_16_RX, SAMSUNG as SAMSUNG_RX
from driver.ir.sony_tx import SONY_ABC as SONY_TX
from driver.ir.sony_rx import SONY_12 AS SONY_12_RX, SONY_15 as SONY_15_RX, SONY_20 as SONY_20_RX
from driver.ir.receiver import IR_RX
import machine


class NEC_8:
    tx = NEC_TX
    rx = NEC_8_RX


class NEC_16:
    tx = NEC_TX
    rx = NEC_8_TX


class SAMSUNG:
    tx = NEC_TX
    rx = SAMSUNG_RX


class SONY_12:
    tx = SONY_TX
    rx = SONY_12_RX


class SONY_15:
    tx = SONY_TX
    rx = SONY_15_RX


class SONY_20:
    tx = SONY_TX
    rx = SONY_20_RX


class IRUnit:
    def __init__(self, port, ir_cls=NEC_8, timer=1) -> None:
        (self._rx_pin, self._tx_pin) = port
        self._ir_cls = ir_cls
        self._timer = timer
        self._transmitter = self._ir_cls.tx(machine.Pin(self._tx_pin, machine.Pin.OUT, value=0))
        self._receiver = None

    def tx(self, cmd, data):
        self._transmitter.transmit(cmd, data)

    def rx_cb(self, cb):
        if self._receiver:
            self._receiver.close()
        IR_RX.Timer_id = self._timer
        self._receiver = self._ir_cls_rx(machine.Pin(self._rx_pin, machine.Pin.IN), cb)
