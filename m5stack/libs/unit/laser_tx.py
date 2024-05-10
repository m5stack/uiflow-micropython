# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import Pin, UART
import sys

if sys.platform != "esp32":
    from typing import Literal

PIN_MODE = 1
UART_MODE = 2


class LaserTxUnit:
    def __init__(self, port: tuple, mode: int = PIN_MODE, id: Literal[1, 2] = 1) -> None:
        self._mode = mode
        if self._mode == PIN_MODE:
            self._pin = Pin(port[1], Pin.OUT)
        elif self._mode == UART_MODE:
            self.uart = UART(id, tx=port[1], rx=port[0])

    def init_uart(
        self,
        baudrate: int = 115200,
        bits: Literal[7, 8, 9] = 8,
        parity: Literal[None, 0, 1] = 8,
        stop: Literal[1, 2] = 1,
    ):
        if self._mode == UART_MODE:
            self.uart.init(baudrate=baudrate, bits=bits, parity=parity, stop=stop)

    def write(self, payload):
        if self._mode == UART_MODE:
            self.uart.write(payload)

    def on(self) -> None:
        if self._mode == PIN_MODE:
            self._pin.value(1)

    def off(self) -> None:
        if self._mode == PIN_MODE:
            self._pin.value(0)

    def value(self, x: bool) -> None:
        if self._mode == PIN_MODE:
            self._pin.value(int(x))
