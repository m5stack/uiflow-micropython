# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT


from unit.mqtt import MQTTUnit
import sys

if sys.platform != "esp32":
    from typing import Literal


class MQTTPoEUnit(MQTTUnit):
    def __init__(self, id: Literal[0, 1, 2] = 1, port: list | tuple = None) -> None:
        super().__init__(id, port)
