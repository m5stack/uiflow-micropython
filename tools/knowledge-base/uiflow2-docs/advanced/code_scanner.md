# code_scanner

<!-- .. include:: ../refs/advanced.code_scanner.ref -->

<!-- .. note:: This module is only applicable to the CoreS3 Controller -->

<!-- .. module:: code_scanner -->
   :synopsis:

``code_scanner`` module for qrcode scanning recognition

## Micropython Example

###### qrcode detect

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
import camera
import code_scanner
import image

img = None
qrcode = None

def setup():
    global img, qrcode
    M5.begin()
    Widgets.fillScreen(0x222222)
    camera.init(pixformat=camera.RGB565, framesize=camera.QVGA)
    camera.set_hmirror(False)

def loop():
    global img, qrcode
    M5.update()
    img = camera.snapshot()
    qrcode = code_scanner.find_qrcodes(img)
    if qrcode:
        print(qrcode.payload())
        print(qrcode.type_name())
        img.draw_string(10, 10, str(qrcode.payload()), color=0x3333FF, scale=2)
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

###### qrcode detect

<!-- .. only:: builder_html -->

    |qrcode_detect_example.m5f2|

## Methods

<!-- .. method:: find_qrcodes(img: image.Image) -> image.qrcode -->

    QR code recognition

    - ``img`` Image to be recognized

    Returns ``image.qrcode`` instance

    UIFlow2.0

## class image.QRCode

``QRCode`` The QRCode object is returned by `code_scanner.find_qrcodes(img: image.Image)`.

<!-- .. method:: payload() -> str -->

    Return the payload string of the QR code

    UIFlow2.0

<!-- .. method:: type_name() -> str -->

    Return the type of the QR code

    UIFlow2.0
