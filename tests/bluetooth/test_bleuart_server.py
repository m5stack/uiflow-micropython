import os, sys, io
import M5
from M5 import *
from bleuart import *
import time


label0 = None
ble_periph = None


data = None


def setup():
  global label0, ble_periph, data

  M5.begin()
  Widgets.fillScreen(0x222222)
  label0 = Widgets.Label("Text", 20, 31, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)

  ble_periph = BLEUARTServer(name='ble-uart')


def loop():
  global label0, ble_periph, data
  M5.update()
  if (ble_periph.any()) > 0:
    data = ble_periph.read()
    label0.setText(str(data))
    ble_periph.write(data)
  else:
    time.sleep_ms(100)


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
