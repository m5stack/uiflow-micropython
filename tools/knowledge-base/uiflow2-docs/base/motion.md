# Atomic Motion Base

<!-- .. sku: A090 -->

<!-- .. include:: ../refs/base.motion.ref -->

Atomic Motion Base is a servo and DC motor driver designed specifically for the ATOM series controllers. It integrates an STM32 control chip internally and uses I2C communication for control. Atomic Motion Base provides 4 servo channels and 2 DC motor interfaces, offering convenience for scenarios that require control of multiple servos or motor drivers, such as multi-axis servo robotic arms or small car motor control.

Atomic Motion Base v1.1 adds INA226 to implement current and voltage detection.

Support the following products:

    ================== ==================
    |Motion|           |Motion Base v1.1|
    ================== ==================

## UiFlow2 Example:

#### Motion Base

Open the |atoms3_lite_motion_base_example.m5f2| project in UiFlow2.

This example controls the servo to rotate to a specified angle and sets the motor to rotate.

UiFlow2 Code Block:

Example output:

    None

#### Motion Base v1.1

Open the |atoms3_motion_base_v1.1_example.m5f2| project in UiFlow2.

The example program switches the motor's running speed when the screen button is pressed, and the screen displays the current, voltage, and power.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example:

#### Motion Base

This example controls the servo to rotate to a specified angle and sets the motor to rotate.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import *
from base import Motion

i2c0 = None
motion = None

def setup():
    global i2c0, motion

    M5.begin()
    i2c0 = I2C(0, scl=Pin(39), sda=Pin(38), freq=100000)
    motion = Motion(i2c0, 0x38)
    motion.set_servo_angle(1, 70)
    motion.set_motor_speed(1, 46)
    print(motion.get_servo_angle(1))

def loop():
    global i2c0, motion
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

#### Motion Base v1.1

The example program switches the motor's running speed when the screen button is pressed, and the screen displays the current, voltage, and power.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from base import Motion
import time

label_speed = None
title_e = None
label_vol = None
label_cur = None
label_pow = None
i2c0 = None
motion = None
speed = None
voltage = None
curent = None
last_time = None
power = None

def btnA_wasClicked_event(state):
    global \
        label_speed, \
        title_e, \
        label_vol, \
        label_cur, \
        label_pow, \
        i2c0, \
        motion, \
        speed, \
        voltage, \
        curent, \
        last_time, \
        power
    speed = speed + 20
    if speed > 120:
        speed = 0
    motion.set_motor_speed(1, speed)
    label_speed.setText(str((str("speed: ") + str(speed))))

def setup():
    global \
        label_speed, \
        title_e, \
        label_vol, \
        label_cur, \
        label_pow, \
        i2c0, \
        motion, \
        speed, \
        voltage, \
        curent, \
        last_time, \
        power
    M5.begin()
    label_speed = Widgets.Label("speed：", 5, 27, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    title_e = Widgets.Title("Motor Ctrl", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label_vol = Widgets.Label("vol:", 5, 55, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_cur = Widgets.Label("cur:", 5, 75, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_pow = Widgets.Label("pow:", 5, 95, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)
    i2c0 = I2C(0, scl=Pin(39), sda=Pin(38), freq=100000)
    motion = Motion(i2c0, 0x38)
    last_time = time.ticks_us()
    speed = 0
    label_speed.setText(str((str("speed: ") + str(speed))))

def loop():
    global \
        label_speed, \
        title_e, \
        label_vol, \
        label_cur, \
        label_pow, \
        i2c0, \
        motion, \
        speed, \
        voltage, \
        curent, \
        last_time, \
        power
    M5.update()
    voltage = motion.read_voltage()
    curent = motion.read_current()
    power = motion.read_power()
    label_vol.setText(str((str("vol: ") + str(voltage))))
    label_cur.setText(str((str("cur: ") + str(curent))))
    label_pow.setText(str((str("pow: ") + str(power))))

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

#### Motion

<!-- .. class:: base.motion.Motion(i2c, address=0x38) -->

    Create an Motion object.

    :param I2C i2c: The I2C port to use.
    :param int address: The device address. Default is 0x38.

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from base import Motion
            from machine import I2C

            i2c0 = I2C(0, scl=Pin(39), sda=Pin(38), freq=100000)
            motion = Motion(i2c0, 0x38)

<!-- .. method:: get_servo_angle(ch) -->

        Get the angle of the servo.

        :param int ch: The servo channel. Range: 1~4.
        :returns: Specify the servo angle for the specified channel. Range: 0~180.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                motion.get_servo_angle()

<!-- .. method:: set_servo_angle(ch, angle) -->

        Set the angle of the servo.

        :param int ch: The servo channel. Range: 1~4.
        :param int angle: The servo angle. Range: 0~180.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                motion.set_servo_angle()

<!-- .. method:: get_servo_pulse(ch) -->

        Get the pulse of the servo.

        :param int ch: The servo channel. Range: 1~4.
        :returns: Specify the servo pulse for the specified channel. Range: 500~2500.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                motion.get_servo_pulse()

<!-- .. method:: write_servo_pulse(ch, pulse) -->

        Write the pulse of the servo.

        :param int ch: The servo channel. Range: 1~4.
        :param int pulse: The servo pulse. Range: 500~2500.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                motion.write_servo_pulse()

<!-- .. method:: get_motor_speed(ch) -->

        Get the speed of the motor.

        :param int ch: The motor channel. Range: 1~2.
        :returns: Specify the speed for the specified channel. Range: -127~127.
        :rtype: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                motion.get_motor_speed()

<!-- .. method:: set_motor_speed(ch, speed) -->

        Set motor speed.

        :param int ch: The motor channel. Range: 1~2.
        :param int speed: The motor speed. Range: -127~127.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                motion.set_motor_speed()

<!-- .. method:: read_voltage() -->

        Read voltage (unit: V).

        :returns: The voltage value in volts.
        :rtype: float

<!-- .. note:: -->
            This method is supported only on Motion Base v1.1 and later versions.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                motion.read_voltage()

<!-- .. method:: read_current() -->

        Read current (unit: A).

        :returns: The current value in amperes.
        :rtype: float

<!-- .. note:: -->
            This method is supported only on Motion Base v1.1 and later versions.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                motion.read_current()

<!-- .. method:: read_power() -->

        Read power (unit: W).

        :returns: The power value in watts.
        :rtype: float

<!-- .. note:: -->
            This method is supported only on Motion Base v1.1 and later versions.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                motion.read_power()
