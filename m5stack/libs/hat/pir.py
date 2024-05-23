# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

from unit.pir import PIRUnit


class PIRHat(PIRUnit):
    def __init__(self, port: tuple = (36, 0)) -> None:
        super().__init__(port)
