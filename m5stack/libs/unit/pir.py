# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from micropython import const
from micropython import schedule
from machine import Pin
import sys

if sys.platform != "esp32":
    from typing import Literal


class PIRUnit:
    IRQ_NEGATIVE = const(0)
    IRQ_ACTIVE = const(1)

    def __init__(self, port: tuple) -> None:
        self._pin = Pin(port[0])
        self._pin.init(mode=self._pin.IN)
        self._pin.irq(self._callback, trigger=self._pin.IRQ_FALLING | self._pin.IRQ_RISING)
        self._handlers = [None, None]

    def get_status(self) -> bool:
        return bool(self._pin())

    def set_callback(self, handler: function, trigger: Literal[0, 1]) -> None:
        self._handlers[trigger] = handler

    def disable_irq(self) -> None:
        self._pin.irq(None)

    def enable_irq(self) -> None:
        self._pin.irq(self._callback, trigger=self._pin.IRQ_FALLING | self._pin.IRQ_RISING)

    def _callback(self, pin) -> None:
        trigger = pin()
        if self._handlers[trigger] is not None:
            schedule(self._handlers[trigger], self)
