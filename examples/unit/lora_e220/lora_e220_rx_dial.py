import os, sys, io
import M5
from M5 import *
from unit import LoRaE220JPUnit


lorae220_0 = None


lorae220_str_data = None
lorae220_rssi = None


def lorae220_0_receive_event(received_data, rssi):
    global lorae220_0, lorae220_str_data, lorae220_rssi
    lorae220_rssi = rssi
    try:
        lorae220_str_data = received_data.decode()
    except:
        lorae220_str_data = str(received_data)
    print(lorae220_str_data)


def setup():
    global lorae220_0, lorae220_str_data, lorae220_rssi

    lorae220_0 = LoRaE220JPUnit((15, 13))
    M5.begin()
    lorae220_0.receiveNoneBlock(lorae220_0_receive_event)


def loop():
    global lorae220_0, lorae220_str_data, lorae220_rssi
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
