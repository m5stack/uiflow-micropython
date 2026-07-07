#########
###### StackChan

<!-- .. include:: ../refs/controllers.stackchan.ref -->

Support the following products:

    |StackChan|

## UiFlow2 Example

#### Servo zero calibration

<!-- .. NOTE:: -->
   Mechanical assembly varies between units. After flashing new firmware, calibrate the servo zero reference manually.

Open the |stackchan_servo_zero_calibrate.m5f2| project in UiFlow2.

#. Run the program.
#. Move the head by hand: on **X**, align the display with the base orientation; on **Y**, set the display perpendicular to the base.
#. Tap **Save** button.

UiFlow2 Code Block:

Example output:

    None

#### Servo angle read

Open the |stackchan_servo_read_example.m5f2| project in UiFlow2.

This example demonstrates reading X and Y servo angles in degrees with torque disabled so the head can move freely.

<!-- .. NOTE:: -->
   **Torque on** holds the last target and resists moving by hand. **Torque off** lets you pose the head freely while readings update—handy for checking calibration.

UiFlow2 Code Block:

Example output:

    None

#### Servo control

Open the |stackchan_servo_control_example.m5f2| project in UiFlow2.

This example demonstrates moving the servos to commanded positions and driving the X servo in PWM mode using ``set_servo_angle`` and ``set_servo_x_pwm``.

UiFlow2 Code Block:

Example output:

    None

#### Face tracking

Open the |stackchan_face_tracking_example.m5f2| project in UiFlow2.

This demo implements face tracking.

UiFlow2 Code Block:

Example output:

    None

#### Servo power info

Open the |stackchan_servo_power_example.m5f2| project in UiFlow2.

This example demonstrates read and display servo power information.

UiFlow2 Code Block:

Example output:

    None

#### Touch & RGB

Open the |stackchan_tp_rgb_example.m5f2| project in UiFlow2.

This example demonstrates mapping touch zones to RGB strip colours (three logical touch points on two strips).

UiFlow2 Code Block:

Example output:

    None

#### NFC

Open the |stackchan_nfc_detect_example.m5f2| project in UiFlow2.

This example demonstrates detecting NFC tags and displaying UID and tag type on screen.
For the full **NFC Unit** API reference (``detect``, read/write, tag types, etc.), see `NFC Unit <../unit/nfc.html>`__.

UiFlow2 Code Block:

Example output:

    None

#### Infrared (IR)

Open the |stackchan_ir_tx_rx_example.m5f2| project in UiFlow2.

This example demonstrates infrared transmit and receive in NEC style.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Servo zero calibration

<!-- .. NOTE:: -->
   Mechanical assembly varies between units. After flashing new firmware, calibrate the servo zero reference manually.

#. Run the program.
#. Move the head by hand: on **X**, align the display with the base orientation; on **Y**, set the display perpendicular to the base.
#. Tap **Save** button.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time
from hardware.stackchan import StackChan

page0 = None
label_title = None
button_save = None
label_angle_x = None
label_angle_y = None
label_tip = None
stackchan = None
x_angle = None
y_angle = None
last_time = None

def button_save_short_clicked_event(event_struct):
    global \
        page0, \
        label_title, \
        button_save, \
        label_angle_x, \
        label_angle_y, \
        label_tip, \
        stackchan, \
        x_angle, \
        y_angle, \
        last_time
    stackchan.set_servo_zero()
    label_tip.set_text(str("Tip: Calibration success"))
    Speaker.tone(1000, 100)

def button_save_event_handler(event_struct):
    global \
        page0, \
        label_title, \
        button_save, \
        label_angle_x, \
        label_angle_y, \
        label_tip, \
        stackchan, \
        x_angle, \
        y_angle, \
        last_time
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button_save_short_clicked_event(event_struct)
    return

def setup():
    global \
        page0, \
        label_title, \
        button_save, \
        label_angle_x, \
        label_angle_y, \
        label_tip, \
        stackchan, \
        x_angle, \
        y_angle, \
        last_time

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "Servo Calibration",
        x=55,
        y=5,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    button_save = m5ui.M5Button(
        text="Save",
        x=128,
        y=195,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    label_angle_x = m5ui.M5Label(
        "X-Axis Servo Angle:",
        x=10,
        y=130,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_angle_y = m5ui.M5Label(
        "Y-Axis Servo Angle:",
        x=8,
        y=160,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    label_tip = m5ui.M5Label(
        "Tip:Move by hand, tap Save.",
        x=33,
        y=70,
        text_c=0xD2E711,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )

    button_save.add_event_cb(button_save_event_handler, lv.EVENT.ALL, None)

    stackchan = StackChan(i2c=1, uart=1)
    page0.screen_load()
    stackchan.set_servo_power(enable=True)
    stackchan.set_servo_torque(stackchan.SERVO_ID_X, enable=False)
    stackchan.set_servo_torque(stackchan.SERVO_ID_Y, enable=False)
    Speaker.begin()
    Speaker.setVolumePercentage(0.6)
    Speaker.tone(1000, 100)

def loop():
    global \
        page0, \
        label_title, \
        button_save, \
        label_angle_x, \
        label_angle_y, \
        label_tip, \
        stackchan, \
        x_angle, \
        y_angle, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        x_angle = stackchan.get_servo_angle(stackchan.SERVO_ID_X)
        y_angle = stackchan.get_servo_angle(stackchan.SERVO_ID_Y)
        label_angle_x.set_text(str((str("X-Axis Servo Angle:") + str(x_angle))))
        label_angle_y.set_text(str((str("Y-Axis Servo Angle:") + str(y_angle))))

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

    None

#### Servo angle read

This example demonstrates reading X and Y servo angles in degrees with torque disabled so the head can move freely.

<!-- .. NOTE:: -->
   **Torque on** holds the last target and resists moving by hand. **Torque off** lets you pose the head freely while readings update—handy for checking calibration.

MicroPython Code Block:

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time
from hardware.stackchan import StackChan

page0 = None
label_title = None
label_agnle_x = None
label_angle_y = None
stackchan = None
last_time = None
x_angle = None
y_angle = None

def setup():
    global page0, label_title, label_agnle_x, label_angle_y, stackchan, last_time, x_angle, y_angle

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "Servo Read Example",
        x=34,
        y=10,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_agnle_x = m5ui.M5Label(
        "X-Axis Servo Angle:",
        x=10,
        y=80,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_angle_y = m5ui.M5Label(
        "Y-Axis Servo Angle:",
        x=10,
        y=125,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    stackchan = StackChan(i2c=1, uart=1)
    page0.screen_load()
    stackchan.set_servo_power(enable=True)
    stackchan.set_servo_torque(stackchan.SERVO_ID_X, enable=False)
    stackchan.set_servo_torque(stackchan.SERVO_ID_Y, enable=False)

def loop():
    global page0, label_title, label_agnle_x, label_angle_y, stackchan, last_time, x_angle, y_angle
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        x_angle = stackchan.get_servo_angle(stackchan.SERVO_ID_X)
        y_angle = stackchan.get_servo_angle(stackchan.SERVO_ID_Y)
        label_agnle_x.set_text(str((str("X-Axis Servo Angle: ") + str(x_angle))))
        label_angle_y.set_text(str((str("Y-Axis Servo Angle: ") + str(y_angle))))

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

    None

#### Servo control

This example demonstrates moving the servos to commanded positions and driving the X servo in PWM mode using ``set_servo_angle`` and ``set_servo_x_pwm``.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time
from hardware.stackchan import StackChan

page0 = None
label_title = None
label_status = None
stackchan = None

def setup():
    global page0, label_title, label_status, stackchan

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "Servo Control Example",
        x=20,
        y=5,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_status = m5ui.M5Label(
        "--",
        x=153,
        y=115,
        text_c=0x0DC9F4,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )

    stackchan = StackChan(i2c=1, uart=1)
    page0.screen_load()
    Speaker.begin()
    Speaker.setVolumePercentage(0.5)
    stackchan.set_servo_power(enable=True)
    stackchan.set_servo_torque(stackchan.SERVO_ID_X, enable=True)
    stackchan.set_servo_torque(stackchan.SERVO_ID_X, enable=True)
    stackchan.set_servo_angle(stackchan.SERVO_ID_X, 0, 1000, 0)
    stackchan.set_servo_angle(stackchan.SERVO_ID_Y, 45, 1000, 0)
    Speaker.tone(678, 300)
    time.sleep_ms(2000)
    label_status.set_text(str("Rotate counterclockwise"))
    label_status.align_to(page0, lv.ALIGN.CENTER, 0, 0)
    stackchan.set_servo_x_pwm(-50)
    time.sleep_ms(3000)
    label_status.set_text(str("Rotate clockwise"))
    label_status.align_to(page0, lv.ALIGN.CENTER, 0, 0)
    stackchan.set_servo_x_pwm(50)
    time.sleep_ms(3000)
    label_status.set_text(str("Go back to center"))
    label_status.align_to(page0, lv.ALIGN.CENTER, 0, 0)
    stackchan.set_servo_angle(stackchan.SERVO_ID_X, 0, 1000, 0)

def loop():
    global page0, label_title, label_status, stackchan
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

    None

#### Face tracking

This example implements face tracking.

MicroPython Code Block:

```python
import os, sys, io
import M5
from M5 import *
import camera
import dl
import image
from hardware.stackchan import StackChan

stackchan = None

import math

img = None
dl_detection_result = None
dl_detector = None
lost_frame = None
res = None
bbox = None
f_x = None
f_y = None
neutral = None
SMOOTH = None
f_w = None
DEADZONE_NORM = None
f_h = None
Y_NEUTRAL = None
f_cx = None
img_cx = None
f_cy = None
img_cy = None
ex = None
angle_x = None
ey = None
angle_y = None
x_target = None
y_target = None

def setup():
    global \
        stackchan, \
        img, \
        dl_detection_result, \
        dl_detector, \
        lost_frame, \
        res, \
        bbox, \
        f_x, \
        f_y, \
        neutral, \
        SMOOTH, \
        f_w, \
        DEADZONE_NORM, \
        f_h, \
        Y_NEUTRAL, \
        f_cx, \
        img_cx, \
        f_cy, \
        img_cy, \
        ex, \
        angle_x, \
        ey, \
        angle_y, \
        x_target, \
        y_target

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)

    stackchan = StackChan(i2c=1, uart=1)
    camera.init(pixformat=camera.RGB565, framesize=camera.QVGA)
    dl_detector = dl.ObjectDetector(dl.model.HUMAN_FACE_DETECT)
    stackchan.set_servo_power(enable=True)
    stackchan.set_servo_torque(stackchan.SERVO_ID_X, enable=True)
    stackchan.set_servo_torque(stackchan.SERVO_ID_Y, enable=True)
    stackchan.set_servo_angle(stackchan.SERVO_ID_X, 0, 0, 0)
    stackchan.set_servo_angle(stackchan.SERVO_ID_Y, 45, 0, 0)
    SMOOTH = 0.1
    DEADZONE_NORM = 0.06
    Y_NEUTRAL = 45
    img_cx = 160
    img_cy = 120
    angle_x = 0
    angle_y = Y_NEUTRAL
    neutral = True

def loop():
    global \
        stackchan, \
        img, \
        dl_detection_result, \
        dl_detector, \
        lost_frame, \
        res, \
        bbox, \
        f_x, \
        f_y, \
        neutral, \
        SMOOTH, \
        f_w, \
        DEADZONE_NORM, \
        f_h, \
        Y_NEUTRAL, \
        f_cx, \
        img_cx, \
        f_cy, \
        img_cy, \
        ex, \
        angle_x, \
        ey, \
        angle_y, \
        x_target, \
        y_target
    M5.update()
    img = camera.snapshot()
    dl_detection_result = dl_detector.infer(img)
    if dl_detection_result:
        lost_frame = 0
        res = dl_detection_result[0]
        bbox = res.bbox()
        f_x = res.x()
        f_y = res.y()
        f_w = res.w()
        f_h = res.h()
        f_cx = int(f_x + f_w * 0.5)
        f_cy = int(f_y + f_h * 0.5)
        ex = (f_cx - img_cx) / img_cx
        ey = (f_cy - img_cy) / img_cy
        if math.fabs(ex) < DEADZONE_NORM:
            ex = 0
        if math.fabs(ey) < DEADZONE_NORM:
            ey = 0
        x_target = min(max(ex * -135, -135), 135)
        y_target = min(max(Y_NEUTRAL - Y_NEUTRAL * ey, 0), 90)
        angle_x = angle_x + SMOOTH * (x_target - angle_x)
        angle_y = angle_y + SMOOTH * (y_target - angle_y)
        stackchan.set_servo_angle(stackchan.SERVO_ID_X, angle_x, 100, 0)
        stackchan.set_servo_angle(stackchan.SERVO_ID_Y, angle_y, 100, 0)
        neutral = False
        lost_frame = 0
        img.draw_rectangle(f_x, f_y, f_w, f_h, color=0x6600CC, thickness=3, fill=False)
    else:
        lost_frame = (lost_frame if isinstance(lost_frame, (int, float)) else 0) + 1
        if lost_frame > 20 and not neutral:
            stackchan.set_servo_angle(stackchan.SERVO_ID_X, 0, 1000, 0)
            stackchan.set_servo_angle(stackchan.SERVO_ID_Y, 45, 1000, 0)
            neutral = True
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

Example output:

    None

#### Servo power info

This example demonstrates read and display servo power information.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time
from hardware.stackchan import StackChan

page0 = None
label_title = None
label_voltage = None
label_current = None
label_power = None
stackchan = None
last_time = None
volatge = None
current = None
power = None

def setup():
    global \
        page0, \
        label_title, \
        label_voltage, \
        label_current, \
        label_power, \
        stackchan, \
        last_time, \
        volatge, \
        current, \
        power

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "Servo Power Info",
        x=56,
        y=5,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_voltage = m5ui.M5Label(
        "Voltage:",
        x=10,
        y=80,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_current = m5ui.M5Label(
        "Current:",
        x=10,
        y=115,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_power = m5ui.M5Label(
        "Power:",
        x=25,
        y=150,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    stackchan = StackChan(i2c=1, uart=1)
    page0.screen_load()

def loop():
    global \
        page0, \
        label_title, \
        label_voltage, \
        label_current, \
        label_power, \
        stackchan, \
        last_time, \
        volatge, \
        current, \
        power
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 200:
        last_time = time.ticks_ms()
        volatge = stackchan.get_battery_voltage()
        current = stackchan.get_battery_current()
        power = stackchan.get_battery_power()
        label_voltage.set_text(str((str("Voltage: ") + str((str(volatge) + str(" V"))))))
        label_current.set_text(str((str("Current: ") + str((str(current) + str(" A"))))))
        label_power.set_text(str((str("Power: ") + str((str(power) + str(" W"))))))

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

    None

#### Touch & RGB

This example demonstrates mapping touch zones to RGB strip colours (three logical touch points on two strips).

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time
from hardware.stackchan import StackChan

page0 = None
label_title = None
stackchan = None
tp = None
tp1 = None
last_time = None
tp2 = None
tp3 = None

def setup():
    global page0, label_title, stackchan, tp, tp1, last_time, tp2, tp3

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "TP & RGB Strip Example",
        x=13,
        y=10,
        text_c=0x0DC9F4,
        bg_c=0x000000,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    stackchan = StackChan(i2c=1, uart=1)
    page0.screen_load()
    last_time = [0, 0, 0]
    Speaker.begin()
    Speaker.setVolumePercentage(0.5)

def loop():
    global page0, label_title, stackchan, tp, tp1, last_time, tp2, tp3
    M5.update()
    tp = stackchan.get_touch()
    tp1 = tp[0]
    tp2 = tp[1]
    tp3 = tp[2]
    if tp1:
        last_time[0] = time.ticks_ms()
        stackchan.set_rgb_color(0, 0, 0x33CC00)
        stackchan.set_rgb_color(0, 1, 0x33CC00)
        stackchan.set_rgb_color(1, 0, 0x33CC00)
        stackchan.set_rgb_color(1, 1, 0x33CC00)
        Speaker.tone(700, 50)
    else:
        if (time.ticks_diff((time.ticks_ms()), (last_time[0]))) > 300:
            stackchan.set_rgb_color(0, 0, 0x000000)
            stackchan.set_rgb_color(0, 1, 0x000000)
            stackchan.set_rgb_color(1, 0, 0x000000)
            stackchan.set_rgb_color(1, 1, 0x000000)
    if tp2:
        last_time[1] = time.ticks_ms()
        stackchan.set_rgb_color(0, 2, 0x00CCCC)
        stackchan.set_rgb_color(0, 3, 0x00CCCC)
        stackchan.set_rgb_color(1, 2, 0x00CCCC)
        stackchan.set_rgb_color(1, 3, 0x00CCCC)
        Speaker.tone(900, 50)
    else:
        if (time.ticks_diff((time.ticks_ms()), (last_time[1]))) > 300:
            stackchan.set_rgb_color(0, 2, 0x000000)
            stackchan.set_rgb_color(0, 3, 0x000000)
            stackchan.set_rgb_color(1, 2, 0x000000)
            stackchan.set_rgb_color(1, 3, 0x000000)
    if tp3:
        last_time[2] = time.ticks_ms()
        stackchan.set_rgb_color(0, 4, 0x000099)
        stackchan.set_rgb_color(0, 5, 0x000099)
        stackchan.set_rgb_color(1, 4, 0x000099)
        stackchan.set_rgb_color(1, 5, 0x000099)
        Speaker.tone(1100, 50)
    else:
        if (time.ticks_diff((time.ticks_ms()), (last_time[2]))) > 300:
            stackchan.set_rgb_color(0, 4, 0x000000)
            stackchan.set_rgb_color(0, 5, 0x000000)
            stackchan.set_rgb_color(1, 4, 0x000000)
            stackchan.set_rgb_color(1, 5, 0x000000)

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

    None

#### NFC

This example demonstrates detecting NFC tags and displaying UID and tag type on screen.
For the full **NFC Unit** API reference (``detect``, read/write, tag types, etc.), see `NFC Unit <../unit/nfc.html>`__.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
import time
from hardware.stackchan import StackChan

page0 = None
label_title = None
label_uid = None
label_type = None
label_size = None
stackchan = None
card_0 = None
card_uid = None
new = None
card_type = None
card_size = None
last_time = None

def setup():
    global \
        page0, \
        label_title, \
        label_uid, \
        label_type, \
        label_size, \
        stackchan, \
        card_0, \
        card_uid, \
        new, \
        card_type, \
        card_size, \
        last_time

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x000000)
    label_title = m5ui.M5Label(
        "NFC Card detect",
        x=58,
        y=5,
        text_c=0x13C2EB,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_uid = m5ui.M5Label(
        "UID:",
        x=18,
        y=70,
        text_c=0xFFFFFF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_type = m5ui.M5Label(
        "Tyep:",
        x=10,
        y=100,
        text_c=0xFFFFFF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_size = m5ui.M5Label(
        "Size:",
        x=16,
        y=130,
        text_c=0xFFFFFF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )

    page0.screen_load()
    stackchan = StackChan(i2c=1, uart=1)
    Speaker.begin()
    Speaker.setVolumePercentage(0.6)

def loop():
    global \
        page0, \
        label_title, \
        label_uid, \
        label_type, \
        label_size, \
        stackchan, \
        card_0, \
        card_uid, \
        new, \
        card_type, \
        card_size, \
        last_time
    M5.update()
    card_0 = stackchan.nfc.detect()
    if card_0:
        card_uid = card_0.uid_str
        card_type = card_0.type_name
        card_size = card_0.user_memory
        label_uid.set_text(str((str("UID: ") + str(card_uid))))
        label_type.set_text(str((str("Tyep: ") + str(card_type))))
        label_size.set_text(str((str("Size: ") + str(card_size))))
        if (time.ticks_diff((time.ticks_ms()), last_time)) >= 3000 or new:
            last_time = time.ticks_ms()
            stackchan.set_rgb_color(0x009900)
            Speaker.tone(1234, 100)
            time.sleep_ms(100)
            stackchan.set_rgb_color(0x000000)
        new = False
    else:
        new = True

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

    None

#### Infrared (IR)

This example demonstrates infrared transmit and receive in NEC style.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2026 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import IR
from hardware.stackchan import StackChan

label_title = None
label_tx_addr = None
label_tx_data = None
label_rx_addr = None
label_rx_data = None
ir = None
stackchan = None
ir_data = None
ir_addr = None
tx_data = None
ir_tx = None
tx_addr = None

def ir_rx_event(_data, _addr, _ctrl):
    global \
        label_title, \
        label_tx_addr, \
        label_tx_data, \
        label_rx_addr, \
        label_rx_data, \
        ir, \
        stackchan, \
        ir_data, \
        ir_addr, \
        tx_data, \
        ir_tx, \
        tx_addr
    ir_data = _data
    ir_addr = _addr
    label_rx_addr.setText(str((str("RX Addr: ") + str(ir_addr))))
    label_rx_data.setText(str((str("RX Data: ") + str(ir_data))))
    Speaker.tone(700, 100)

def btn_pwr_was_clicked_event(state):
    global \
        label_title, \
        label_tx_addr, \
        label_tx_data, \
        label_rx_addr, \
        label_rx_data, \
        ir, \
        stackchan, \
        ir_data, \
        ir_addr, \
        tx_data, \
        ir_tx, \
        tx_addr
    tx_data = (tx_data if isinstance(tx_data, (int, float)) else 0) + 1
    if tx_data > 255:
        tx_data = 0
    ir.tx(tx_addr, tx_data)
    label_tx_addr.setText(str((str("TX Addr: ") + str(tx_addr))))
    label_tx_data.setText(str((str("TX Data: ") + str(tx_data))))

def setup():
    global \
        label_title, \
        label_tx_addr, \
        label_tx_data, \
        label_rx_addr, \
        label_rx_data, \
        ir, \
        stackchan, \
        ir_data, \
        ir_addr, \
        tx_data, \
        ir_tx, \
        tx_addr

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "IR TX & RX Example", 41, 5, 1.0, 0x0DC9F4, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_tx_addr = Widgets.Label(
        "TX Addr:", 9, 59, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_tx_data = Widgets.Label(
        "TX Data:", 170, 59, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_rx_addr = Widgets.Label(
        "RX Addr:", 10, 100, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_rx_data = Widgets.Label(
        "RX Data:", 170, 100, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    BtnPWR.setCallback(type=BtnPWR.CB_TYPE.WAS_CLICKED, cb=btn_pwr_was_clicked_event)

    stackchan = StackChan(i2c=1, uart=1)
    ir = IR()
    ir.rx_cb(ir_rx_event)
    tx_addr = 1
    tx_data = 0
    Speaker.begin()
    Speaker.setVolumePercentage(0.5)
    label_tx_addr.setText(str((str("TX Addr: ") + str(tx_addr))))

def loop():
    global \
        label_title, \
        label_tx_addr, \
        label_tx_data, \
        label_rx_addr, \
        label_rx_data, \
        ir, \
        stackchan, \
        ir_data, \
        ir_addr, \
        tx_data, \
        ir_tx, \
        tx_addr
    M5.update()
    if ir_tx:
        ir_tx = False

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

#### StackChan

<!-- .. class:: hardware.stackchan.StackChan -->

    StackChan board driver: SCS serial servos on UART, RGB and servo power on M5IOE1, Si12T touch, INA226 (battery bus), and onboard NFC (``ST25R3916``) as :class:`unit.nfc.NFCUnit`.

    The class is a **singleton**; always construct with the same ``i2c`` and ``uart`` ids.

    :param int i2c: ``I2C`` peripheral id.
    :param int uart: ``UART`` id for the 1 Mbaud servo bus.

    After init, the instance exposes ``nfc`` (a :class:`unit.nfc.NFCUnit`—see `NFC Unit <../unit/nfc.html>`__ for the complete API), ``touch``, ``i2c``, and low-level ``servo`` (``Scscl`` instance) for advanced use.

    Module constants include ``SERVO_ID_X`` (``1``), ``SERVO_ID_Y`` (``2``) and related limits—also available as class attributes on ``StackChan``.

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from hardware.stackchan import StackChan, SERVO_ID_X, SERVO_ID_Y

            sc = StackChan(i2c=1, uart=1)

<!-- .. method:: set_servo_zero() -->

        Save logical **zero** for both axes into NVS (namespace ``servo``, keys ``zero_pos_1`` / ``zero_pos_2``).

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                sc.set_servo_zero()

<!-- .. method:: set_servo_power(enable=True) -->

        Enable or disable servo rail power via the IO expander.

        :param bool enable: Power on or off.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                sc.set_servo_power(True)

<!-- .. method:: set_servo_torque(servo_id, enable=True) -->

        Enable or disable torque on one servo.

        :param int servo_id: ``SERVO_ID_X`` or ``SERVO_ID_Y``.
        :param bool enable: Torque on or off.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                sc.set_servo_torque(SERVO_ID_X, True)

<!-- .. method:: set_servo_angle(servo_id, angle_deg, time_ms=10, speed=0) -->

        Move the given servo to ``angle_deg`` (degrees). Use about **-135°~135°** for the X axis (``SERVO_ID_X`` / pan) and **0°~90°** for the Y axis (``SERVO_ID_Y`` / tilt).

        :param int servo_id: ``SERVO_ID_X`` or ``SERVO_ID_Y``.
        :param float angle_deg: Target angle in degrees (**-135~135** for X, **0~90** for Y).
        :param int time_ms: Move time (ms) passed to the controller; ``0`` means the time parameter does not take effect.
        :param int speed: User speed **0~100** (mapped to the bus); ``0`` means the speed parameter does not take effect.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                sc.set_servo_angle(SERVO_ID_X, 0.0, 500, 0)
                sc.set_servo_angle(SERVO_ID_X, 0.0, 0, 50)

<!-- .. method:: get_servo_angle(servo_id) -->

        Read the servo angle in degrees.

        :param int servo_id: ``SERVO_ID_X`` or ``SERVO_ID_Y``.
        :returns: Angle in degrees, or ``None`` if the read failed.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                deg = sc.get_servo_angle(SERVO_ID_X)

<!-- .. method:: set_servo_x_pwm(value) -->

        Run the **X** servo in PWM mode for continuous rotation. User range is **-100~100**; the sign selects rotation direction, and the magnitude sets drive strength.

        :param int value: Signed PWM strength (clamped). Positive and negative values rotate in opposite directions; ``0`` stops output.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                sc.set_servo_x_pwm(50)

<!-- .. method:: set_rgb_color(*args) -->

        Set RGB LEDs on the strip.

        - One argument: fill all LEDs with ``color``.
        - Two arguments: ``strip`` (``0`` or ``1``) and ``color`` for that logical strip.
        - Three arguments: ``strip``, ``index``, ``color`` for a single LED (strip ``1`` index order matches the driver).

        :returns: ``True`` on success where applicable.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                sc.set_rgb_color(0x00FF00)
                sc.set_rgb_color(0, 0x0000FF)
                sc.set_rgb_color(0, 0, 0xFF0000)

<!-- .. method:: get_rgb_color(strip, index) -->

        Get RGB color of a single LED.

        :param int strip: ``0`` or ``1``.
        :param int index: ``0~5`` per logical strip.
        :returns: ``tuple`` ``(r, g, b)``.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                r, g, b = sc.get_rgb_color(0, 0)

<!-- .. method:: get_touch(index=None) -->

        Read touch state (three logical slots).

        :param int index: If ``None``, return a list of three levels; if ``0``, ``1``, or ``2``, return that slot’s level.
        :returns: ``OUTPUT_NONE``…``OUTPUT_HIGH`` style values, or ``None`` on failure.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                tp = sc.get_touch()
                one = sc.get_touch(0)

<!-- .. method:: get_battery_voltage() -->

        Bus voltage from the INA226 (volts).

        :returns: ``float`` or ``None`` if unavailable.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                v = sc.get_battery_voltage()

<!-- .. method:: get_battery_current() -->

        Current from the INA226 (A).

        :returns: ``float`` or ``None``.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                a = sc.get_battery_current()

<!-- .. method:: get_battery_power() -->

        Power from the INA226 (W), when both voltage and current are valid.

        :returns: ``float`` or ``None``.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                p = sc.get_battery_power()
