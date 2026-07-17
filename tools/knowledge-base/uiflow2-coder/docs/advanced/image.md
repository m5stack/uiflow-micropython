# image

> Note: This module is only applicable to the CoreS3 Controller
## MicroPython Example

### draw test

```python
import os, sys, io
import M5
from M5 import *
import camera
import image

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
    img.draw_string(10, 10, str("M5Stack"), color=0x3366FF, scale=2)
    img.draw_rectangle(60, 80, 50, 40, color=0x33CC00, thickness=3, fill=False)
    img.draw_line(200, 60, 260, 100, color=0xFF0000, thickness=3)
    img.draw_circle(160, 120, 30, color=0xFFCC00, thickness=2, fill=False)
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

### find qrcode

```python
import os, sys, io
import M5
from M5 import *
import camera
import image

img = None
qrcode_list = None
qrcode_res = None
corners = None
i = None
point = None
coord = None
x0 = None
y0 = None
x1 = None
y1 = None

def setup():
    global img, qrcode_list, corners, point, i, coord, x0, y0, x1, y1
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    camera.init(pixformat=camera.RGB565, framesize=camera.QVGA)

def loop():
    global img, qrcode_list, corners, point, i, coord, x0, y0, x1, y1
    M5.update()
    img = camera.snapshot()
    qrcode_list = img.find_qrcodes()
    if qrcode_list:
        for qrcode_res in qrcode_list:
            corners = qrcode_res.corners()
            for i in range(len(corners)):
                point = i
                coord = corners[int((point + 1) - 1)]
                x0 = coord[0]
                y0 = coord[1]
                point = (i + 1) % len(corners)
                coord = corners[int((point + 1) - 1)]
                x1 = coord[0]
                y1 = coord[1]
                img.draw_line(x0, y0, x1, y1, color=0x3333FF, thickness=3)
            img.draw_string(0, 0, str(qrcode_res.payload()), color=0x3333FF, scale=1.5)
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

## **API**

### `class image.Image`

    The image.Image object is returned by `camera.snapshot()`.

### `width()`

        Returns the image width in pixels.

```python
width()
```
### `height()`

        Returns the image height in pixels.

```python
height()
```
### `format()`

        Returns the image format.

        Returns image.GRAYSCALE for grayscale images, image.RGB565 for RGB565 images, image.BAYER for bayer pattern images, and image.JPEG for JPEG images.

```python
format()
```
### `size()`

        Returns the image size in bytes.

```python
size()
```
### `bytearray()`

        Returns a bytearray object that points to the image data for byte-level read/write access.

```python
bytearray()
```
### `draw_line(x0, y0, x1, y1, color, thickness)`

        Draws a line from (x0, y0) to (x1, y1) on the image. You may either
        pass x0, y0, x1, y1 separately or as a tuple (x0, y0, x1, y1).

        - Parameter `x0` (`int`): start x coordinate.
        - Parameter `y0` (`int`): start y coordinate.
        - Parameter `x1` (`int`): end x coordinate.
        - Parameter `y1` (`int`): end y coordinate.
        - Parameter `color`: RGB888 tuple, grayscale value (0-255), or RGB565 value. Defaults to white.
        - Parameter `thickness` (`int`): line thickness in pixels. Defaults to 1.

```python
img.draw_line(10, 10, 100, 100, color=(255,0,0), thickness=2)
```
### `draw_rectangle(x, y, w, h, color, thickness, fill)`

        Draws a rectangle on the image. You may either pass x, y, w, h separately
        or as a tuple (x, y, w, h).

        - Parameter `x` (`int`): top-left x coordinate.
        - Parameter `y` (`int`): top-left y coordinate.
        - Parameter `w` (`int`): rectangle width.
        - Parameter `h` (`int`): rectangle height.
        - Parameter `color`: RGB888 tuple, grayscale value (0-255), or RGB565 value. Defaults to white.
        - Parameter `thickness` (`int`): border thickness in pixels. Defaults to 1.
        - Parameter `fill` (`bool`): set True to fill the rectangle. Defaults to False.

```python
img.draw_rectangle(20, 20, 80, 60, color=(0,255,0), thickness=2, fill=True)
```
### `draw_circle(x, y, radius, color, thickness, fill)`

        Draws a circle on the image. You may either pass x, y, radius separately or
        as a tuple (x, y, radius).

        - Parameter `x` (`int`): circle center x coordinate.
        - Parameter `y` (`int`): circle center y coordinate.
        - Parameter `radius` (`int`): circle radius.
        - Parameter `color`: RGB888 tuple, grayscale value (0-255), or RGB565 value. Defaults to white.
        - Parameter `thickness` (`int`): border thickness in pixels. Defaults to 1.
        - Parameter `fill` (`bool`): set True to fill the circle. Defaults to False.

```python
img.draw_circle(50, 50, 30, color=(0,0,255), thickness=3, fill=False)
```
### `draw_string(x, y, text, color, scale)`

        Draws 8x16 text starting at location (x, y) in the image. You may either pass
        x, y separately or as a tuple (x, y).

        - Parameter `x` (`int`): text start x coordinate.
        - Parameter `y` (`int`): text start y coordinate.
        - Parameter `text` (`str`): text to draw. Supports `\n`, `\r`, `\r\n` line breaks.
        - Parameter `color`: RGB888 tuple, grayscale value (0-255), or RGB565 value. Defaults to white.
        - Parameter `scale`: scale factor to resize text. Integer or float > 0. Defaults to 1.

```python
img.draw_string(10, 10, "Hello", color=(255,255,0), scale=2)
```
### `find_qrcodes()`

        Finds all QR codes returns a list of `image.qrcode` objects.
        Please see the image.qrcode object for more details.

```python
qrcodes = img.find_qrcodes()
```
### `class image.qrcode`

    Please call `Image.find_qrcodes()` to create this object.

### `corners()`

        Get the 4 corners of the QR code in clockwise order starting from the top-left.

```python
q.corners()
```
### `rect()`

        Get the bounding box of the QR code.

```python
q.rect()
```
### `x()`

        Get the bounding box x coordinate.

```python
q.x()
```
### `y()`

        Get the bounding box y coordinate.

```python
q.y()
```
### `w()`

        Get the bounding box width.

```python
q.w()
```
### `h()`

        Get the bounding box height.

```python
q.h()
```
### `payload()`

        Get the decoded payload string (e.g. URL) from the QR code.

```python
q.payload()
```
### `version()`

        Get the QR code version number.

```python
q.version()
```
### `ecc_level()`

        Get the QR code ECC (error correction) level.

        ECC levels: L, M, Q, H. Higher levels allow more damage tolerance but reduce data capacity.

```python
q.ecc_level()
```
### `mask()`

        Get the QR code mask pattern (0~7).

        Mask is used to improve QR readability.

```python
q.mask()
```
### `eci()`

        Get the QR code ECI (Extended Channel Interpretation) value.

        ECI indicates the text encoding (e.g. UTF-8, Shift-JIS). `0` means ECI not used.

```python
q.eci()
```
## Constants

### `RGB565`

    RGB565 pixel format. Each pixel is 16-bits, 2-bytes. 5-bits are used for red,
    6-bits are used for green, and 5-bits are used for blue.

### `GRAYSCALE`

    GRAYSCALE pixel format. Each pixel is 8-bits, 1-byte.

### `JPEG`

    A JPEG image.

### `YUV422`

    A pixel format that is very easy to jpeg compress. Each pixel is stored as a grayscale
    8-bit Y value followed by alternating 8-bit U/V color values that are shared between two
    Y values (8-bits Y1, 8-bits U, 8-bits Y2, 8-bits V, etc.). Only some image processing
    methods work with YUV422.
