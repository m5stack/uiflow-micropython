# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# apps/helloworld.py

import M5
from M5 import Lcd

M5.begin()

print("Hello world,M5STACK!")

Lcd.clear(0)
Lcd.setCursor(int(Lcd.width() / 2) - 60, int(Lcd.height() / 2) - 15)
Lcd.print("M5STACK")
