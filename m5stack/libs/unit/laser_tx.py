# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import Pin, UART
import sys

if sys.platform != "esp32":
    from typing import Literal

PIN_MODE = 1
UART_MODE = 2


class LaserTXUnit:
    """
    note:
        en: LASER.TX is one of the communication devices among the M5Units family - a Laser emitter with adjustable focal length.It is mainly built with a laser diode Laser communications devices are wireless connections through the atmosphere. They work similarly to fiber-optic links, except the beam is transmitted through free space. While the transmitter and receiver must require line-of-sight conditions, they have the benefit of eliminating the need for broadcast rights and buried cables.

    details:
        link: https://docs.m5stack.com/en/unit/laser-tx
        image: https://static-cdn.m5stack.com/resource/docs/products/unit/laser-tx/laser-tx_01.webp
        category: Unit

    example:
        - ../../../examples/unit/laser/lasertx_cores3_example.py

    m5f2:
        - unit/laser/lasertx_cores3_example.m5f2
    """

    def __init__(self, port: tuple, mode: int = PIN_MODE, id: Literal[1, 2] = 1) -> None:
        """
        note:
            en: Initialize the LaserTXUnit with the specified port, communication mode, and UART ID.

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

    def write(self, payload):
        """
        note:
            en: Transmit data through UART.

        params:
            payload:
                note: The data to be transmitted via UART.
        """
        if self._mode == UART_MODE:
            self.uart.write(payload)

    def on(self) -> None:
        """
        note:
            en: Turn on the laser when using PIN_MODE.

        params:
            note:
        """
        if self._mode == PIN_MODE:
            self._pin.value(1)

    def off(self) -> None:
        """
        note:
            en: Turn off the laser when using PIN_MODE.

        params:
            note:
        """
        if self._mode == PIN_MODE:
            self._pin.value(0)

    def value(self, x: bool) -> None:
        """
        note:
            en: Set the laser state to either on or off using PIN_MODE.

        params:
            x:
                note: A boolean value; True turns the laser on, False turns it off.
        """
        if self._mode == PIN_MODE:
            self._pin.value(int(x))
