import os, sys, io
import M5
from M5 import *
from bleuart import *
import time


ble_central = None


nums = None
i = None


def setup():
    global ble_central, nums, i

    M5.begin()
    ble_central = BLEUARTClient()
    ble_central.connect("ble-uart", timeout=2000)
    while not (ble_central.is_connected()):
        time.sleep_ms(100)
    print("Connected")
    nums = [4, 8, 15, 16, 23, 46]
    i = 1
    while True:
        ble_central.write((str((nums[int(i - 1)]))))
        i = (i + 1) % len(nums)
        time.sleep(1)
        print((str("rx:") + str(((ble_central.read()).decode()))))
    ble_central.close()
    ble_central.deinit()


def loop():
    global ble_central, nums, i
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
