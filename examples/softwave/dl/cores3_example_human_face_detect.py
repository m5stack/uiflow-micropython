import os, sys, io
import M5
from M5 import *
import camera
import dl
import image


img = None
detector = None
detection_result = None
res = None
kp = None

def setup():
  img, detector, detection_result, kp
  M5.begin()
  Widgets.fillScreen(0x222222)
  camera.init(pixformat=camera.RGB565, framesize=camera.QVGA)
  detector = dl.ObjectDetector(dl.model.HUMAN_FACE_DETECT)

def loop():
  img, detector, detection_result, kp
  M5.update()
  img = camera.snapshot()
  detection_result = detector.infer(img)
  if detection_result:
    for res in detection_result:
      kp = res.keypoint()
      img.draw_circle(kp[0], kp[1], 3, color=0x0000ff, thickness=1, fill=True)
      img.draw_circle(kp[2], kp[3], 3, color=0x00ff00, thickness=1, fill=True)
      img.draw_circle(kp[4], kp[5], 3, color=0xff0000, thickness=1, fill=True)
      img.draw_circle(kp[6], kp[7], 3, color=0x0000ff, thickness=1, fill=True)
      img.draw_circle(kp[8], kp[9], 3, color=0x00ff00, thickness=1, fill=True)
      img.draw_rectangle(res.x(), res.y(), res.w(), res.h(), color=0x3366ff, thickness=3, fill=False)
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
