# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from hardware import Button


def DualButtonUnit(port):  # noqa: N802
    return Button(port[0]), Button(port[1])
