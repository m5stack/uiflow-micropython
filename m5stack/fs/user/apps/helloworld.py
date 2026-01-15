# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

# apps/helloworld.py

import M5
from M5 import Lcd

M5.begin()

print("Hello M5Stack!")

text = "M5Stack"
Lcd.clear(0)
Lcd.setFont(M5.Lcd.FONTS.DejaVu18)
Lcd.setTextColor(0x169FDD, 0x000000)
# Calculate center position
text_width = Lcd.textWidth(text, M5.Lcd.FONTS.DejaVu18)
text_height = Lcd.fontHeight(M5.Lcd.FONTS.DejaVu18)
x = (Lcd.width() - text_width) // 2
y = (Lcd.height() - text_height) // 2
Lcd.setCursor(x, y)
Lcd.print(text)
