# -*- encoding: utf-8 -*-
# UNIT PAHUBUnit + ENVUnit
import M5
import time
from M5 import Widgets
from machine import Pin, I2C
from unit import ENVUnit, PAHUBUnit

label0 = None
label1 = None
label2 = None

i2c0 = None
pahub0_0 = None
pahub0_1 = None
env2_0 = None
env2_1 = None

"""
ATOMS3 PortA: [1(scl), 2(sda), V, G]
"""


def setup():
    global label0, label1, label2, label3, label4, label5, env2_0, env2_1
    M5.begin()
    label0 = Widgets.Label("Text", 9, 0, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Text", 9, 20, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Text", 9, 40, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Text", 9, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Text", 9, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("Text", 9, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    # I2C Bus
    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    # PAHUB Bus, up to 6 channel to use
    pahub0_0 = PAHUBUnit(i2c=i2c0, channel=0)
    pahub0_1 = PAHUBUnit(i2c=i2c0, channel=1)
    # ENVUnit connect to PAHUB port
    env2_0 = ENVUnit(i2c=pahub0_0, type=2)
    env2_1 = ENVUnit(i2c=pahub0_1, type=2)


def loop():
    global label0, label1, label2, label3, label4, label5, env2_0, env2_1
    label0.setText("T:" + str(env2_0.read_temperature()))
    label1.setText("H:" + str(env2_0.read_humidity()))
    label2.setText("P:" + str(env2_0.read_pressure()))

    label3.setText("T:" + str(env2_1.read_temperature()))
    label4.setText("H:" + str(env2_1.read_humidity()))
    label5.setText("P:" + str(env2_1.read_pressure()))
    time.sleep(1)


if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except Exception as ex:
        # error handler
        raise ex
