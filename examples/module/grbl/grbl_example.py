import os, sys, io
import M5
from M5 import *
from module import GRBLModule


grbl_0 = None


def setup():
    global grbl_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    grbl_0 = GRBLModule(address=0x70)
    print(grbl_0.get_message())
    print(grbl_0.get_status())
    print(grbl_0.get_idle_state())
    print(grbl_0.get_lock_state())
    grbl_0.set_mode(GRBLModule.MODE_ABSOLUTE)
    grbl_0.unlock()
    grbl_0.turn(5, 5, 10, 5)
    grbl_0.wait_idle()
    grbl_0.lock()


def loop():
    global grbl_0
    M5.update()


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
