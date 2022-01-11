# -*- encoding: utf-8 -*-
# Fill random size and position to circle to screen
import m5
from m5 import lcd
import random

m5.begin()

while True:
    lcd.fillCircle(random.randint(20, 300), random.randint(20, 220),
                    random.randint(5, 30), random.randint(0, 0xffffff))
