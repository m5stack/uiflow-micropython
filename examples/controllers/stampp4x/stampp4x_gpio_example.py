import os, sys, io
import M5
from M5 import *
from hardware import Pin
import time


pin15 = None


last_time = None
enable = None


def setup():
    global pin15, last_time, enable

    M5.begin()
    pin15 = Pin(15, mode=Pin.OUT)
    last_time = time.ticks_ms()


def loop():
    global pin15, last_time, enable
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
        last_time = time.ticks_ms()
        enable = not enable
        if enable:
            print("set pin15 high")
            pin15.on()
        else:
            print("set pin15 low")
            pin15.off()


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
