# keyboard

<!-- .. currentmodule:: usb.device.keyboard -->

<!-- .. module:: keyboard -->
    :synopsis: bluetooth keyboard

usb device keyboard

<!-- .. include:: ../../../refs/advanced.usb.device.keyboard.ref -->

<!-- .. note:: This module is only applicable to the CoreS3 Controller -->

## Micropython Example

###### USB keyboard

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from unit import CardKBUnit
from usb.device.keyboard import Keyboard
from hardware import I2C
from hardware import Pin

label = None
keyboard = None
i2c0 = None
cardkb_0 = None
key = None
update = None

def cardkb_0_pressed_event(kb):
    global label, keyboard, i2c0, cardkb_0, key, update
    key = cardkb_0.get_key()
    update = True

def setup():
    global label, keyboard, i2c0, cardkb_0, key, update
    M5.begin()
    Widgets.fillScreen(0x222222)
    label = Widgets.Label("USB Keyboard", 73, 6, 1.0, 0x3CC7F1, 0x222222, Widgets.FONTS.DejaVu24)
    keyboard = Keyboard()
    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    cardkb_0 = CardKBUnit(i2c0)
    cardkb_0.set_callback(cardkb_0_pressed_event)
    update = False

def loop():
    global label, keyboard, i2c0, cardkb_0, key, update
    M5.update()
    cardkb_0.tick()
    if keyboard.is_open():
        if update:
            keyboard.input(str(chr(key)))
            update = False

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

###### USB keyboard

<!-- .. only:: builder_html -->

    |m5cores3_usbd_keyboard_example.m5f2|

## class Keyboard

<!-- .. class:: usb.device.keyboard.Keyboard() -->

    Create Keyboard object

    UIFlow2.0

<!-- .. method:: Keyboard.set_modifiers(right_gui: bool = False, right_alt: bool = False, right_shift: bool = False, right_ctrl: bool = False, \ -->
                       left_gui: bool = False, left_alt: bool = False, left_shift: bool = False, left_ctrl: bool = False)

    Set modifier keys

    - ``right_gui`` The state of the right-side GUI key. True indicates that the key is pressed.
    - ``right_alt`` The state of the right-side Alt key. True indicates that the key is pressed.
    - ``right_shift`` The state of the right-side Shift key. True indicates that the key is pressed.
    - ``right_ctrl`` The state of the right-side Ctrl key. True indicates that the key is pressed.
    - ``left_gui`` The state of the left-side GUI key. True indicates that the key is pressed.
    - ``left_alt`` The state of the left-side Alt key. True indicates that the key is pressed.
    - ``left_shift`` The state of the left-side Shift key. True indicates that the key is pressed.
    - ``left_ctrl``  The state of the left-side Ctrl key. True indicates that the key is pressed.

    :note: Changes will take effect after calling Keyboard.send_report().

    UIFlow2.0

<!-- .. method:: Keyboard.set_keys(k0: int = 0, k1: int = 0, k2: int = 0, k3: int = 0, k4: int = 0, k5: int = 0) -->

    Press specified keys (up to 6 key values at a time)

    - ``k0~k5`` The input is a standard HID key value. For details, refer to the KeyCode() class.

    :note: Changes will take effect after calling Keyboard.send_report().

    example: Press the lowercase 'a'

```
```
        Keyboard.set_keys(k0=KeyCode.A)
        Keyboard.send_report()
        Keyboard.set_keys(k0=0)
        Keyboard.send_report()

    example: Press the uppercase 'A'

```
```
        Keyboard.set_modifiers(right_shift=True)
        Keyboard.set_keys(k0=KeyCode.A)
        Keyboard.send_report()
        Keyboard.set_modifiers(right_shift=False)
        Keyboard.set_keys(k0=0)
        Keyboard.send_report()

    UIFlow2.0

<!-- .. method:: Keyboard.send_report() -->

    Send keyboard status report

    UIFlow2.0

<!-- .. method:: Keyboard.input(key) -->

    input key

    - ``key`` The input can be a string within the ASCII range or a value from KeyCode.

    example::

        Keyboard.input("Hello M5")
        Keyboard.input(KeyCode.A)

    UIFlow2.0
