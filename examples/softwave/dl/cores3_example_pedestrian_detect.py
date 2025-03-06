# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
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
    global img, detector, detection_result, kp
    M5.begin()
    Widgets.fillScreen(0x222222)
    camera.init(pixformat=camera.RGB565, framesize=camera.QVGA)
    detector = dl.ObjectDetector(dl.model.PEDESTRIAN_DETECT)


def loop():
    global img, detector, detection_result, kp
    M5.update()
    img = camera.snapshot()
    detection_result = detector.infer(img)
    if detection_result:
        for res in detection_result:
            kp = res.keypoint()
            img.draw_rectangle(
                res.x(), res.y(), res.w(), res.h(), color=0x3366FF, thickness=3, fill=False
            )
    M5.Lcd.show(img, 0, 0, 320, 240)


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
