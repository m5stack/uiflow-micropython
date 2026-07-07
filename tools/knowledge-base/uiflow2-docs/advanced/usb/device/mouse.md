# mouse

<!-- .. currentmodule:: usb.device.keyboard -->

<!-- .. module:: mouse -->
    :synopsis: usb mouse

usb device mouse

<!-- .. include:: ../../../refs/advanced.usb.device.mouse.ref -->

<!-- .. note:: This module is only applicable to the CoreS3 Controller -->

## Micropython Example

###### USB Mouse

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from usb.device.mouse import Mouse
import time
import m5utils

label0 = None
mouse = None
touch_active = None
sensitivity = None
x = None
last_touch_time = None
y = None
dx = None
click_active = None
dy = None
prev_x = None
prev_y = None

def setup():
    global \
        label0, \
        mouse, \
        touch_active, \
        sensitivity, \
        x, \
        last_touch_time, \
        y, \
        dx, \
        click_active, \
        dy, \
        prev_x, \
        prev_y
    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("USB Mouse", 91, 6, 1.0, 0x158EE6, 0x222222, Widgets.FONTS.DejaVu24)
    mouse = Mouse()
    touch_active = False
    sensitivity = 2
    last_touch_time = 0
    click_active = False

def loop():
    global \
        label0, \
        mouse, \
        touch_active, \
        sensitivity, \
        x, \
        last_touch_time, \
        y, \
        dx, \
        click_active, \
        dy, \
        prev_x, \
        prev_y
    M5.update()
    if mouse.is_open():
        if M5.Touch.getCount():
            x = m5utils.remap(M5.Touch.getX(), 0, 320, -127, 127)
            y = m5utils.remap(M5.Touch.getY(), 0, 240, -127, 127)
            if not touch_active:
                touch_active = True
                prev_x = x
                prev_y = y
                last_touch_time = time.ticks_ms()
            if x != prev_x or y != prev_y:
                dx = x - prev_x
                dy = y - prev_y
                prev_x = x
                prev_y = y
                mouse.move(int(dx * sensitivity), int(dy * sensitivity))
        else:
            touch_active = False
            dx = 0
            dy = 0
            if (time.ticks_diff((time.ticks_ms()), last_touch_time)) < 100:
                if click_active and dx < 30 and dy < 30:
                    click_active = False
                    mouse.click_left(True)
            else:
                click_active = True
        if BtnPWR.wasClicked():
            mouse.click_right(True)
    else:
        time.sleep_ms(100)

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

###### USB Mouse

<!-- .. only:: builder_html -->

    |m5cores3_usbd_mouse_example.m5f2|

## class Mouse

<!-- .. class:: usb.device.mouse.Mouse() -->

    Create Mouse object

    UIFlow2.0

<!-- .. method:: Mouse.set_axes(x: int = 0, y: int = 0) -->

    Set Cursor Position

    - ``x`` Horizontal movement, range: -127 to 127. A value less than 0 moves the cursor to the left, and a value greater than 0 moves it to the right.
    - ``y`` Vertical movement, range: -127 to 127. A value less than 0 scrolls the cursor up, and a value greater than 0 scrolls it down.

    :note: Changes will take effect after calling Mouse.send_report().

    UIFlow2.0

<!-- .. method:: Mouse.set_wheel(w: int = 0) -->

    Set mouse wheel value

    - ``w`` Wheel value, range: -127 to 127. A value less than 0 scrolls the wheel down, and a value greater than 0 scrolls the wheel up.

    :note: Changes will take effect after calling Mouse.send_report().

    UIFlow2.0

<!-- .. method:: Mouse.set_buttons(left: bool = False, right: bool = False, middle: bool = False) -->

    Set mouse button status

    - ``left`` True indicates the left button is pressed.
    - ``right`` True indicates the right button is pressed.
    - ``middle`` True indicates the middle (wheel) button is pressed.

    :note: Changes will take effect after calling Mouse.send_report().

    example: Mouse click left button

```
```
        set_buttons(left=True)  # press
        send_report()
        set_buttons(left=False) # release
        send_report()

    UIFlow2.0

<!-- .. method:: Mouse.send_report() -->

    Send the mouse status report.

    UIFlow2.0

<!-- .. method:: Mouse.move(x: int = 0, y: int = 0) -->

    Move cursor

    - ``x`` Horizontal movement, range: -127 to 127. A value less than 0 moves the cursor to the left, and a value greater than 0 moves it to the right.
    - ``y`` Vertical movement, range: -127 to 127. A value less than 0 moves the cursor up, and a value greater than 0 moves it down.

    UIFlow2.0

<!-- .. method:: Mouse.click_left(release: bool = True) -->

    Click left button

    - ``release``  Set to True to release the left mouse button after pressing, or False to not release.

    UIFlow2.0

<!-- .. method:: Mouse.click_right(release: bool = True) -->

    Click right button

    - ``release``  Set to True to release the right mouse button after pressing, or False to not release.

    UIFlow2.0

<!-- .. method:: Mouse.click_middle(release: bool = True) -->

    Click middle button

    - ``release``  Set to True to release the left middle button after pressing, or False to not release.

    UIFlow2.0

<!-- .. method:: Mouse.click_forawrd() -->

    Click forward button

    - ``release``  Set to True to release the left forward button after pressing, or False to not release.

    UIFlow2.0

<!-- .. method:: Mouse.click_backward() -->

    Click backward button

    - ``release``  Set to True to release the left backward button after pressing, or False to not release.

    UIFlow2.0

<!-- .. method:: Mouse.scroll(w: int) -->

    Scroll wheel

    - ``w`` range: -127 to 127, values less than 0 scroll up, and values greater than 0 scroll down.

    UIFlow2.0
