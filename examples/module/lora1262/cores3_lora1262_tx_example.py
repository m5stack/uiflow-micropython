import os, sys, io
import M5
from M5 import *
from module import LoRa1262Module
import time


title0 = None
label_t = None
label_tx = None
label_ts = None
label_time = None
lora1262_0 = None


count = None
message = None


def setup():
    global title0, label_t, label_tx, label_ts, label_time, lora1262_0, count, message

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("LoRa1262 Module Tx", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18)
    label_t = Widgets.Label("Send:", 5, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)
    label_tx = Widgets.Label("hello", 65, 50, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)
    label_ts = Widgets.Label(
        "timestamp:", 5, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18
    )
    label_time = Widgets.Label("1", 118, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)

    count = 0
    lora1262_0 = LoRa1262Module(pin_cs=0, pin_busy=2, pin_irq=14, address=0x74)


def loop():
    global title0, label_t, label_tx, label_ts, label_time, lora1262_0, count, message
    M5.update()
    message = str("Module LoRa1262 ") + str(count)
    lora1262_0.send(message, None)
    label_tx.setText(str(message))
    label_time.setText(str(time.ticks_ms()))
    count = count + 1
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
