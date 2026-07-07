#######
###### DualKey

<!-- .. include:: ../refs/controllers.dualkey.ref -->

Support the following products:

    |DualKey|

## UiFlow2 Example

#### Button LED Control

Open the |dualkey_button_led_example.m5f2| project in UiFlow2.

This example demonstrates button callback functions to toggle RGB LEDs. When the left button (BtnA) is clicked, it toggles the left RGB LED (LED 0). When the right button (BtnB) is clicked, it toggles the right RGB LED (LED 1).

UiFlow2 Code Block:

Example output:

    None

#### Power Detection

Open the |dualkey_power_detection_example.m5f2| project in UiFlow2.

This example demonstrates battery voltage monitoring and switch position detection. It reads the switch position (left/middle/right) and displays corresponding RGB LED colors, while also periodically reading and displaying the battery voltage in millivolts.

UiFlow2 Code Block:

Example output:

    None

#### USB Mouse

Open the |dualkey_usb_mouse_example.m5f2| project in UiFlow2.

This example demonstrates USB HID mouse functionality with button-triggered clicks. When the left button (BtnA) is clicked, it sends a left mouse click and lights up the left RGB LED. When the right button (BtnB) is clicked, it sends a right mouse click and lights up the right RGB LED. The LEDs automatically turn off after 300ms.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Button LED Control

This example demonstrates button callback functions to toggle RGB LEDs. When the left button (BtnA) is clicked, it toggles the left RGB LED (LED 0). When the right button (BtnB) is clicked, it toggles the right RGB LED (LED 1).

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import RGB

rgb = None
led1_state = None
led2_state = None

def btnb_was_clicked_event(state):
    global rgb, led1_state, led2_state
    print("clicke left")
    led1_state = not led1_state
    if led1_state:
        rgb.set_color(0, 0x009900)
    else:
        rgb.set_color(0, 0x000000)

def btna_was_clicked_event(state):
    global rgb, led1_state, led2_state
    print("click right")
    led2_state = not led2_state
    if led2_state:
        rgb.set_color(1, 0x009900)
    else:
        rgb.set_color(1, 0x000000)

def setup():
    global rgb, led1_state, led2_state

    M5.begin()
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)

    rgb = RGB()
    rgb.set_color(0, 0x33CCFF)
    rgb.set_color(1, 0x33CCFF)

def loop():
    global rgb, led1_state, led2_state
    M5.update()

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

    None

#### Power Detection

This example demonstrates battery voltage monitoring and switch position detection. It reads the switch position (left/middle/right) and displays corresponding RGB LED colors, while also periodically reading and displaying the battery voltage in millivolts.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import RGB
from hardware import dualkey
import time

rgb = None
sw_status = None
battery_voltage = None

def setup():
    global rgb, sw_status, battery_voltage
    M5.begin()
    rgb = RGB()
    rgb.set_color(0, 0x000000)
    rgb.set_color(1, 0x000000)

def loop():
    global rgb, sw_status, battery_voltage
    M5.update()
    sw_status = dualkey.get_switch_position()
    if sw_status == 0:
        print("Left")
        rgb.set_color(0, 0x009900)
        rgb.set_color(1, 0x000000)
    elif sw_status == 1:
        print("Middle")
        rgb.set_color(0, 0x000000)
        rgb.set_color(1, 0x000000)
    elif sw_status == 2:
        rgb.set_color(0, 0x000000)
        rgb.set_color(1, 0x009900)
        print("Right")
    battery_voltage = dualkey.get_battery_voltage()
    print((str((str("Battery voltage: ") + str(battery_voltage))) + str("mV")))
    time.sleep_ms(500)

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

    None

#### USB Mouse

This example demonstrates USB HID mouse functionality with button-triggered clicks. When the left button (BtnA) is clicked, it sends a left mouse click and lights up the left RGB LED. When the right button (BtnB) is clicked, it sends a right mouse click and lights up the right RGB LED. The LEDs automatically turn off after 300ms.

<!-- .. note:: When USB mouse is initialized, the USB-CDC REPL may disconnect. You may need to reconnect to the device after running this example. -->

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
from hardware import RGB
from usb.device.mouse import Mouse
import time

rgb = None
mouse = None
click_left = None
click_right = None
last_time = None

def btnb_was_clicked_event(state):
    global rgb, mouse, click_left, click_right, last_time
    print("click left")
    click_left = True

def btna_was_clicked_event(state):
    global rgb, mouse, click_left, click_right, last_time
    print("click right")
    click_right = True

def setup():
    global rgb, mouse, click_left, click_right, last_time

    M5.begin()
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)

    rgb = RGB()
    rgb.set_color(0, 0x3333FF)
    rgb.set_color(1, 0x3333FF)
    mouse = Mouse()

def loop():
    global rgb, mouse, click_left, click_right, last_time
    M5.update()
    if click_left:
        click_left = False
        if mouse.is_open():
            mouse.click_left(True)
            rgb.set_color(0, 0x009900)
            rgb.set_color(1, 0x000000)
            last_time = time.ticks_ms()
    if click_right:
        click_right = False
        if mouse.is_open():
            mouse.click_right(True)
            rgb.set_color(0, 0x000000)
            rgb.set_color(1, 0x009900)
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 300:
        rgb.set_color(0, 0x000000)
        rgb.set_color(1, 0x000000)

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

    None

## **API**

#### class DualKey

<!-- .. class:: hardware.dualkey.DualKey() -->

    DualKey module - voltage and switch detection (singleton).

    The DualKey class is a singleton that provides methods to monitor battery voltage, VBUS voltage, charging status, and switch position.

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from hardware import dualkey

<!-- .. method:: get_battery_voltage() -->

        Get battery voltage.

        :returns: Battery voltage value in millivolts (mV).
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                voltage = dualkey.get_battery_voltage()
                print(f"Battery voltage: {voltage} mV")

<!-- .. method:: get_vbus_voltage() -->

        Get VBUS(USB power) voltage.

        :returns: VBUS voltage value in millivolts (mV).
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                vbus_voltage = dualkey.get_vbus_voltage()
                print(f"VBUS voltage: {vbus_voltage} mV")

<!-- .. method:: is_charging() -->

        Check if the device is charging.

        :returns: Returns `True` if charging, `False` if not charging.
        :rtype: bool

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                if dualkey.is_charging():
                    print("Device is charging")
                else:
                    print("Device is not charging")

<!-- .. method:: get_switch_position() -->

        Get switch position.

        :returns: Switch position value:
            - ``0``: left
            - ``1``: middle
            - ``2``: right
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                position = dualkey.get_switch_position()
                if position == 0:
                    print("Switch position: left")
                elif position == 1:
                    print("Switch position: middle")
                elif position == 2:
                    print("Switch position: right")
