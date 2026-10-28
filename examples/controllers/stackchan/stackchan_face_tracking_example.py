import os, sys, io
import M5
from M5 import *
import camera
import dl
import image
from hardware.stackchan import StackChan


stackchan = None


import math

img = None
dl_detection_result = None
dl_detector = None
lost_frame = None
res = None
bbox = None
f_x = None
f_y = None
neutral = None
SMOOTH = None
f_w = None
DEADZONE_NORM = None
f_h = None
Y_NEUTRAL = None
f_cx = None
img_cx = None
f_cy = None
img_cy = None
ex = None
angle_x = None
ey = None
angle_y = None
x_target = None
y_target = None


def setup():
    global \
        stackchan, \
        img, \
        dl_detection_result, \
        dl_detector, \
        lost_frame, \
        res, \
        bbox, \
        f_x, \
        f_y, \
        neutral, \
        SMOOTH, \
        f_w, \
        DEADZONE_NORM, \
        f_h, \
        Y_NEUTRAL, \
        f_cx, \
        img_cx, \
        f_cy, \
        img_cy, \
        ex, \
        angle_x, \
        ey, \
        angle_y, \
        x_target, \
        y_target

    M5.begin()
    Widgets.setRotation(0)
    Widgets.fillScreen(0x222222)

    stackchan = StackChan(i2c=1, uart=1)
    camera.init(pixformat=camera.RGB565, framesize=camera.QVGA)
    dl_detector = dl.ObjectDetector(dl.model.HUMAN_FACE_DETECT)
    stackchan.set_servo_power(enable=True)
    stackchan.set_servo_torque(stackchan.SERVO_ID_X, enable=True)
    stackchan.set_servo_torque(stackchan.SERVO_ID_Y, enable=True)
    stackchan.set_servo_angle(stackchan.SERVO_ID_X, 0, 0, 0)
    stackchan.set_servo_angle(stackchan.SERVO_ID_Y, 45, 0, 0)
    SMOOTH = 0.1
    DEADZONE_NORM = 0.06
    Y_NEUTRAL = 45
    img_cx = 160
    img_cy = 120
    angle_x = 0
    angle_y = Y_NEUTRAL
    neutral = True


def loop():
    global \
        stackchan, \
        img, \
        dl_detection_result, \
        dl_detector, \
        lost_frame, \
        res, \
        bbox, \
        f_x, \
        f_y, \
        neutral, \
        SMOOTH, \
        f_w, \
        DEADZONE_NORM, \
        f_h, \
        Y_NEUTRAL, \
        f_cx, \
        img_cx, \
        f_cy, \
        img_cy, \
        ex, \
        angle_x, \
        ey, \
        angle_y, \
        x_target, \
        y_target
    M5.update()
    img = camera.snapshot()
    dl_detection_result = dl_detector.infer(img)
    if dl_detection_result:
        lost_frame = 0
        res = dl_detection_result[0]
        bbox = res.bbox()
        f_x = res.x()
        f_y = res.y()
        f_w = res.w()
        f_h = res.h()
        f_cx = int(f_x + f_w * 0.5)
        f_cy = int(f_y + f_h * 0.5)
        ex = (f_cx - img_cx) / img_cx
        ey = (f_cy - img_cy) / img_cy
        if math.fabs(ex) < DEADZONE_NORM:
            ex = 0
        if math.fabs(ey) < DEADZONE_NORM:
            ey = 0
        x_target = min(max(ex * -135, -135), 135)
        y_target = min(max(Y_NEUTRAL - Y_NEUTRAL * ey, 0), 90)
        angle_x = angle_x + SMOOTH * (x_target - angle_x)
        angle_y = angle_y + SMOOTH * (y_target - angle_y)
        stackchan.set_servo_angle(stackchan.SERVO_ID_X, angle_x, 100, 0)
        stackchan.set_servo_angle(stackchan.SERVO_ID_Y, angle_y, 100, 0)
        neutral = False
        lost_frame = 0
        img.draw_rectangle(f_x, f_y, f_w, f_h, color=0x6600CC, thickness=3, fill=False)
    else:
        lost_frame = (lost_frame if isinstance(lost_frame, (int, float)) else 0) + 1
        if lost_frame > 20 and not neutral:
            stackchan.set_servo_angle(stackchan.SERVO_ID_X, 0, 1000, 0)
            stackchan.set_servo_angle(stackchan.SERVO_ID_Y, 45, 1000, 0)
            neutral = True
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
