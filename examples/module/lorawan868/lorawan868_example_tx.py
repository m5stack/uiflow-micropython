import os, sys, io
import M5
from M5 import *
from module import LoRaWAN868Module
import time


lorawan868_0 = None


def setup():
    global lorawan868_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    lorawan868_0 = LoRaWAN868Module(1, (17, 16))
    lorawan868_0.wake_up()
    lorawan868_0.set_parameters(0, 0, 5, 0, 1, 8, 0, 0, 0)
    lorawan868_0.set_auto_low_power(False)
    print(lorawan868_0.query_chip_id())
    print(lorawan868_0.query_lorawan_mode())
    print(lorawan868_0.any())
    lorawan868_0.set_mode(LoRaWAN868Module.MODE_LORA)


def loop():
    global lorawan868_0
    M5.update()
    lorawan868_0.send_hex("Hello Lora!")
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
