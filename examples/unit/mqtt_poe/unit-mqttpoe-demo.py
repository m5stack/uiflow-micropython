import os, sys, io
import M5
from M5 import *
from unit import MQTTPoEUnit
import time


mqttpoe_0 = None


def mqttpoe_0_SubTopic_event(data):  # noqa: N802
    global mqttpoe_0
    print(data[0])
    print(data[1])


def setup():
    global mqttpoe_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    mqttpoe_0 = MQTTPoEUnit(port=(18, 17))
    mqttpoe_0.set_client("m5-mqtt-xxx", "mqtt.m5stack.com", 1883, "", "", 120)
    mqttpoe_0.set_subscribe("SubTopic", mqttpoe_0_SubTopic_event, 0)
    mqttpoe_0.set_connect()


def loop():
    global mqttpoe_0
    M5.update()
    mqttpoe_0.check_msg()
    time.sleep_ms(50)


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
