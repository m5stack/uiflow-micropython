# -*- encoding: utf-8 -*-
# Touch test
import M5
from M5 import Display
import time


def setup():
    M5.begin()


def loop():
    M5.update()
    if M5.Touch.getCount():
        Display.drawCircle(M5.Touch.getX(), M5.Touch.getY(), 5, M5.Display.COLOR.BLUE)
    time.sleep(0.01)


if __name__ == "__main__":
    setup()
    try:
        while True:
            loop()
    except:
        # error handler
        # if use canvas, need manual delete it to free allocated memory for now
        pass
