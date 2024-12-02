# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from unit import DualButtonUnit
from hardware import *
import camera
import dl
import image


dual_button_0_blue = None
dual_button_0_red = None
sys_state = None
FACE_RECOGNIZE = None
FACE_ENROLL = None
FACE_DELETE = None
detector = None
img = None
dl_recognizer = None
detection_result = None
IDLE = None
res = None
kp = None
sys_state_prev = None
frame_count = None
dl_recognize_result = None


def dual_button_0_blue_wasClicked_event(state):
    global dual_button_0_blue, dual_button_0_red, sys_state, FACE_RECOGNIZE, FACE_ENROLL, FACE_DELETE, detector, img, dl_recognizer, detection_result, IDLE, kp, sys_state_prev, frame_count, res, dl_recognize_result
    sys_state = FACE_RECOGNIZE

def dual_button_0_red_wasClicked_event(state):
    global dual_button_0_blue, dual_button_0_red, sys_state, FACE_RECOGNIZE, FACE_ENROLL, FACE_DELETE, detector, img, dl_recognizer, detection_result, IDLE, kp, sys_state_prev, frame_count, res, dl_recognize_result
    sys_state = FACE_ENROLL

def btnPWR_wasClicked_event(state):
    global dual_button_0_blue, dual_button_0_red, sys_state, FACE_RECOGNIZE, FACE_ENROLL, FACE_DELETE, detector, img, dl_recognizer, detection_result, IDLE, kp, sys_state_prev, frame_count, res, dl_recognize_result
    sys_state = FACE_DELETE

def setup():
    global dual_button_0_blue, dual_button_0_red, sys_state, FACE_RECOGNIZE, FACE_ENROLL, FACE_DELETE, detector, img, dl_recognizer, detection_result, IDLE, kp, sys_state_prev, frame_count, res, dl_recognize_result
    M5.begin()
    Widgets.fillScreen(0x222222)
    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btnPWR_wasClicked_event)
    camera.init(pixformat=camera.RGB565, framesize=camera.QVGA)
    dual_button_0_blue, dual_button_0_red = DualButtonUnit((8, 9))
    dual_button_0_blue.setCallback(type=dual_button_0_blue.CB_TYPE.WAS_CLICKED, cb=dual_button_0_blue_wasClicked_event)
    dual_button_0_red.setCallback(type=dual_button_0_red.CB_TYPE.WAS_CLICKED, cb=dual_button_0_red_wasClicked_event)
    detector = dl.ObjectDetector(dl.model.HUMAN_FACE_DETECT)
    dl_recognizer = dl.HumanFaceRecognizer()
    IDLE = 0
    FACE_ENROLL = 1
    FACE_RECOGNIZE = 2
    FACE_DELETE = 3
    sys_state = IDLE
    sys_state_prev = IDLE
    frame_count = 0

def loop():
    global dual_button_0_blue, dual_button_0_red, sys_state, FACE_RECOGNIZE, FACE_ENROLL, FACE_DELETE, detector, img, dl_recognizer, detection_result, IDLE, kp, sys_state_prev, frame_count, res, dl_recognize_result
    M5.update()
    dual_button_0_blue.tick(None)
    dual_button_0_red.tick(None)
    img = camera.snapshot()
    detection_result = detector.infer(img)
    if detection_result:
        for res in detection_result:
            kp = res.keypoint()
            img.draw_string(10, 10, str('face'), color=0x3333ff, scale=1)
            img.draw_circle(kp[0], kp[1], 3, color=0x3333ff, thickness=1, fill=True)
            img.draw_circle(kp[2], kp[3], 3, color=0x33ff33, thickness=1, fill=True)
            img.draw_circle(kp[4], kp[5], 3, color=0xff0000, thickness=1, fill=True)
            img.draw_circle(kp[6], kp[7], 3, color=0x3333ff, thickness=1, fill=True)
            img.draw_circle(kp[8], kp[9], 3, color=0x33ff33, thickness=1, fill=True)
            img.draw_rectangle(res.x(), res.y(), res.w(), res.h(), color=0x3366ff, thickness=3, fill=False)
    if sys_state == FACE_DELETE:
        dl_recognizer.delete_id()
        sys_state_prev = sys_state
        sys_state = IDLE
        frame_count = 15
    elif sys_state != IDLE:
        if detection_result:
            if len(detection_result) == 1:
                res = detection_result[0]
                if sys_state == FACE_ENROLL:
                    dl_recognizer.enroll_id(img, res.keypoint())
                elif sys_state == FACE_RECOGNIZE:
                    dl_recognize_result = dl_recognizer.recognize(img, res.keypoint())
                    if (dl_recognize_result.id()) > 0:
                        print((str('similarity: ') + str((dl_recognize_result.similarity()))))
                sys_state_prev = sys_state
                sys_state = IDLE
                frame_count = 15
        else:
            img.draw_string(104, 10, str('face no detect'), color=0xff0000, scale=1)
    if frame_count > 0:
        frame_count = frame_count - 1
        if sys_state_prev == FACE_ENROLL:
            img.draw_string(116, 10, str('face enroll'), color=0x33ff33, scale=1)
        elif sys_state_prev == FACE_RECOGNIZE:
            if (dl_recognize_result.id()) > 0:
                img.draw_string(100, 10, str((str('recognize id: ') + str((dl_recognize_result.id())))), color=0x33ff33, scale=1)
            else:
                img.draw_string(96, 10, str('no recognized'), color=0xff0000, scale=1)
        elif sys_state_prev == FACE_DELETE:
            img.draw_string(100, 10, str((str('remaining id: ') + str((dl_recognizer.enrolled_id_num())))), color=0xff0000, scale=1)
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

