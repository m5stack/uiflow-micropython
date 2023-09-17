# -*- encoding: utf-8 -*-
# button callback test
import M5
import time
import random
from M5 import Lcd, BtnA, BtnB, BtnC


def btnA_wasPressed_cb(state):
    Lcd.clear(random.randint(0, 0xFFFF))
    Lcd.setCursor(0, 0)
    Lcd.print("btnA_wasPressed_cb")


def btnB_wasHold_cb(state):
    Lcd.clear(random.randint(0, 0xFFFF))
    Lcd.setCursor(0, 0)
    Lcd.print("btnB_wasHold_cb")


def btnC_wasDoubleClicked_cb(state):
    Lcd.clear(random.randint(0, 0xFFFF))
    Lcd.setCursor(0, 0)
    Lcd.print("btnC_wasDoubleClicked_cb")


M5.begin()

BtnA.setCallback(type=BtnA.CALLBACK_TYPE.WAS_PRESSED, callback=btnA_wasPressed_cb)
BtnB.setCallback(type=BtnA.CALLBACK_TYPE.WAS_HOLD, callback=btnB_wasHold_cb)
BtnC.setCallback(type=BtnA.CALLBACK_TYPE.WAS_DOUBLECLICKED, callback=btnC_wasDoubleClicked_cb)


while True:
    M5.update()  # button callback function need call this update   --.
    time.sleep_ms(30)
