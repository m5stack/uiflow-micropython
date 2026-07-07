# Finger Unit

<!-- .. include:: ../refs/unit.finger.ref -->

The following products are supported:

    |FingerUnit|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import FingerUnit
import time

rect0 = None
rect1 = None
rect2 = None
label0 = None
label1 = None
label2 = None
label3 = None
title0 = None
finger_0 = None

ret = None
cur_time = None
t_x = None
last_touch_time = None
t_y = None

# Describe this function...
def add_handler():
    global \
        ret, \
        cur_time, \
        t_x, \
        last_touch_time, \
        t_y, \
        rect0, \
        rect1, \
        rect2, \
        label0, \
        label1, \
        label2, \
        label3, \
        title0, \
        finger_0
    label2.setColor(0xFFFFFF, 0x222222)
    label2.setText(str("add..."))
    if (finger_0.add_user(1, 1)) == 1:
        label2.setColor(0xFFFFFF, 0x62B900)
        label2.setText(str("added"))
    else:
        label2.setColor(0xFFFFFF, 0xF45554)
        label2.setText(str("add failed"))

# Describe this function...
def match_handler():
    global \
        ret, \
        cur_time, \
        t_x, \
        last_touch_time, \
        t_y, \
        rect0, \
        rect1, \
        rect2, \
        label0, \
        label1, \
        label2, \
        label3, \
        title0, \
        finger_0
    label2.setColor(0xFFFFFF, 0x222222)
    label2.setText(str("macth..."))
    ret = finger_0.compare_finger()
    if ret == 1:
        label2.setColor(0xFFFFFF, 0x62B900)
        label2.setText(str("macth"))
    else:
        label2.setColor(0xFFFFFF, 0xF45554)
        label2.setText(str("no macth"))

def setup():
    global \
        rect0, \
        rect1, \
        rect2, \
        label0, \
        label1, \
        label2, \
        label3, \
        title0, \
        finger_0, \
        ret, \
        cur_time, \
        t_x, \
        last_touch_time, \
        t_y

    M5.begin()
    Widgets.fillScreen(0x222222)
    rect0 = Widgets.Rectangle(8, 206, 95, 30, 0xFFFFFF, 0xFFFFFF)
    rect1 = Widgets.Rectangle(112, 206, 95, 30, 0xFFFFFF, 0xFFFFFF)
    rect2 = Widgets.Rectangle(216, 206, 95, 30, 0xFFFFFF, 0xFFFFFF)
    label0 = Widgets.Label("Add", 37, 213, 1.0, 0x000000, 0xFFFFFF, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("Match", 132, 212, 1.0, 0x000000, 0xFCFCFC, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 132, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 8, 27, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title("Finger Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    finger_0 = FingerUnit(port=(18, 17))
    finger_0.delete_all_user()
    finger_0.set_add_mode(0)
    label3.setText(str((str("User Num: ") + str((finger_0.get_user_count())))))
    last_touch_time = time.ticks_ms()

def loop():
    global \
        rect0, \
        rect1, \
        rect2, \
        label0, \
        label1, \
        label2, \
        label3, \
        title0, \
        finger_0, \
        ret, \
        cur_time, \
        t_x, \
        last_touch_time, \
        t_y
    M5.update()
    if M5.Touch.getCount():
        cur_time = time.ticks_ms()
        if cur_time - last_touch_time > 150:
            t_x = M5.Touch.getX()
            t_y = M5.Touch.getY()
            if t_x >= 8 and t_x <= 8 + 95 and t_y >= 206 and t_y <= 206 + 30:
                rect0.setColor(color=0x007BFF, fill_c=0x007BFF)
                label0.setColor(0xFFFFFF, 0x007BFF)
                add_handler()
            else:
                rect0.setColor(color=0xFFFFFF, fill_c=0xFFFFFF)
                label0.setColor(0x000000, 0xFFFFFF)
            if t_x >= 112 and t_x <= 112 + 95 and t_y >= 206 and t_y <= 206 + 30:
                rect1.setColor(color=0x007BFF, fill_c=0x007BFF)
                label1.setColor(0xFFFFFF, 0x007BFF)
                match_handler()
            else:
                rect1.setColor(color=0xFFFFFF, fill_c=0xFFFFFF)
                label1.setColor(0x000000, 0xFFFFFF)
            last_touch_time = time.ticks_ms()
    label3.setText(str((str("User Num: ") + str((finger_0.get_user_count())))))

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

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |cores3_finger_example.m5f2|

## class FingerUnit

## Constructors

<!-- .. class:: FingerUnit(id: Literal[0, 1, 2] = 1, port: list | tuple = None) -->

    Create a FingerUnit object.

    :param id: The ID of the UART, 0 or 1 or 2.
    :param port: UART pin numbers.

    UIFLOW2:

<!-- .. _unit.FingerUnit.Methods: -->

## Methods

<!-- .. method:: FingerUnit.sleep() -> bool -->

    After calling this method successfully, FPC1020A will not be able to respond to any messages.

    :returns: True if the command was successful, False otherwise.

    UIFLOW2:

<!-- .. method:: FingerUnit.get_add_mode() -> int -->

    In the no-repeat mode, only one user can be added with the same finger,
    and an error message will be returned if the second round of adding is
    forced.

    :returns: mode (0: no-repeat mode, 1: repeat mode)

    UIFLOW2:

<!-- .. method:: FingerUnit.set_add_mode(mode: int) -> int -->

    In the no-repeat mode, only one user can be added with the same finger,
    and an error message will be returned if the second round of adding is
    forced.

    :param mode: mode (0: no-repeat mode, 1: repeat mode)

    :returns: mode (0: no-repeat mode, 1: repeat mode)

    UIFLOW2:

<!-- .. method:: FingerUnit.add_user(id: int, permission: Literal[1, 2, 3]) -> int -->

    add new user

    After calling this method, you need to put your finger on the fingerprint module.

    :param id: user id (0-149)
    :param permission: user permission (1: normal, 2: admin, 3: super admin)

    :returns: -1 if the command was unsuccessful, otherwise the user id.

    UIFLOW2:

<!-- .. method:: FingerUnit.delete_user(id: int) -> int -->

    Delete the user with the specified id.

    :param id: user id (0-149)

    :returns: -1 if the command was unsuccessful, otherwise the user id.

    UIFLOW2:

<!-- .. method:: FingerUnit.delete_all_user() -> bool -->

    Delete all users.

    :returns: True if the command was successful, False otherwise.

    UIFLOW2:

<!-- .. method:: FingerUnit.get_user_count() -> int -->

    Get registered users count.

    :returns: -1 if the command was unsuccessful, otherwise the number of registered users.

    UIFLOW2:

<!-- .. method:: FingerUnit.get_user_capacity() -> int -->

    Get the maximum number of users that can be registered.

    :returns: -1 if the command was unsuccessful, otherwise the maximum number of users that can be registered.

    UIFLOW2:

<!-- .. method:: FingerUnit.compare_id(id: int, timeout: int=5000) -> bool -->

    Check whether the currently collected fingerprint matches the specified user id.

    :param id: user id (0-149)

    :returns: -1 if the command was unsuccessful, otherwise the user id.

    UIFLOW2:

<!-- .. method:: FingerUnit.compare_finger(timeout: int=5000) -> int -->

    Detect whether the currently collected fingerprint is a registered user.

    :returns: -1 if the command was unsuccessful, otherwise the user id.

    UIFLOW2:

<!-- .. method:: FingerUnit.get_user_list() -> list -->

    Get the list of registered users.

    :returns: list of registered users.

    UIFLOW2:

<!-- .. method:: FingerUnit.get_user_info(id: int) -> Union[tuple, None]: -->

    Get the information of the user with the specified id.

    :param id: user id (0-149)

    :returns: tuple of (id, permission) if the command was successful, None otherwise.

    UIFLOW2:

<!-- .. method:: FingerUnit.get_user_permission(id: int) -> int -->

    Get the permission of the user with the specified id.

    :param id: user id (0-149)

    :returns: -1 if the command was unsuccessful, otherwise the permission of the user.

    UIFLOW2:

<!-- .. method:: FingerUnit.get_user_characteristics(id: int) -> Union[bytes, None] -->

    Get the characteristics of the user with the specified id.

    :param id: user id (0-149)

    :returns: bytes of the characteristics if the command was successful, None otherwise.

    UIFLOW2:

<!-- .. method:: FingerUnit.add_user_info(id, permissions, characteristic, timeout: int=5000) -> bool -->

    Register a new user with FPC1020A.

    :param id: user id (0-149)
    :param permissions: user permission (1: normal, 2: admin, 3: super admin)
    :param characteristic: user characteristics
    :param timeout: timeout in milliseconds

    :returns: True if the command was successful, False otherwise.

    UIFLOW2:

<!-- .. method:: FingerUnit.capture_characteristic(timeout: int=5000) -> bytes -->

    Capture the characteristics of the fingerprint.

    :param timeout: timeout in milliseconds

    :returns: bytes of the characteristics if the command was successful, None otherwise.

<!-- .. method:: FingerUnit.get_match_level() -> int -->

    The comparison level ranges from 0 to 9, the larger the value, the stricter the comparison, and the default value is 5.

    :returns: match level (0-9)

    UIFLOW2:

<!-- .. method:: FingerUnit.set_match_level(level: int) -> int -->

    The comparison level ranges from 0 to 9, the larger the value, the stricter the comparison, and the default value is 5.

    :param level: match level (0-9)

    :returns: match level (0-9)

    UIFLOW2:

<!-- .. method:: FingerUnit.get_version() -> str -->

    Get the version information of FPC1020A.

    :returns: version information.
