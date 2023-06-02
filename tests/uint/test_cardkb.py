import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import *


i2c0 = None
cardkb_0 = None


def cardkb_0_pressed_event(kb):
  global i2c0, cardkb_0
  print(cardkb_0.get_string())


def setup():
  global i2c0, cardkb_0

  i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
  cardkb_0 = CardKB(i2c0)
  cardkb_0.set_callback(cardkb_0_pressed_event)
  M5.begin()


def loop():
  global i2c0, cardkb_0
  M5.update()
  cardkb_0.tick()


if __name__ == '__main__':
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
