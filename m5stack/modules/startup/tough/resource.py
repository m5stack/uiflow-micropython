# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import M5


_RESOURCE_ROOT = "/system/toughc5" if M5.getBoard() == M5.BOARD.M5ToughC5 else "/system/tough"


def resource(path: str) -> str:
    return _RESOURCE_ROOT + path
