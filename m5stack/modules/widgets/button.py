# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from . import base


class Button(base.Base):
    def __init__(self, parent) -> None:
        super().__init__(parent)
