import os, sys, io
import M5
from M5 import *
from hardware import ADC
from hardware import Pin
import time


adc23 = None


last_time = None


def setup():
    global adc23, last_time

    M5.begin()
    adc23 = ADC(Pin(23), atten=ADC.ATTN_11DB)
    last_time = time.ticks_ms()


def loop():
    global adc23, last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 200:
        last_time = time.ticks_ms()
        print((str("ADC(pin23): ") + str((adc23.read_u16()))))


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
