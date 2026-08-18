# BaseX Module

BaseX is an M5Stack stackable module with 4 DC motor channels and 2 servo
channels. It communicates with the host via I2C address `0x22`. The onboard
controller handles motor PWM output, motor encoder count, position/speed mode
configuration, and servo output.

Support the following products:

    BaseXModule

## MicroPython Example

#### Servo control

Control two servos by button.

```python
import os, sys, io
import M5
from M5 import *
from module import ModuleBaseX

label_title = None
label_angle1 = None
label_angle2 = None
label_btn1 = None
label_btn2 = None
label_btn3 = None
basex_0 = None
angle1 = None
agnle2 = None

def btna_was_clicked_event(state):
    global \
        label_title, \
        label_angle1, \
        label_angle2, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        angle1, \
        agnle2
    angle1 = angle1 + 30
    if angle1 > 180:
        angle1 = 0
    basex_0.set_servo_angle(1, angle1)
    label_angle1.setText(str((str("Servo1 Angle: ") + str(angle1))))

def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_angle1, \
        label_angle2, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        angle1, \
        agnle2
    agnle2 = agnle2 + 30
    if agnle2 > 180:
        agnle2 = 0
    basex_0.set_servo_angle(2, agnle2)
    label_angle2.setText(str((str("Servo2 Angle: ") + str(agnle2))))

def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_angle1, \
        label_angle2, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        angle1, \
        agnle2
    angle1 = 0
    agnle2 = 0
    basex_0.set_servo_angle(1, 0)
    basex_0.set_servo_angle(2, 0)
    label_angle1.setText(str("Servo1 Angle:  0"))
    label_angle2.setText(str("Servo2 Angle:  0"))

def setup():
    global \
        label_title, \
        label_angle1, \
        label_angle2, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        angle1, \
        agnle2

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "BaseX Servo Control", 36, 1, 1.0, 0x12DEEE, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_angle1 = Widgets.Label(
        "Servo1 Angle: --", 20, 70, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_angle2 = Widgets.Label(
        "Servo2 Angle: --", 20, 110, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_btn1 = Widgets.Label(
        "Servo1", 38, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_btn2 = Widgets.Label(
        "Servo2", 124, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_btn3 = Widgets.Label(
        "Reset", 219, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    basex_0 = ModuleBaseX()
    angle1 = 0
    agnle2 = 0
    label_angle1.setText(str("Servo1 Angle:  0"))
    label_angle2.setText(str("Servo2 Angle:  0"))

def loop():
    global \
        label_title, \
        label_angle1, \
        label_angle2, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        angle1, \
        agnle2
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

#### Motor normal control

Set all motors to Normal mode and control PWM duty by button.

```python
import os, sys, io
import M5
from M5 import *
from module import ModuleBaseX

label_title = None
label_speed = None
label_btn1 = None
label_btn2 = None
label_mode = None
label_btn3 = None
basex_0 = None
pwm = None
i = None

def btna_was_clicked_event(state):
    global \
        label_title, \
        label_speed, \
        label_btn1, \
        label_btn2, \
        label_mode, \
        label_btn3, \
        basex_0, \
        pwm, \
        i
    pwm = pwm + 20
    if pwm > 120:
        pwm = 0
    for i in range(4):
        basex_0.set_motor_pwm(i + 1, pwm)

    label_speed.setText(str((str("motor pwm: ") + str(pwm))))

def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_speed, \
        label_btn1, \
        label_btn2, \
        label_mode, \
        label_btn3, \
        basex_0, \
        pwm, \
        i
    pwm = pwm - 20
    if pwm < -120:
        pwm = 0
    for i in range(4):
        basex_0.set_motor_pwm(i + 1, pwm)

    label_speed.setText(str((str("motor pwm: ") + str(pwm))))

def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_speed, \
        label_btn1, \
        label_btn2, \
        label_mode, \
        label_btn3, \
        basex_0, \
        pwm, \
        i
    pwm = 0
    for i in range(4):
        basex_0.set_motor_pwm(i + 1, 0)

    label_speed.setText(str("motor pwm: "))

def setup():
    global \
        label_title, \
        label_speed, \
        label_btn1, \
        label_btn2, \
        label_mode, \
        label_btn3, \
        basex_0, \
        pwm, \
        i

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "BaseX Motor Control", 34, 0, 1.0, 0x12DEEE, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_speed = Widgets.Label(
        "motor pwm: 0", 20, 105, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_btn1 = Widgets.Label("+20", 50, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18)
    label_btn2 = Widgets.Label(
        "-20", 140, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_mode = Widgets.Label(
        "control mode: normal", 20, 70, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_btn3 = Widgets.Label("0", 238, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    basex_0 = ModuleBaseX()
    pwm = 0
    label_speed.setText(str("motor pwm: 0"))
    for i in range(4):
        basex_0.set_motor_mode(i + 1, ModuleBaseX.MOTOR_MODE_NORMAL)
        basex_0.set_motor_pwm(i + 1, 0)

def loop():
    global \
        label_title, \
        label_speed, \
        label_btn1, \
        label_btn2, \
        label_mode, \
        label_btn3, \
        basex_0, \
        pwm, \
        i
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

#### Motor position control

Use position mode to move Motor1 between fixed target positions.

```python
import os, sys, io
import M5
from M5 import *
from module import ModuleBaseX
import time

label_title = None
label_mode = None
label_target = None
label_encoder = None
label_btn1 = None
label_btn2 = None
label_btn3 = None
basex_0 = None

position_target = None

def btna_was_clicked_event(state):
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_encoder, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        position_target
    position_target = 720
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_POSITION)
    basex_0.set_motor_position_pid(1, 3, 1, 15)
    basex_0.set_motor_position_max_speed(1, 80)
    basex_0.set_motor_position_target(1, position_target)
    label_target.setText(str((str("target pos: ") + str(position_target))))

def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_encoder, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        position_target
    position_target = -720
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_POSITION)
    basex_0.set_motor_position_pid(1, 3, 1, 15)
    basex_0.set_motor_position_max_speed(1, 80)
    basex_0.set_motor_position_target(1, position_target)
    label_target.setText(str((str("target pos: ") + str(position_target))))

def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_encoder, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        position_target
    position_target = 0
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_POSITION)
    basex_0.set_motor_position_pid(1, 3, 1, 15)
    basex_0.set_motor_position_max_speed(1, 80)
    basex_0.set_motor_position_target(1, position_target)
    label_target.setText(str((str("target pos: ") + str(position_target))))

def setup():
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_encoder, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        position_target

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "BaseX Position Control", 16, 0, 1.0, 0x12DEEE, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_mode = Widgets.Label(
        "control mode: position", 20, 65, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_target = Widgets.Label(
        "target pos: 0", 20, 105, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_encoder = Widgets.Label(
        "encoder: 0", 20, 145, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_btn1 = Widgets.Label(
        "+720", 45, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_btn2 = Widgets.Label(
        "-720", 136, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_btn3 = Widgets.Label(
        "Reset", 220, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    basex_0 = ModuleBaseX()
    position_target = 0
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_NORMAL)
    basex_0.set_motor_pwm(1, 0)
    basex_0.set_motor_encoder(1, 0)
    basex_0.set_motor_position_pid(1, 3, 1, 15)
    basex_0.set_motor_position_max_speed(1, 80)
    basex_0.set_motor_position_target(1, 0)
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_POSITION)
    label_target.setText(str("target pos: 0"))
    label_encoder.setText(str("encoder: 0"))

def loop():
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_encoder, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        position_target
    M5.update()
    label_encoder.setText(str((str("encoder: ") + str((basex_0.get_motor_encoder(1))))))
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

#### Motor speed control

Use speed mode to set Motor1 speed target.

```python
import os, sys, io
import M5
from M5 import *
from module import ModuleBaseX
import time

label_title = None
label_mode = None
label_target = None
label_feedback = None
label_btn1 = None
label_btn2 = None
label_btn3 = None
basex_0 = None
speed_target = None

def btna_was_clicked_event(state):
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_feedback, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        speed_target
    speed_target = speed_target + 5
    if speed_target > 20:
        speed_target = 20
    basex_0.set_motor_speed_target(1, speed_target)
    label_target.setText(str((str("target speed: ") + str(speed_target))))

def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_feedback, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        speed_target
    speed_target = speed_target - 5
    if speed_target < -20:
        speed_target = -20
    basex_0.set_motor_speed_target(1, speed_target)
    label_target.setText(str((str("target speed: ") + str(speed_target))))

def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_feedback, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        speed_target
    speed_target = 0
    basex_0.set_motor_speed_target(1, speed_target)
    label_target.setText(str((str("target speed: ") + str(speed_target))))

def setup():
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_feedback, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        speed_target

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "BaseX Speed Control", 34, 0, 1.0, 0x12DEEE, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_mode = Widgets.Label(
        "control mode: speed", 20, 65, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_target = Widgets.Label(
        "target speed: 0", 20, 105, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_feedback = Widgets.Label(
        "speed20ms: --", 20, 145, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_btn1 = Widgets.Label("+5", 55, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18)
    label_btn2 = Widgets.Label("-5", 145, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18)
    label_btn3 = Widgets.Label("0", 245, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18)

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    basex_0 = ModuleBaseX()
    speed_target = 0
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_NORMAL)
    basex_0.set_motor_pwm(1, 0)
    basex_0.set_motor_encoder(1, 0)
    basex_0.set_motor_speed_pid(1, 3, 1, 15)
    basex_0.set_motor_speed_target(1, 0)
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_SPEED)
    label_target.setText(str("target speed: 0"))
    label_feedback.setText(str("speed20ms: --"))

def loop():
    global \
        label_title, \
        label_mode, \
        label_target, \
        label_feedback, \
        label_btn1, \
        label_btn2, \
        label_btn3, \
        basex_0, \
        speed_target
    M5.update()
    label_feedback.setText(str((str("speed20ms: ") + str(basex_0.get_motor_speed_20ms(1)))))
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

#### Read encoder

Display encoder values for four motor channels. Button B clears all encoder
values.

```python
import os, sys, io
import M5
from M5 import *
from module import ModuleBaseX
import time

label_title = None
label_encoder1 = None
label_encoder2 = None
label_encoder3 = None
label_encoder4 = None
label_btn2 = None
basex_0 = None

def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_encoder1, \
        label_encoder2, \
        label_encoder3, \
        label_encoder4, \
        label_btn2, \
        basex_0
    basex_0.set_motor_encoder(1, 0)
    basex_0.set_motor_encoder(2, 0)
    basex_0.set_motor_encoder(3, 0)
    basex_0.set_motor_encoder(4, 0)

def setup():
    global \
        label_title, \
        label_encoder1, \
        label_encoder2, \
        label_encoder3, \
        label_encoder4, \
        label_btn2, \
        basex_0

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "BaseX Encoder", 58, 0, 1.0, 0x12DEEE, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_encoder1 = Widgets.Label(
        "M1 encoder: --", 20, 45, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_encoder2 = Widgets.Label(
        "M2 encoder: --", 20, 75, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_encoder3 = Widgets.Label(
        "M3 encoder: --", 20, 105, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_encoder4 = Widgets.Label(
        "M4 encoder: --", 20, 135, 1.0, 0x1AE179, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_btn2 = Widgets.Label(
        "B: Clear All", 108, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)

    basex_0 = ModuleBaseX()
    basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_NORMAL)
    basex_0.set_motor_pwm(1, 0)
    basex_0.set_motor_mode(2, ModuleBaseX.MOTOR_MODE_NORMAL)
    basex_0.set_motor_pwm(2, 0)
    basex_0.set_motor_mode(3, ModuleBaseX.MOTOR_MODE_NORMAL)
    basex_0.set_motor_pwm(3, 0)
    basex_0.set_motor_mode(4, ModuleBaseX.MOTOR_MODE_NORMAL)
    basex_0.set_motor_pwm(4, 0)
    basex_0.set_motor_encoder(1, 0)
    basex_0.set_motor_encoder(2, 0)
    basex_0.set_motor_encoder(3, 0)
    basex_0.set_motor_encoder(4, 0)

def loop():
    global \
        label_title, \
        label_encoder1, \
        label_encoder2, \
        label_encoder3, \
        label_encoder4, \
        label_btn2, \
        basex_0
    M5.update()
    label_encoder1.setText(str((str("M1 encoder: ") + str((basex_0.get_motor_encoder(1))))))
    label_encoder2.setText(str((str("M2 encoder: ") + str((basex_0.get_motor_encoder(2))))))
    label_encoder3.setText(str((str("M3 encoder: ") + str((basex_0.get_motor_encoder(3))))))
    label_encoder4.setText(str((str("M4 encoder: ") + str((basex_0.get_motor_encoder(4))))))
    time.sleep_ms(200)

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

#### ModuleBaseX

### `class ModuleBaseX()`

    Create a BaseX module object.

```python
from module import ModuleBaseX

basex_0 = ModuleBaseX()
```
### `MOTOR_MODE_NORMAL`

        Normal PWM mode.

### `MOTOR_MODE_POSITION`

        Position control mode.

### `MOTOR_MODE_SPEED`

        Speed target control mode.

### `set_servo_angle(channel, angle)`

        Set servo angle.

        - Parameter `channel` (`int`): Servo channel. Range: 1 ~ 2.
        - Parameter `angle` (`int`): Servo angle. Range: 0 ~ 180.

```python
basex_0.set_servo_angle(1, 90)
```
### `set_servo_pulse(channel, pulse_us)`

        Set servo pulse width.

        - Parameter `channel` (`int`): Servo channel. Range: 1 ~ 2.
        - Parameter `pulse_us` (`int`): Pulse width in microseconds. Range: 500 ~ 2500.

        The servo PWM frequency is 50Hz, with a period of 20ms. The pulse range
        500 ~ 2500us corresponds to about 2.5% ~ 12.5% duty.

```python
basex_0.set_servo_pulse(1, 1500)
```
### `set_motor_pwm(channel, duty)`

        Set motor PWM duty.

        - Parameter `channel` (`int`): Motor channel. Range: 1 ~ 4.
        - Parameter `duty` (`int`): PWM duty. Range: -127 ~ 127.

        The sign indicates direction. `abs(duty)` 0 ~ 127 maps to 0% ~ 100%
        duty.

```python
basex_0.set_motor_pwm(1, 80)
```
### `get_motor_speed_20ms(channel)`

        Get motor speed feedback over 20ms.

        - Parameter `channel` (`int`): Motor channel. Range: 1 ~ 4.
        - Returns: Encoder delta over 20ms.
        - Return type: int

```python
speed = basex_0.get_motor_speed_20ms(1)
```
### `get_motor_encoder(channel)`

        Get motor encoder value.

        - Parameter `channel` (`int`): Motor channel. Range: 1 ~ 4.
        - Returns: Encoder count as signed 32-bit integer.
        - Return type: int

```python
encoder = basex_0.get_motor_encoder(1)
```
### `set_motor_encoder(channel, value)`

        Set motor encoder value.

        - Parameter `channel` (`int`): Motor channel. Range: 1 ~ 4.
        - Parameter `value` (`int`): Encoder count as signed 32-bit integer.

```python
basex_0.set_motor_encoder(1, 0)
```
### `set_motor_mode(channel, mode)`

        Set motor control mode.

        - Parameter `channel` (`int`): Motor channel. Range: 1 ~ 4.
        - Parameter `mode` (`int`): Motor mode. `MOTOR_MODE_NORMAL`,
            `MOTOR_MODE_POSITION` or `MOTOR_MODE_SPEED`.

```python
basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_NORMAL)
```
### `set_motor_position_pid(channel, p=3, i=1, d=15)`

        Set motor position mode PID parameters.

        - Parameter `channel` (`int`): Motor channel. Range: 1 ~ 4.
        - Parameter `p` (`int`): Position P parameter. Default is 3.
        - Parameter `i` (`int`): Position I parameter. Default is 1.
        - Parameter `d` (`int`): Position D parameter. Default is 15.

```python
basex_0.set_motor_position_pid(1)
```
### `set_motor_position_target(channel, position)`

        Set motor position mode target.

        - Parameter `channel` (`int`): Motor channel. Range: 1 ~ 4.
        - Parameter `position` (`int`): Position target as signed 32-bit integer.

```python
basex_0.set_motor_position_target(1, 720)
```
### `set_motor_position_max_speed(channel, speed)`

        Set motor position mode max speed.

        - Parameter `channel` (`int`): Motor channel. Range: 1 ~ 4.
        - Parameter `speed` (`int`): Max speed. Range: -127 ~ 127.

        The sign indicates direction.

```python
basex_0.set_motor_position_max_speed(1, 80)
```
### `set_motor_speed_pid(channel, p=3, i=1, d=15)`

        Set motor speed mode PID parameters.

        - Parameter `channel` (`int`): Motor channel. Range: 1 ~ 4.
        - Parameter `p` (`int`): Speed P parameter. Default is 3.
        - Parameter `i` (`int`): Speed I parameter. Default is 1.
        - Parameter `d` (`int`): Speed D parameter. Default is 15.

```python
basex_0.set_motor_speed_pid(1)
```
### `set_motor_speed_target(channel, speed)`

        Set motor speed mode target.

        - Parameter `channel` (`int`): Motor channel. Range: 1 ~ 4.
        - Parameter `speed` (`int`): Speed target. Range: -20 ~ 20.

        The sign indicates direction. The target controls the feedback value
        returned by `get_motor_speed_20ms`.

```python
basex_0.set_motor_speed_target(1, 20)
```
