# dl --- deep learning

<!-- .. include:: ../refs/advanced.dl.ref -->

<!-- .. note:: This module is only applicable to the CoreS3 Controller -->

<!-- .. module:: dl -->
   :synopsis: deep learning

## UiFlow2 Example

###### human face detect

Open the |cores3_example_human_face_detect.m5f2| project in UiFlow2.

This example uses a face detection algorithm to detect faces in real time from
the camera feed. When a face is detected, a bounding box is drawn on the screen
to mark the face's position, providing an intuitive visualization of the
detection results.

UiFlow2 Code Block:

Example output:

    None

###### pedestrain detect

Open the |cores3_example_pedestrian_detect.m5f2| project in UiFlow2.

This example uses a pedestrian detection algorithm to detect pedestrian targets
in real time from the camera feed. When a pedestrian is detected, a bounding box
is drawn on the screen to highlight the pedestrian's position, providing an
intuitive demonstration of the detection results.

UiFlow2 Code Block:

Example output:

    None

###### human face recognition

Open the |cores3_example_human_face_recognition.m5f2| project in UiFlow2.

To run this example, you will need the `CoreS3 <https://docs.m5stack.com/en/core/CoreS3>`_
and the `Unit Dual Button <https://docs.m5stack.com/en/unit/dual_button>`_.

This example uses a face recognition algorithm to detect faces in real time from
the camera feed.

By pressing different buttons, you can either enroll new face data or perform
face recognition. The detected faces and recognition results are displayed on
the screen with bounding boxes.

UiFlow2 Code Block:

Example output:

    None

## Micropython Example

###### human face detect

MicroPython Code Block:

```python
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
    detector = dl.ObjectDetector(dl.model.HUMAN_FACE_DETECT)

def loop():
    global img, detector, detection_result, kp
    M5.update()
    img = camera.snapshot()
    detection_result = detector.infer(img)
    if detection_result:
        for res in detection_result:
            kp = res.keypoint()
            img.draw_circle(kp[0], kp[1], 3, color=0x0000FF, thickness=1, fill=True)
            img.draw_circle(kp[2], kp[3], 3, color=0x00FF00, thickness=1, fill=True)
            img.draw_circle(kp[4], kp[5], 3, color=0xFF0000, thickness=1, fill=True)
            img.draw_circle(kp[6], kp[7], 3, color=0x0000FF, thickness=1, fill=True)
            img.draw_circle(kp[8], kp[9], 3, color=0x00FF00, thickness=1, fill=True)
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

```

Example output:

    None

###### pedestrain detect

MicroPython Code Block:

```python
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

```

Example output:

    None

###### human face recognition

MicroPython Code Block:

```python
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

def dual_button_0_blue_wasClicked_event(state):  # noqa: N802
    global \
        dual_button_0_blue, \
        dual_button_0_red, \
        sys_state, \
        FACE_RECOGNIZE, \
        FACE_ENROLL, \
        FACE_DELETE, \
        detector, \
        img, \
        dl_recognizer, \
        detection_result, \
        IDLE, \
        kp, \
        sys_state_prev, \
        frame_count, \
        res, \
        dl_recognize_result
    sys_state = FACE_RECOGNIZE

def dual_button_0_red_wasClicked_event(state):  # noqa: N802
    global \
        dual_button_0_blue, \
        dual_button_0_red, \
        sys_state, \
        FACE_RECOGNIZE, \
        FACE_ENROLL, \
        FACE_DELETE, \
        detector, \
        img, \
        dl_recognizer, \
        detection_result, \
        IDLE, \
        kp, \
        sys_state_prev, \
        frame_count, \
        res, \
        dl_recognize_result
    sys_state = FACE_ENROLL

def btnPWR_wasClicked_event(state):  # noqa: N802
    global \
        dual_button_0_blue, \
        dual_button_0_red, \
        sys_state, \
        FACE_RECOGNIZE, \
        FACE_ENROLL, \
        FACE_DELETE, \
        detector, \
        img, \
        dl_recognizer, \
        detection_result, \
        IDLE, \
        kp, \
        sys_state_prev, \
        frame_count, \
        res, \
        dl_recognize_result
    sys_state = FACE_DELETE

def setup():
    global \
        dual_button_0_blue, \
        dual_button_0_red, \
        sys_state, \
        FACE_RECOGNIZE, \
        FACE_ENROLL, \
        FACE_DELETE, \
        detector, \
        img, \
        dl_recognizer, \
        detection_result, \
        IDLE, \
        kp, \
        sys_state_prev, \
        frame_count, \
        res, \
        dl_recognize_result
    M5.begin()
    Widgets.fillScreen(0x222222)
    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btnPWR_wasClicked_event)
    camera.init(pixformat=camera.RGB565, framesize=camera.QVGA)
    dual_button_0_blue, dual_button_0_red = DualButtonUnit((8, 9))
    dual_button_0_blue.setCallback(
        type=dual_button_0_blue.CB_TYPE.WAS_CLICKED, cb=dual_button_0_blue_wasClicked_event
    )
    dual_button_0_red.setCallback(
        type=dual_button_0_red.CB_TYPE.WAS_CLICKED, cb=dual_button_0_red_wasClicked_event
    )
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
    global \
        dual_button_0_blue, \
        dual_button_0_red, \
        sys_state, \
        FACE_RECOGNIZE, \
        FACE_ENROLL, \
        FACE_DELETE, \
        detector, \
        img, \
        dl_recognizer, \
        detection_result, \
        IDLE, \
        kp, \
        sys_state_prev, \
        frame_count, \
        res, \
        dl_recognize_result
    M5.update()
    dual_button_0_blue.tick(None)
    dual_button_0_red.tick(None)
    img = camera.snapshot()
    detection_result = detector.infer(img)
    if detection_result:
        for res in detection_result:
            kp = res.keypoint()
            img.draw_string(10, 10, str("face"), color=0x3333FF, scale=1)
            img.draw_circle(kp[0], kp[1], 3, color=0x3333FF, thickness=1, fill=True)
            img.draw_circle(kp[2], kp[3], 3, color=0x33FF33, thickness=1, fill=True)
            img.draw_circle(kp[4], kp[5], 3, color=0xFF0000, thickness=1, fill=True)
            img.draw_circle(kp[6], kp[7], 3, color=0x3333FF, thickness=1, fill=True)
            img.draw_circle(kp[8], kp[9], 3, color=0x33FF33, thickness=1, fill=True)
            img.draw_rectangle(
                res.x(), res.y(), res.w(), res.h(), color=0x3366FF, thickness=3, fill=False
            )
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
                        print((str("similarity: ") + str((dl_recognize_result.similarity()))))
                sys_state_prev = sys_state
                sys_state = IDLE
                frame_count = 15
        else:
            img.draw_string(104, 10, str("face no detect"), color=0xFF0000, scale=1)
    if frame_count > 0:
        frame_count = frame_count - 1
        if sys_state_prev == FACE_ENROLL:
            img.draw_string(116, 10, str("face enroll"), color=0x33FF33, scale=1)
        elif sys_state_prev == FACE_RECOGNIZE:
            if (dl_recognize_result.id()) > 0:
                img.draw_string(
                    100,
                    10,
                    str((str("recognize id: ") + str((dl_recognize_result.id())))),
                    color=0x33FF33,
                    scale=1,
                )
            else:
                img.draw_string(96, 10, str("no recognized"), color=0xFF0000, scale=1)
        elif sys_state_prev == FACE_DELETE:
            img.draw_string(
                100,
                10,
                str((str("remaining id: ") + str((dl_recognizer.enrolled_id_num())))),
                color=0xFF0000,
                scale=1,
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

```

Example output:

    None

## Funtions

<!-- .. function:: dl.ObjectDetector(model) -> ObjectDetector -->

    Create an object detector instance.

    :param model: Load a detection model. Supported values:

    - ``dl.model.HUMAN_FACE_DETECT``: Human face detection.
    - ``dl.model.PEDESTRIAN_DETECT``: Pedestrian detection.

    Returns An ``ObjectDetector`` instance.

    UiFlow2 Code Block:

    **Example**::

        detector = dl.ObjectDetector(dl.model.HUMAN_FACE_DETECT)
        detector = dl.ObjectDetector(dl.model.PEDESTRIAN_DETECT)

<!-- .. function:: dl.HumanFaceRecognizer() -> HumanFaceRecognizer -->

    Create a human face recognizer instance.

    Returns: A ``HumanFaceRecognizer`` instance.

    UiFlow2 Code Block:

## class ObjectDetector

The ObjectDetector object is returned by `dl.ObjectDetector(model)`.

<!-- .. method:: ObjectDetector.infer(img: image.Image) -> DetectionResult -->

    Returns: A ``DetectionResult`` instance.

    UiFlow2 Code Block:

## class HumanFaceRecognizer

The HumanFaceRecognizer object is returned by `dl.HumanFaceRecognizer()`.

<!-- .. method:: HumanFaceRecognizer.recognize(img: image:Image, keypoint: tuple) -> RecognitionResult -->

    Face recognize

    - ``img`` imput image
    - ``keypoint`` face keypoint, ref: DetectionResult.keypoint()

    Returns an ``RecognitionResult`` object

    UiFlow2 Code Block:

<!-- .. method:: HumanFaceRecognizer.clear_id() -->

    clear id

    UiFlow2 Code Block:

<!-- .. method:: HumanFaceRecognizer.enroll_id(img: image:Image, keypoint: tuple) -> bool -->

    enroll id

    - ``img`` imput image
    - ``keypoint`` face keypoint, ref: DetectionResult.keypoint()

    UiFlow2 Code Block:

<!-- .. method:: HumanFaceRecognizer.delete_id([id]) -->

    delete id

    id is an optional parameter. If provided, it deletes the specified face information. By default, it deletes the most recently recorded id.

    UiFlow2 Code Block:

<!-- .. method:: HumanFaceRecognizer.enrolled_id_num() -> int -->

    get enrolled id num

    UiFlow2 Code Block:

## class DetectionResult -- DetectionResult object

The line object is returned by `ObjectDetector.infer()`.

<!-- .. method:: DetectionResult.bbox() -> tuple(x, y, w, h) -->

    Get the bounding box of the object detection.

    UiFlow2 Code Block:

<!-- .. method:: DetectionResult.x() -> int -->

    The x-coordinate of the top-left corner of the bounding box.

    UiFlow2 Code Block:

<!-- .. method:: DetectionResult.y() -> int -->

    The y-coordinate of the top-left corner of the bounding box.

    UiFlow2 Code Block:

<!-- .. method:: DetectionResult.w() -> int -->

    The width of the bounding box.

    UiFlow2 Code Block:

<!-- .. method:: DetectionResult.h() -> int -->

    The height of the bounding box.

    UiFlow2 Code Block:

<!-- .. method:: DetectionResult.category() -> int -->

    The detected object's category.

    UiFlow2 Code Block:

<!-- .. method:: DetectionResult.keypoint() -> tuple -->

    Keypoint information (currently, only the face detection model outputs this data):

    - ``keypoint()[0], keypoint()[1]`` are the coordinates of the left eye.
    - ``keypoint()[2], keypoint()[3]`` are the coordinates of the left corner of the mouth.
    - ``keypoint()[4], keypoint()[5]`` are the coordinates of the nose.
    - ``keypoint()[6], keypoint()[7]`` are the coordinates of the right eye.
    - ``keypoint()[8], keypoint()[9]`` are the coordinates of the right corner of the mouth.

    UiFlow2 Code Block:

## class RecognitionResult -- RecognitionResult object

The ``RecognitionResult`` is returned by `HumanFaceRecognizer.recognize(img, keypoint)`.

<!-- .. method:: RecognitionResult.similarity() -> float -->

    Gets the face similarity, with a value closer to 1 indicating higher similarity.

    UiFlow2 Code Block:

<!-- .. method:: RecognitionResult.id() -> int -->

    Gets the face ID. A value greater than 0 indicates that the face recognition was successful.

    UiFlow2 Code Block:
