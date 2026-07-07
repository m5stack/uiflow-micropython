# USB Module

<!-- .. include:: ../refs/module.usb.ref -->

The USB Module is a module that uses the SPI interface to expand USB functionality, implemented with the MAX3421E.

Support the following products:

|USB Module|

## Micropython Example

<!-- .. note:: Before using the following examples, please check the DIP switches on the module to ensure that the pins used in the example match the DIP switch positions. For specific configurations, please refer to the product manual page. The SPI configuration has been implemented internally, so users do not need to worry about it. -->

###### Input/Output Pin Control

The module exposes 5 IN (input) pins and 5 OUT (output) pins through headers. This example demonstrates controlling the high and low level switching of the output pins, as well as reading and printing the level status of the input pins.

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from module import USBModule
import time

module_usb_0 = None
last_time = None
i = None
last_set_time = None
value = None
state = None
toggle = None

def setup():
    global module_usb_0, last_time, last_set_time, value, state, toggle, i
    M5.begin()
    Widgets.fillScreen(0x222222)
    module_usb_0 = USBModule(pin_cs=1, pin_int=10)
    module_usb_0.write_gpout(0, 0)
    module_usb_0.write_gpout(1, 1)
    module_usb_0.write_gpout(2, 0)
    module_usb_0.write_gpout(3, 1)
    module_usb_0.write_gpout(4, 0)
    state = [0] * 5
    toggle = True

def loop():
    global module_usb_0, last_time, last_set_time, value, state, toggle, i
    M5.update()
    module_usb_0.poll_data()
    if (time.ticks_diff((time.ticks_ms()), last_time)) > 200:
        last_time = time.ticks_ms()
        for i in range(5):
            value = module_usb_0.read_gpin(i)
            state[int((i + 1) - 1)] = value
        print(state)
    if (time.ticks_diff((time.ticks_ms()), last_set_time)) > 1000:
        last_set_time = time.ticks_ms()
        if toggle:
            for i in range(5):
                module_usb_0.write_gpout(i, 1)
        else:
            for i in range(5):
                module_usb_0.write_gpout(i, 0)
        toggle = not toggle

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

###### Mouse

Implementing USB host to capture mouse input

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from module import USBModule

title0 = None
label_x = None
label_y = None
module_usb_0 = None
x = None
y = None
mouse_move = None
dx = None
dy = None

def setup():
    global title0, label_x, label_y, module_usb_0, x, y, mouse_move, dx, dy
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "Module USB Example mouse", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label_x = Widgets.Label("x", 130, 90, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label_y = Widgets.Label("y", 180, 90, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    module_usb_0 = USBModule(pin_cs=1, pin_int=10)
    x = 0
    y = 0

def loop():
    global title0, label_x, label_y, module_usb_0, x, y, mouse_move, dx, dy
    module_usb_0.poll_data()
    if module_usb_0.is_left_btn_pressed():
        print("click left")
    if module_usb_0.is_right_btn_pressed():
        print("click right")
    if module_usb_0.is_middle_btn_pressed():
        print("click middle")
    mouse_move = module_usb_0.read_mouse_move()
    dx = mouse_move[0]
    dy = mouse_move[1]
    if dx != 0 or dy != 0:
        print((str("move: ") + str((str(dx) + str((str(", ") + str(dy)))))))
        x = min(max(x + dx, 0), 320)
        y = min(max(y + dy, 0), 240)
        label_x.setText(str(x))
        label_y.setText(str(y))

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

###### Keyboard

Implementing USB host to capture keyboard input

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from module import USBModule

module_usb_0 = None
modifier = None
indata = None

def setup():
    global module_usb_0, modifier, indata
    M5.begin()
    Widgets.fillScreen(0x222222)
    module_usb_0 = USBModule(pin_cs=1, pin_int=10)

def loop():
    global module_usb_0, modifier, indata
    M5.update()
    module_usb_0.poll_data()
    modifier = module_usb_0.read_kb_modifier()
    if modifier & 0x01:
        print("Left Control pressed")
    if modifier & 0x02:
        print("Left Shift pressed")
    if modifier & 0x04:
        print("Left Alt pressed")
    if modifier & 0x08:
        print("Left GUI pressed")
    if modifier & 0x10:
        print("Right Control pressed")
    if modifier & 0x20:
        print("Right Shift pressed")
    if modifier & 0x40:
        print("Right Alt pressed")
    if modifier & 0x80:
        print("Right GUI pressed")
    indata = module_usb_0.read_kb_input(True)
    if indata:
        print(indata)

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

###### Input/Output Pin Control

<!-- .. only:: builder_html -->

    |cores3_module_usb_gpio_example.m5f2|

###### Mouse

<!-- .. only:: builder_html -->

    |cores3_module_usb_mouse_example.m5f2|

###### Keyboard

<!-- .. only:: builder_html -->

    |cores3_module_usb_kb_example.m5f2|

## class USBModule

## Constructors

<!-- .. class:: USBModule(pin_cs: int = 1, pin_int: int = 10) -->

    :param int pin_cs: (RST) 复位引脚
    :param int pin_irq: (INT) 中断引脚

    UIFLOW2:

<!-- .. method:: poll_data() -->

    poll data

    **Note**: It needs to be called in the main loop

    UIFlow2.0

<!-- .. method:: is_left_btn_pressed() -> bool -->

    Check if the left mouse button is pressed.

    UIFlow2.0

<!-- .. method:: is_right_btn_pressed() -> bool -->

    Check if the right mouse button is pressed.

    UIFlow2.0

<!-- .. method:: is_middle_btn_pressed() -> bool -->

    Check if the middle mouse button is pressed.

    UIFlow2.0

<!-- .. method:: is_forward_btn_pressed() -> bool -->

    Check if the forward mouse button is pressed.

    UIFlow2.0

<!-- .. method:: is_back_btn_pressed() -> bool -->

    Check if the back mouse button is pressed.

    UIFlow2.0

<!-- .. method:: read_mouse_move() -> tuple[int, int] -->

    Read Mouse Cursor Movement

    Returns a tuple (x, y) containing the horizontal displacement x and vertical displacement y of the mouse;
    x range: -127 to 127; 0 indicates no movement, negative values indicate movement to the left, and positive values indicate movement to the right;
    y range: -127 to 127; 0 indicates no movement, negative values indicate movement upward, and positive values indicate movement downward.

    **Example:**

```
```
        move = usb_module.read_mouse_move()
        x = move[0]
        y = move[1]

    UIFlow2.0

<!-- .. method:: read_wheel_move() -> int -->

    Read Mouse Wheel Movement

    Returns a value in the range of -127 to 127, 0 indicates no movement, Positive values indicate forward scrolling, Negative values indicate backward scrolling.

    UIFlow2.0

<!-- .. method:: read_kb_input(convert: bool = True) -> list -->

    Read keyboard input

    - ``convert`` Whether to convert HID Keycode to the corresponding string.

    Returns a list containing keyboard inputs (up to 6 elements, meaning a maximum of 6 key values can be input at once).

    **Example:**

```
```
        res = usb_module.read_kb_input(convert=True)
        # output ['a', 'b', 'Enter']

        res = usb_module.read_kb_input(convert=False)
        # output [0x04, 0x05, 0x28]

    UIFlow2.0

<!-- .. method:: read_kb_modifier() -> int -->

    Read the keyboard modifier keys, namely "Ctrl", "Shift", "Alt", and "Win" keys.

    - ``Return``: The status of the keyboard modifier keys, usually represented by a bit mask to indicate the status of different modifier keys.
        - 0x01: Left Control key
        - 0x02: Left Shift key
        - 0x04: Left Alt key
        - 0x08: Left Windows key (Left GUI)
        - 0x10: Right Control key
        - 0x20: Right Shift key
        - 0x40: Right Alt key
        - 0x80: Right Windows key (Right GUI)

    **Example:**

```
```
        modifier = module_usb.read_kb_modifier()
        if modifier & 0x01:
            print("left ctrl key pressed")

    UIFlow2.0

<!-- .. method:: read_gpin(pin) -> int -->

    Read input pin value

    - ``pin`` pin number
    - ``Return`` 1 represents high level, and 0 represents low level.

    UIFlow2.0

<!-- .. method:: write_gpout(pin, value) -->

    Write output pin value

    - ``pin`` pin number
    - ``Return`` 1 represents high level, and 0 represents low level.

    UIFlow2.0
