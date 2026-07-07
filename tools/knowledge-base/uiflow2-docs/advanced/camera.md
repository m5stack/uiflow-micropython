# camera

<!-- .. include:: ../refs/advanced.camera.ref -->

The camera module is used for taking pictures.

<!-- .. note:: This module is only applicable to the CoreS3 Controller -->

<!-- .. module:: camera -->
    :synopsis: camera sensor

## Micropython Example

###### capture display

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
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

## UiFlow2 Example

###### capture display

<!-- .. only:: builder_html -->

    |cores3_example_camera_display.m5f2|

## Functions

<!-- .. function:: camera.init(pixformat, framesize) -->

    Initializes the camera sensor.

    The ``pixformat`` supports (note: camera.JPEG is only for AtomS3R-M12):

    - ``camera.RGB565``
    - ``camera.JPEG``

    The ``framesize`` supports (note: Resolutions higher than camera.QVGA are only supported when pixformat is set to JPEG.):

    - ``camera.QQVGA``: 160x120
    - ``camera.QCIF``: 176x144
    - ``camera.HQVGA``: 240x176
    - ``camera.FRAME_240X240``: 240x240
    - ``camera.QVGA``: 320x240
    - ``camera.VGA``: 640x480
    - ``camera.SVGA``: 800x600
    - ``camera.XGA``: 1024x768
    - ``camera.HD``: 1280x720
    - ``camera.SXGA``: 1280x1024
    - ``camera.UXGA``: 1600x1200
    - ``camera.FHD``: 1920x1080
    - ``camera.QXGA``: 2048x1536

    UiFlow2

<!-- .. function:: camera.snapshot() -> image.Iamge -->

    Capture a single frame.

    Returns An ``image.Image`` object.

    UiFlow2

<!-- .. function:: camera.set_hmirror(enable) -->

    Turns horizontal mirror mode on (True) or off (False). Defaults to on.

    UiFlow2

<!-- .. function:: camera.set_vflip(enable) -->

    Turns vertical flip mode on (True) or off (False). Defaults to off.

    UiFlow2

<!-- .. function:: camera.get_hmirror() -->

    Returns if horizontal mirror mode is enabled.

    UiFlow2

<!-- .. function:: camera.get_vflip() -->

    Returns if vertical flip mode is enabled.

    UiFlow2
