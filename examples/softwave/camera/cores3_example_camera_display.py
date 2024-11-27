    import os, sys, io
    import M5
    from M5 import *
    import camera


    img = None

    def setup():
      global img
      M5.begin()
      Widgets.fillScreen(0x222222)
      camera.init(pixformat=camera.RGB565, framesize=camera.QVGA)

    def loop():
      global img
      M5.update()
      img = camera.snapshot()
      M5.Lcd.show(img, 0, 0, 320, 240)

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