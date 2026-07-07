<!-- .. currentmodule:: m5ui -->

# M5LED

<!-- .. include:: ../refs/m5ui.led.ref -->

M5LED is a lightweight widget that simulates a light-emitting diode indicator in the user interface.

## UiFlow2 Example

#### LED Basic Usage Example

Open the |m5cores3_m5ui_led_example.m5f2| project in UiFlow2.

This example demonstrates how to create and control an LED widget.
It shows how to turn the LED on and off, change its color, adjust brightness.

UiFlow2 Code Block:

Example output:

    None.

## MicroPython Example

#### LED Basic Usage Example

This example demonstrates how to create and control an LED widget.
It shows how to turn the LED on and off, change its color, adjust brightness.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import m5utils

page0 = None
led0 = None
switch0 = None
slider0 = None
label0 = None
brightness = None

def switch0_checked_event(event_struct):
    global page0, led0, switch0, slider0, label0, brightness
    led0.set_color(0x3366FF)
    led0.on()

def switch0_unchecked_event(event_struct):
    global page0, led0, switch0, slider0, label0, brightness
    led0.off()
    led0.set_color(0x000000)

def slider0_value_changed_event(event_struct):
    global page0, led0, switch0, slider0, label0, brightness
    brightness = slider0.get_value()
    led0.set_brightness(int(m5utils.remap(brightness, 0, 100, 80, 255)))
    label0.set_text(str((str("Brightness: ") + str((str(brightness) + str("%"))))))
    print(led0.get_brightness())

def switch0_event_handler(event_struct):
    global page0, led0, switch0, slider0, label0, brightness
    event = event_struct.code
    obj = event_struct.get_target_obj()
    if event == lv.EVENT.VALUE_CHANGED:
        if obj.has_state(lv.STATE.CHECKED):
            switch0_checked_event(event_struct)
        else:
            switch0_unchecked_event(event_struct)
    return

def slider0_event_handler(event_struct):
    global page0, led0, switch0, slider0, label0, brightness
    event = event_struct.code
    if event == lv.EVENT.VALUE_CHANGED and True:
        slider0_value_changed_event(event_struct)
    return

def setup():
    global page0, led0, switch0, slider0, label0, brightness
    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    led0 = m5ui.M5LED(x=135, y=14, size=50, color=0x00FF00, on=True, parent=page0)
    switch0 = m5ui.M5Switch(
        x=110,
        y=159,
        w=100,
        h=40,
        bg_c=0xE7E3E7,
        bg_c_checked=0x2196F3,
        circle_c=0xFFFFFF,
        parent=page0,
    )
    slider0 = m5ui.M5Slider(
        x=20,
        y=118,
        w=280,
        h=16,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=25,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    label0 = m5ui.M5Label(
        "Brightness: 0%",
        x=99,
        y=85,
        text_c=0x2193F3,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    switch0.add_event_cb(switch0_event_handler, lv.EVENT.ALL, None)
    slider0.add_event_cb(slider0_event_handler, lv.EVENT.ALL, None)
    page0.screen_load()
    led0.off()
    brightness = 0
    slider0.set_value(0, True)
    led0.align_to(page0, lv.ALIGN.TOP_MID, 0, 5)
    label0.align_to(slider0, lv.ALIGN.CENTER, 0, -25)
    led0.set_brightness(80)
    print(led0.get_brightness())

def loop():
    global page0, led0, switch0, slider0, label0, brightness
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None.

## **API**

#### M5LED

## M5LED
Create a LED object.

:param int x: The x position of the LED.
:param int y: The y position of the LED.
:param int size: The size (width and height) of the LED.
:param int color: The color of the LED in RGB888 format.
:param bool on: Initial state of the LED (True for ON, False for OFF).
:param lv.obj parent: The parent object to attach the LED to. If not specified, the LED will be attached to the default screen.

UiFlow2 Code Block:

    None

MicroPython Code Block:

    .. code-block:: python

        from m5ui import M5Led
        import lvgl as lv

        m5ui.init()
        led_0 = M5Led(x=50, y=50, size=50, color=0x00FF00, on=True, parent=page0)

### `set_color`

### `set_brightness`
Set the brightness of the LED.

:param int brightness: Brightness level (0-100). Will be mapped to 80-255 internally.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        led_0.set_brightness(50)  # Set brightness to 50%

### `get_brightness`
Get the brightness of the LED.

:return: Brightness level (0-100).
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        brightness = led_0.get_brightness()

<!-- .. py:method:: on() -->

        Turn on the LED.

        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                led_0.on()

<!-- .. py:method:: off() -->

        Turn off the LED.

        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                led_0.off()

<!-- .. py:method:: toggle() -->

        Toggle the state of a LED.

        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                led_0.toggle()

<!-- .. py:method:: set_color(color) -->

        Set the color of the LED.

        :param int color: The color of the LED (RGB888 format).
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                led_0.set_color(color)

<!-- .. py:method:: set_pos(x, y) -->

        Set the position of the LED.

        :param int x: The x position of the LED.
        :param int y: The y position of the LED.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                led_0.set_pos(x, y)

<!-- .. py:method:: set_x(x) -->

        Set the x position of the LED.

        :param int x: The x position of the LED.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                led_0.set_x(x)

<!-- .. py:method:: set_y(y) -->

        Set the y position of the LED.

        :param int y: The y position of the LED.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                led_0.set_y(y)

<!-- .. py:method:: get_x() -->

        Get the x position of the LED.

        :return: The x position of the LED.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                x = led_0.get_x()

<!-- .. py:method:: get_y() -->

        Get the y position of the LED.

        :return: The y position of the LED.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                y = led_0.get_y()

<!-- .. py:method:: set_size(width, height) -->

        Set the size of the LED.

        :param int width: The width of the LED.
        :param int height: The height of the LED.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                led_0.set_size(width, height)

<!-- .. py:method:: set_width(width) -->

        Set the width of the LED.

        :param int width: The width of the LED.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                led_0.set_width(width)

<!-- .. py:method:: set_height(height) -->

        Set the height of the LED.

        :param int height: The height of the LED.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                led_0.set_height(height)

<!-- .. py:method:: align_to(obj, align, x, y) -->

        Align the LED relative to another object.

        :param obj: The reference object (e.g. page0).
        :param int align: Alignment option (see lv.ALIGN constants below).
        :param int x: X offset after alignment.
        :param int y: Y offset after alignment.
        :return: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                led_0.align_to(page0, lv.ALIGN.CENTER, 0, 0)

<!-- .. py:data:: lv.ALIGN -->

        Alignment options for positioning objects.

        - lv.ALIGN.DEFAULT
        - lv.ALIGN.TOP_LEFT
        - lv.ALIGN.TOP_MID
        - lv.ALIGN.TOP_RIGHT
        - lv.ALIGN.BOTTOM_LEFT
        - lv.ALIGN.BOTTOM_MID
        - lv.ALIGN.BOTTOM_RIGHT
        - lv.ALIGN.LEFT_MID
        - lv.ALIGN.RIGHT_MID
        - lv.ALIGN.CENTER
        - lv.ALIGN.OUT_TOP_LEFT
        - lv.ALIGN.OUT_TOP_MID
        - lv.ALIGN.OUT_TOP_RIGHT
        - lv.ALIGN.OUT_BOTTOM_LEFT
        - lv.ALIGN.OUT_BOTTOM_MID
        - lv.ALIGN.OUT_BOTTOM_RIGHT
        - lv.ALIGN.OUT_LEFT_TOP
        - lv.ALIGN.OUT_LEFT_MID
        - lv.ALIGN.OUT_LEFT_BOTTOM
        - lv.ALIGN.OUT_RIGHT_TOP
        - lv.ALIGN.OUT_RIGHT_MID
        - lv.ALIGN.OUT_RIGHT_BOTTOM
