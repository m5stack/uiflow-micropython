import os, sys, io
import M5
from M5 import *
from hardware import PWM
from hardware import Pin
import time


pwm15 = None


duty = None
last_time = None
dir2 = None


def setup():
    global pwm15, duty, last_time, dir2

    M5.begin()
    pwm15 = PWM(Pin(15), freq=20000, duty=512)
    duty = 0
    dir2 = True
    last_time = time.ticks_ms()


def loop():
    global pwm15, duty, last_time, dir2
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 10:
        last_time = time.ticks_ms()
        duty = (duty if isinstance(duty, (int, float)) else 0) + 1
        if duty >= 1023:
            duty = 0
            dir2 = not dir2
        if dir2:
            pwm15.duty(duty)
            print((str("duty: ") + str(duty)))
        else:
            pwm15.duty((1023 - duty))
            print((str("duty: ") + str((1023 - duty))))


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
