# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
from .base import Base


class Button(Base):
    def __init__(self, parent) -> None:
        super().__init__(parent)
