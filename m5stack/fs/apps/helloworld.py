# apps/helloworld.py

import m5
from m5 import lcd

m5.begin()

print("Hello world,M5STACK!")

lcd.clear(0)
lcd.setCursor(int(lcd.width() / 2) - 60, int(lcd.height() / 2) - 15)
lcd.print("M5STACK")
