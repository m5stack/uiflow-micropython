# Servo Kit 360°

This is the driver library of Servo 360 Unit, which is used to control the rotation speed and direction of the servo.

Support the following products:

    |Servo Kit 360°|

## MicroPython Example

#### Control servo rotation

This example controls the servo rotation direction and speed.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from unit import Servo360Unit

page0 = None
label0 = None
button0 = None
slider0 = None
button1 = None
button2 = None
servo360_0 = None

def button0_short_clicked_event(event_struct):
    global page0, label0, button0, slider0, button1, button2, servo360_0
    servo360_0.clockwise(slider0.get_value())

def button1_short_clicked_event(event_struct):
    global page0, label0, button0, slider0, button1, button2, servo360_0
    servo360_0.stop()

def button2_short_clicked_event(event_struct):
    global page0, label0, button0, slider0, button1, button2, servo360_0
    servo360_0.counterclockwise(slider0.get_value())

def button0_event_handler(event_struct):
    global page0, label0, button0, slider0, button1, button2, servo360_0
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button0_short_clicked_event(event_struct)
    return

def button1_event_handler(event_struct):
    global page0, label0, button0, slider0, button1, button2, servo360_0
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button1_short_clicked_event(event_struct)
    return

def button2_event_handler(event_struct):
    global page0, label0, button0, slider0, button1, button2, servo360_0
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button2_short_clicked_event(event_struct)
    return

def setup():
    global page0, label0, button0, slider0, button1, button2, servo360_0

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label0 = m5ui.M5Label(
        "speed:",
        x=136,
        y=77,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    button0 = m5ui.M5Button(
        text="CW",
        x=11,
        y=202,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    slider0 = m5ui.M5Slider(
        x=69,
        y=113,
        w=180,
        h=14,
        mode=lv.slider.MODE.NORMAL,
        min_value=0,
        max_value=100,
        value=50,
        bg_c=0x2193F3,
        color=0x2193F3,
        parent=page0,
    )
    button1 = m5ui.M5Button(
        text="stop",
        x=131,
        y=202,
        bg_c=0xF32121,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    button2 = m5ui.M5Button(
        text="CCW",
        x=245,
        y=202,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)
    button1.add_event_cb(button1_event_handler, lv.EVENT.ALL, None)
    button2.add_event_cb(button2_event_handler, lv.EVENT.ALL, None)

    page0.screen_load()
    servo360_0 = Servo360Unit((1, 2))
    servo360_0.stop()

def loop():
    global page0, label0, button0, slider0, button1, button2, servo360_0
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

## **API**

#### Servo360Unit

## `Servo360Unit`
Control a 360-degree continuous rotation servo motor.

> Note: For Servo Kit 360°, the duty cycle microseconds count controls rotation
> speed and direction: **count_low** corresponds to maximum
> clockwise speed, **count_high** to maximum counterclockwise speed, and
> the **midpoint** value indicates stop. Values in
> **count_low** ~ **midpoint** rotate clockwise
> (smaller values = faster speed), while values in
> **midpoint** ~ **count_high** rotate counterclockwise
> (larger values = faster speed). **midpoint** controls the stop position.
- Parameter `port`: The port the servo is connected to.
- Type of `port`: tuple
- Parameter `pin` (`int`): The pin the servo is connected to (if not using a port).
- Parameter `freq` (`int`): The PWM frequency. Default is 50Hz.
- Parameter `count_low` (`int`): The duty cycle microseconds count for the lowest range. Default is 500.
- Parameter `count_high` (`int`): The duty cycle microseconds count for the highest range. Default is 2500.

```python
from unit import Servo360Unit

servo_0 = Servo360Unit((33, 32)) # Adjust the port as needed
servo_1 = Servo360Unit(None, pin=15)  # Directly specify the pin
```

### `clockwise`
Rotate the servo clockwise at a specified speed.

- Parameter `speed` (`int`): Speed percentage (0 to 100).
- Parameter `wait` (`bool`): Whether to wait for the operation to complete.

```python
servo_0.clockwise(50)  # Rotate clockwise at 50% speed
```

### `counterclockwise`
Rotate the servo counterclockwise at a specified speed.

- Parameter `speed` (`int`): Speed percentage (0 to 100).
- Parameter `wait` (`bool`): Whether to wait for the operation to complete.

```python
servo_0.counterclockwise(50)  # Rotate counterclockwise at 50% speed
```

### `stop`
Stop the servo rotation.

- Parameter `wait` (`bool`): Whether to wait for the operation to complete.

```python
servo_0.stop()  # Stop the servo
```
