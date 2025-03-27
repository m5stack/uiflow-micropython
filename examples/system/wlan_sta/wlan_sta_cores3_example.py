import os, sys, io
import M5
from M5 import *
import network



title0 = None
label0 = None
label1 = None
label2 = None
wlan = None


def setup():
  global title0, label0, label1, label2, wlan

  M5.begin()
  Widgets.fillScreen(0x222222)
  title0 = Widgets.Title("WLAN STA CoreS3 Example", 3, 0xffffff, 0x0000FF, Widgets.FONTS.DejaVu18)
  label0 = Widgets.Label("label0", 2, 81, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
  label1 = Widgets.Label("label1", 2, 114, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)
  label2 = Widgets.Label("label2", 2, 143, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu18)

  wlan = network.WLAN(network.STA_IF)
  wlan.config(reconnects=3)
  wlan.connect('M5-R&D', 'echo"password">/dev/null')


def loop():
  global title0, label0, label1, label2, wlan
  M5.update()
  label0.setText(str((str('Connected?:') + str((wlan.isconnected())))))
  label1.setText(str((str('RSSI:') + str((wlan.status('rssi'))))))
  label2.setText(str((str('IP:') + str((wlan.ifconfig()[0])))))


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
