# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from driver.modbus.master.uSerial import uSerial
from machine import Pin


class RS485Unit(uSerial):
    def __init__(self, id=1, port=None, debug=False) -> None:
        self._id = id
        self._port = port
        self._debug = debug
        super().__init__(self._id, self._port[1], self._port[0], debug=self._debug)

    def init(
        self,
        tx_pin=17,
        rx_pin=18,
        baudrate=9600,
        data_bits=8,
        stop_bits=1,
        parity=None,
        ctrl_pin=None,
    ) -> None:
        if tx_pin is not None and rx_pin is not None:
            self._port = (rx_pin, tx_pin)
        if data_bits is None and stop_bits is None:
            data_bits = 8
            stop_bits = 1
        self._mdbus_uart.init(
            baudrate=baudrate,
            bits=data_bits,
            parity=parity,
            stop=stop_bits,
            tx=self._port[1],
            rx=self._port[0],
        )
        if ctrl_pin is not None:
            self._ctrlPin = Pin(ctrl_pin, mode=Pin.OUT)

    def write(self, payload) -> None:
        self._mdbus_uart.write(payload)

    def read(self, byte=None) -> bytes | None:
        if byte is not None:
            return self._mdbus_uart.read(byte)
        else:
            return self._mdbus_uart.read()

    def readline(self) -> bytes | None:
        return self._mdbus_uart.readline()

    def any(self) -> int:
        return self._mdbus_uart.any()
