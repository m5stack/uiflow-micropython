# jpg

<!-- .. include:: ../refs/advanced.jpg.ref -->

<!-- .. note:: This module is only applicable to the CoreS3 Controller -->

<!-- .. module:: jpg -->
   :synopsis:

``jpg`` module for encoding and decoding operations of JPG format images

## Micropython Example

###### take photo

Click the screen to start the countdown and take a photo

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
import camera
import image
import time
import jpg

file_0 = None
img = None
cnt = None
last_time = None
index = None
img_jpg = None

def setup():
    global file_0, img, cnt, last_time, index, img_jpg
    M5.begin()
    Widgets.fillScreen(0x222222)
    camera.init(pixformat=camera.RGB565, framesize=camera.QVGA)
    cnt = 0
    last_time = 0
    index = 0

def loop():
    global file_0, img, cnt, last_time, index, img_jpg
    M5.update()
    img = camera.snapshot()
    if (M5.Touch.getCount()) > 0:
        cnt = 5
        print("hello M5")
    if cnt > 0:
        if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
            last_time = time.ticks_ms()
            cnt = cnt - 1
            if cnt == 0:
                img_jpg = jpg.encode(img, 80)
                index = index + 1
                file_0 = open(
                    "/flash/" + str((str("photo") + str((str(index) + str(".jpg"))))), "w"
                )
                file_0.write(img_jpg.bytearray())
                file_0.close()
        img.draw_string(140, 80, str(cnt), color=0x000099, scale=5)
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

## UIFlow2.0 Example

###### take photo

Click the screen to start the countdown and take a photo

<!-- .. only:: builder_html -->

    |take_photo_example.m5f2|

## Methods

<!-- .. method:: encode(img: image.Image, quality=60) -> image.Image -->

    encode to jog photo

    - ``img`` Image to be encoded, in the format of image.RGB565

    Return ``image.Image`` instance, image format image.JPEG

    UIFlow2.0

<!-- .. method:: decode(img_jpg: image.Image) -> image.Image -->

    jpg photo decode

    - ``img`` Image to be decoded, in the format of image.JPEG

    Return ``image.Image`` instance, image format image.RGB565

    UIFlow2.0
