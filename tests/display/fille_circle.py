# -*- encoding: utf-8 -*-
# Fill random size and position to circle to screen
import M5
from M5 import Display
import random


def setup():
    M5.begin()


def loop():
    Display.fillCircle(
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
    except:
        # error handler
        # if use canvas, need manual delete it to free allocated memory for now
        pass
