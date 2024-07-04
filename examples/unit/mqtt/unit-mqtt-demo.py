import os, sys, io
import M5
from M5 import *
from unit import MQTTUnit
import time


mqtt_0 = None


def mqtt_0_SubTopic_event(data):  # noqa: N802
    global mqtt_0
    print(data[0])
    print(data[1])


def setup():
    global mqtt_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    mqtt_0 = MQTTUnit(port=(18, 17))
    mqtt_0.set_client("m5-mqtt-xxx", "mqtt.m5stack.com", 1883, "", "", 120)
    mqtt_0.set_subscribe("SubTopic", mqtt_0_SubTopic_event, 0)
    mqtt_0.set_connect()


def loop():
    global mqtt_0
    M5.update()
    mqtt_0.check_msg()
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
