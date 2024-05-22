# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from machine import Pin


class Relay2Unit:
    def __init__(self, port: tuple) -> None:
        self._relay1 = Pin(port[0])
        self._relay2 = Pin(port[1])
        self._relay1.init(mode=Pin.OUT)
        self._relay2.init(mode=Pin.OUT)

    def set_relay_cntrl(self, num: int = 1, control: int = 0) -> None:
        self._relay1(control) if num == 1 else self._relay2(control)

    def get_relay_status(self, num: int = 1) -> bool:
        return bool(self._relay1() if num == 1 else self._relay2())
