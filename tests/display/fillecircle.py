# -*- encoding: utf-8 -*-
# Fill random size and position to circle to screen
import m5
from m5 import lcd
import random


def setup():
    m5.begin()


def loop():
    lcd.fillCircle(
        random.randint(20, 300),
        random.randint(20, 220),
        random.randint(5, 30),
        random.randint(0, 0xFFFFFF),
    )


if __name__ == "__main__":
    setup()
    try:
        while True:
            loop()
    except Exception as e:
        pass
