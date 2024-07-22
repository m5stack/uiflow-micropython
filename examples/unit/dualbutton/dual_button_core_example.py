import os, sys, io
import M5
from M5 import *
from unit import DualButtonUnit


dual_button_0_blue = None
dual_button_0_red = None


def dual_button_0_blue_wasClicked_event(state):  # noqa: N802
    global dual_button_0_blue, dual_button_0_red
    print(dual_button_0_blue.isHolding())


def setup():
    global dual_button_0_blue, dual_button_0_red

    M5.begin()
    Widgets.fillScreen(0x222222)

    dual_button_0_blue, dual_button_0_red = DualButtonUnit((36, 26))
    dual_button_0_blue.setCallback(
        type=dual_button_0_blue.CB_TYPE.WAS_CLICKED, cb=dual_button_0_blue_wasClicked_event
    )
    print(dual_button_0_blue.isHolding())


def loop():
    global dual_button_0_blue, dual_button_0_red
    M5.update()
    dual_button_0_blue.tick(None)


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
