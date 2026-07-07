# Atomic Stepmotor Base

<!-- .. sku: A132 -->

<!-- .. include:: ../refs/base.stepmotor.ref -->

Support the following products:

    |Atomic Stepmotor Base|

## UiFlow2 Example

#### Direction control

Open the |atoms3r_stepmotor_direction_control_example.m5f2| project in UiFlow2.

The example demonstrates motor direction control. Pressing the screen button toggles the rotation direction.

UiFlow2 Code Block:

Example output:

    None

#### Rotate control

Open the |atoms3r_stepmotor_rotate_control_example.m5f2| project in UiFlow2.

The example demonstrates the motor continuously rotating for multiple turns, then reversing for multiple turns, and repeating the cycle after a 2-second pause.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### Direction control

The example demonstrates motor direction control. Pressing the screen button toggles the rotation direction.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomicStepmotorBase
import time

title0 = None
label0 = None
label_vol = None
base_stepmotor = None
direction = None

def btna_cliked_cb(state):
    global title0, label0, label_vol, base_stepmotor, direction
    direction = not direction
    base_stepmotor.set_direction(direction)

def setup():
    global title0, label0, label_vol, base_stepmotor, direction
    M5.begin()
    title0 = Widgets.Title("Steps Ctrl", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("vol:", 5, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_vol = Widgets.Label("12.0V", 43, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_cliked_cb)
    base_stepmotor = AtomicStepmotorBase(5, 7, 6, 38, 39, 8)
    label_vol.setText(str((str((base_stepmotor.get_voltage())) + str("V"))))
    direction = True

def loop():
    global title0, label0, label_vol, base_stepmotor, direction
    M5.update()
    base_stepmotor.step()
    time.sleep_ms(1)

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

#### Rotate control

The example demonstrates the motor continuously rotating for multiple turns, then reversing for multiple turns, and repeating the cycle after a 2-second pause.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import AtomicStepmotorBase
import time

title0 = None
label0 = None
label_vol = None
base_stepmotor = None
step_per_rev = None
microstep = None
rotate_circle = None
total_steps = None

def setup():
    global \
        title0, \
        label0, \
        label_vol, \
        base_stepmotor, \
        step_per_rev, \
        microstep, \
        rotate_circle, \
        total_steps
    M5.begin()
    title0 = Widgets.Title("Steps Ctrl", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("vol:", 5, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_vol = Widgets.Label("12.0V", 43, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    step_per_rev = 200
    microstep = 1 / 2
    rotate_circle = 5
    total_steps = (step_per_rev / microstep) * rotate_circle
    base_stepmotor = AtomicStepmotorBase(5, 7, 6, 38, 39, 8)
    label_vol.setText(str((str((base_stepmotor.get_voltage())) + str("V"))))

def loop():
    global \
        title0, \
        label0, \
        label_vol, \
        base_stepmotor, \
        step_per_rev, \
        microstep, \
        rotate_circle, \
        total_steps
    M5.update()
    print(base_stepmotor.get_voltage())
    base_stepmotor.rotate(total_steps, 1, True)
    time.sleep_ms(100)
    base_stepmotor.rotate(total_steps, 1, False)
    time.sleep_ms(100)
    label_vol.setText(str((str((base_stepmotor.get_voltage())) + str("V"))))
    time.sleep_ms(2000)

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

#### AtomicStepmotorBase

## AtomicStepmotorBase
Create an AtomicStepmotorBase object.

:param int en: Enable pin, used to enable or disable the stepper motor.
:param int dir: Direction pin, used to control the rotation direction of the motor.
:param int stp: Step pin, used for step control of the motor.
:param int flt: Fault pin, used to monitor the motor's fault status.
:param int rst: Reset pin, used to reset the motor driver.
:param int pwr_adc: Power ADC monitoring pin, used to measure the input power supply voltage.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from base import AtomicStepmotorBase

        base_stepmotor = AtomicStepmotorBase(en=5, dir=7, stp=6, flt=38, rst=39, pwr_adc=8)

### `enable`
Enable the stepper motor driver.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_stepmotor.enable()

### `disable`
Disable the stepper motor driver.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_stepmotor.disable()

### `set_direction`
Set direction.

:param bool direction: Rotation direction. True or False.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_stepmotor.set_direction(direction)

### `step`
Move the stepper motor one step.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_stepmotor.step()

### `rotate`
Rotate the stepper motor for a specified number of steps.

:param int steps: Number of steps to rotate.
:param int delay_ms: Delay between steps (in milliseconds), default is 0ms.
:param bool direction: Rotation direction (True or False).

The actual rotation direction (clockwise or counterclockwise) depends on the motor wiring.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_stepmotor.rotate(steps, delay_ms, direction)

### `stop`
Stop motor.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_stepmotor.stop()

### `get_status`
Get motor driver status.

:returns: Returns True if the driver is operating normally, or False if a fault is detected.
:rtype: bool

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_stepmotor.get_status()

### `reset`
Reset the stepper motor driver.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_stepmotor.reset()

### `get_voltage`
Get voltage.

:returns: The driver input voltage. unit: V
:rtype: float

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        base_stepmotor.get_voltage()
