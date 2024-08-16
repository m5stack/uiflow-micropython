import os, sys, io
import M5
from M5 import *
from m5espnow import *
import time
import random

espnow_0 = None
espnow_mac = None
espnow_data = None


def espnow_recv_callback(espnow_obj):
    global espnow_0, espnow_mac, espnow_data
    espnow_mac, espnow_data = espnow_obj.recv_data()
    print(espnow_mac)
    print(espnow_data)


def setup():
    global espnow_0, espnow_mac, espnow_data

    M5.begin()
    Widgets.fillScreen(0x222222)

    espnow_0 = M5ESPNow(0)
    espnow_0.set_irq_callback(espnow_recv_callback)
    espnow_0.set_add_peer("84cca8601ebc", 1, 0, False)


def loop():
    global espnow_0, espnow_mac, espnow_data
    M5.update()
    espnow_0.send_data(1, random.randint(1000000, 9999999))
    time.sleep(2)


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
