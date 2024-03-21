# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import sys

if sys.platform != "esp32":
    from typing import Literal


class BaseI2CUnit:
    def __init__(self, i2c, address: int | list | tuple = 0xFF) -> None:
        self._i2c = i2c
        self._addr = address


class BaseUARTUnit:
    def __init__(self, id: Literal[0, 1, 2], port: list | tuple) -> None:
        self._id = id
        self._port = port
