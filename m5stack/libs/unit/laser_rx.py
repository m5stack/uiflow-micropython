# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import Pin, UART
import sys

if sys.platform != "esp32":
    from typing import Literal

PIN_MODE = 1
UART_MODE = 2


class LaserRXUnit:
    def __init__(self, port: tuple, mode: int = PIN_MODE, id: Literal[1, 2] = 1) -> None:
        self._mode = mode
        if self._mode == PIN_MODE:
            self._pin = Pin(port[0], Pin.IN, Pin.PULL_UP)
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

    def read(self, byte=None):
        if self._mode == UART_MODE:
            if byte is not None:
                return self.uart.read(byte)
            else:
                return self.uart.read()

    def readline(self):
        if self._mode == UART_MODE:
            return self.uart.readline()

    def any(self):
        if self._mode == UART_MODE:
            return self.uart.any()

    def value(self) -> None:
        if self._mode == PIN_MODE:
            return self._pin.value()
