import os, sys, io
import M5
from M5 import *
import time
from unit import *


label0 = None
label1 = None
lorae220_0 = None


lorae220_rssi = None
lorae220_data = None


def lorae220_0_receive_event(received_data, rssi):
    global label0, label1, lorae220_0, lorae220_rssi, lorae220_data
    lorae220_data = received_data
    lorae220_rssi = rssi
    label0.setText(str(lorae220_data.decode()))


def setup():
    global label0, label1, lorae220_0, lorae220_rssi, lorae220_data

    lorae220_0 = LoRaE220JPUnit((33, 32))
    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 37, 43, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 37, 130, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    lorae220_0.setup(0x0000, 0, 0x2333)
    lorae220_0.receiveNoneBlock(lorae220_0_receive_event)


def loop():
    global label0, label1, lorae220_0, lorae220_rssi, lorae220_data
    M5.update()
    lorae220_0.send(0x0000, 0, "Hello???555")
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
