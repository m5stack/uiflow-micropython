# Atomic Stepmotor Base

Support the following products:

    Atomic Stepmotor Base

## MicroPython Example

#### Direction control

The example demonstrates motor direction control. Pressing the screen button toggles the rotation direction.

```python
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

#### Rotate control

The example demonstrates the motor continuously rotating for multiple turns, then reversing for multiple turns, and repeating the cycle after a 2-second pause.

```python
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

## **API**

#### AtomicStepmotorBase

## `AtomicStepmotorBase`
Create an AtomicStepmotorBase object.

- Parameter `en` (`int`): Enable pin, used to enable or disable the stepper motor.
- Parameter `dir` (`int`): Direction pin, used to control the rotation direction of the motor.
- Parameter `stp` (`int`): Step pin, used for step control of the motor.
- Parameter `flt` (`int`): Fault pin, used to monitor the motor's fault status.
- Parameter `rst` (`int`): Reset pin, used to reset the motor driver.
- Parameter `pwr_adc` (`int`): Power ADC monitoring pin, used to measure the input power supply voltage.

```python
from base import AtomicStepmotorBase

base_stepmotor = AtomicStepmotorBase(en=5, dir=7, stp=6, flt=38, rst=39, pwr_adc=8)
```

### `enable`
Enable the stepper motor driver.

```python
base_stepmotor.enable()
```

### `disable`
Disable the stepper motor driver.

```python
base_stepmotor.disable()
```

### `set_direction`
Set direction.

- Parameter `direction` (`bool`): Rotation direction. True or False.

```python
base_stepmotor.set_direction(direction)
```

### `step`
Move the stepper motor one step.

```python
base_stepmotor.step()
```

### `rotate`
Rotate the stepper motor for a specified number of steps.

- Parameter `steps` (`int`): Number of steps to rotate.
- Parameter `delay_ms` (`int`): Delay between steps (in milliseconds), default is 0ms.
- Parameter `direction` (`bool`): Rotation direction (True or False).

The actual rotation direction (clockwise or counterclockwise) depends on the motor wiring.

```python
base_stepmotor.rotate(steps, delay_ms, direction)
```

### `stop`
Stop motor.

```python
base_stepmotor.stop()
```

### `get_status`
Get motor driver status.

- Returns: Returns True if the driver is operating normally, or False if a fault is detected.
- Return type: bool

```python
base_stepmotor.get_status()
```

### `reset`
Reset the stepper motor driver.

```python
base_stepmotor.reset()
```

### `get_voltage`
Get voltage.

- Returns: The driver input voltage. unit: V
- Return type: float

```python
base_stepmotor.get_voltage()
```
