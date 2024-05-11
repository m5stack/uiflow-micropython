# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import Pin, ADC
from micropython import const
from micropython import schedule

import sys

if sys.platform != "esp32":
    from typing import Literal


class ReflectiveIRUnit:
    EVENT_DETECTED = const(0)
    EVENT_NOT_DETECTED = const(1)

    def __init__(self, port: tuple) -> None:
        self._ain = ADC(Pin(port[0]), atten=ADC.ATTN_11DB)
        self._din = Pin(port[1], mode=Pin.IN)
        self._handlers = [None, None]

    def get_digital_value(self):
        return self._din()

    def get_analog_value(self):
        return self._ain.read_u16()

    def set_callback(self, handler, trigger: Literal[0, 1]) -> None:
        self._handlers[trigger] = handler

    def disable_irq(self) -> None:
        self._din.irq(None)

    def enable_irq(self) -> None:
        self._din.irq(self._callback, trigger=self._din.IRQ_FALLING | self._din.IRQ_RISING)

    def _callback(self, pin) -> None:
        trigger = pin()
        if self._handlers[trigger] is not None:
            schedule(self._handlers[trigger], self)
