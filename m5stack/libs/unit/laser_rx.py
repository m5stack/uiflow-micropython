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
    """
    note:
        en: LASER.RX is one of the communication devices among M5Units, a Laser receiver. It is mainly built with a laser transistor. Laser communications devices are wireless connections through the atmosphere. They work similarly to fiber-optic links, except the beam is transmitted through free space. While the transmitter and receiver must require line-of-sight conditions, they have the benefit of eliminating the need for broadcast rights and buried cables. Laser communications systems can be easily deployed since they are inexpensive, small, low power and do not require any radio interference studies. Two parallel beams are needed, one for transmission and one for reception. Therefore we have a LASER.TX in parallel.

    details:
        link: https://docs.m5stack.com/en/unit/laser-rx
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/laser-rx/laser-rx_01.webp
        category: Unit

    example:
        - ../../../examples/unit/laser/laserrx_core2_example.py

    m5f2:
        - unit/laser/laserrx_core2_example.m5f2
    """

    def __init__(self, port: tuple, mode: int = PIN_MODE, id: Literal[1, 2] = 1) -> None:
        """
        note:
            en: Initialize the LaserRXUnit with the specified port, communication mode, and UART ID.

        params:
            port:
                note: A tuple containing pin numbers for TX and RX.
            mode:
                note: Communication mode; use PIN_MODE or UART_MODE.
            id:
                note: UART ID, either 1 or 2.
        """
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
        """
        note:
            en: Initialize UART communication with specified parameters.

        params:
            baudrate:
                note: The baud rate for UART communication. Default is 115200.
            bits:
                note: The number of data bits; 7, 8, or 9. Default is 8.
            parity:
                note: Parity setting; None, 0, or 1. Default is 8.
            stop:
                note: The number of stop bits; 1 or 2. Default is 1.
        """
        if self._mode == UART_MODE:
            self.uart.init(baudrate=baudrate, bits=bits, parity=parity, stop=stop)

    def read(self, byte=None):
        """
        note:
            en: Read data from UART. Optionally specify the number of bytes to read.

        params:
            byte:
                note: The number of bytes to read. If None, reads all available data.

        returns:
            note: The data read from UART or None if no data is available.
        """
        if self._mode == UART_MODE:
            if byte is not None:
                return self.uart.read(byte)
            else:
                return self.uart.read()

    def readline(self):
        """
        note:
            en: Read a single line of data from UART.

        params:
            note:

        returns:
            note: The line read from UART or None if no data is available.
        """
        if self._mode == UART_MODE:
            return self.uart.readline()

    def any(self):
        """
        note:
            en: Check if there is any data available in UART buffer.

        params:
            note:

        returns:
            note: True if data is available; otherwise, False.
        """
        if self._mode == UART_MODE:
            return self.uart.any()

    def value(self) -> None:
        """
        note:
            en: Get the current value of the input pin when using PIN_MODE.

        params:
            note:

        returns:
            note: The value of the pin (0 or 1).
        """
        if self._mode == PIN_MODE:
            return self._pin.value()
