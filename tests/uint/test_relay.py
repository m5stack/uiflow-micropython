import os, sys, io
import M5
from M5 import *
import time
from unit import *


relay_0 = None


def setup():
    global relay_0

    relay_0 = RelayUnit((1, 2))
    M5.begin()


def loop():
    global relay_0
    M5.update()
    relay_0.on()
    time.sleep(1)
    relay_0.off()
    time.sleep(1)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
