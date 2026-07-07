<!-- .. py:currentmodule:: touch -->

# Touch

<!-- .. include:: ../refs/hardware.touch.ref -->

The ``Touch`` class provides methods for reading touch coordinates, the number of touch points, and detailed touch information on M5Stack devices with touch screens.

## UiFlow2 Example

#### Getting Touch Coordinates

Open the |cores3_touch_example.m5f2| project in UiFlow2.

This example demonstrates how to obtain the X and Y coordinates of a touch event and display them on the screen.

UiFlow2 Code Block:

Example output:

    Screen displays the current X and Y coordinates of the touch event.

## MicroPython Example

#### Getting Touch Coordinates

This example demonstrates how to obtain the X and Y coordinates of a touch event and display them on the screen.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *

label0 = None
label1 = None

cur_x = None
cur_y = None

def setup():
    global label0, label1, cur_x, cur_y

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("x: 0", 32, 41, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("y: 0", 33, 84, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

def loop():
    global label0, label1, cur_x, cur_y
    M5.update()
    if M5.Touch.getCount():
        cur_x = M5.Touch.getX()
        cur_y = M5.Touch.getY()
        label0.setText(str((str("x: ") + str(cur_x))))
        label1.setText(str((str("y: ") + str(cur_y))))

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

    Screen displays the current X and Y coordinates of the touch event.

## API

#### Touch

<!-- .. class:: M5.Touch() -->

<!-- .. py:method:: getX() -->

        Get the current X coordinate of the touch.

        The returned coordinate is automatically adjusted based on the current
        display rotation set by ``setRotation()``.

        :returns: int - The X coordinate.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                x = M5.Touch.getX()

<!-- .. py:method:: getY() -->

        Get the current Y coordinate of the touch.

        The returned coordinate is automatically adjusted based on the current
        display rotation set by ``setRotation()``.

        :returns: int - The Y coordinate.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                y = M5.Touch.getY()

<!-- .. py:method:: getCount() -->

        Get the number of current touch points.

        :returns: int - Number of active touches (0 if no touch).

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                count = M5.Touch.getCount()

<!-- .. py:method:: getDetail(index=0) -->

        Get detailed information about a specific touch point.

        :param int index: Index of the touch point (default is 0).
        :returns: tuple - A tuple of 11 elements containing detailed touch status:

            - ``[0] deltaX`` (int): The X-axis difference since the last measurement.
            - ``[1] deltaY`` (int): The Y-axis difference since the last measurement.
            - ``[2] distanceX`` (int): The total X-axis distance moved since touched.
            - ``[3] distanceY`` (int): The total Y-axis distance moved since touched.
            - ``[4] isPressed`` (bool): True if currently being pressed.
            - ``[5] wasPressed`` (bool): True if just transitioned to pressed state.
            - ``[6] wasClicked`` (bool): True if just clicked.
            - ``[7] isReleased`` (bool): True if currently released.
            - ``[8] wasReleased`` (bool): True if just transitioned to released state.
            - ``[9] isHolding`` (bool): True if currently being held.
            - ``[10] wasHold`` (bool): True if it was held.

        MicroPython Code Block:

<!-- .. code-block:: python -->

                detail = M5.Touch.getDetail(0)

<!-- .. py:method:: getTouchPointRaw(index=0) -->

        Get the raw touch point coordinates.

<!-- .. warning:: -->

            This method returns **raw hardware coordinates** that are **NOT**
            adjusted for the current display rotation set by ``setRotation()``.
            If you have changed the display rotation, you must manually transform
            the coordinates to match the display orientation.

            For single-touch scenarios, prefer ``getX()`` / ``getY()`` which
            automatically adjust for rotation. Use ``getTouchPointRaw()`` only
            when you need multi-touch support.

        :param int index: Index of the touch point (default is 0).
        :returns: tuple - A tuple of 4 elements containing raw touch point data:

            - ``[0] x`` (int): The raw X coordinate.
            - ``[1] y`` (int): The raw Y coordinate.
            - ``[2] size`` (int): The size or pressure of the touch point.
            - ``[3] id`` (int): The unique identifier for tracking the touch point.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                raw = M5.Touch.getTouchPointRaw(0)

        **Coordinate Transformation for Multi-Touch**

        When the display rotation is changed via ``setRotation()``, the raw
        coordinates from ``getTouchPointRaw()`` must be manually transformed
        to match the current screen orientation:

<!-- .. code-block:: python -->

                def transform_touch(raw_x, raw_y, rotation, raw_w, raw_h):
                    """Transform raw touch coordinates to match display rotation."""
                    if rotation == 0:
                        return raw_x, raw_y
                    elif rotation == 1:
                        return raw_y, (raw_w - 1) - raw_x
                    elif rotation == 2:
                        return (raw_w - 1) - raw_x, (raw_h - 1) - raw_y
                    elif rotation == 3:
                        return (raw_h - 1) - raw_y, raw_x
                    return raw_x, raw_y

                # Usage:
                raw = M5.Touch.getTouchPointRaw(0)
                if raw:
                    x, y, _, _ = raw
                    # raw_w, raw_h = physical panel size (before rotation)
                    sx, sy = transform_touch(x, y, M5.Lcd.getRotation(), 1280, 720)

        For single-touch scenarios, prefer ``getX()`` / ``getY()`` which
        handle rotation automatically.
