# Atomic HDriver Base

Support the following products:

    Atomic HDriver Base

## MicroPython Example:

#### Motor speed control

The example demonstrates the motor speed changing from low to high, high to low, and then reversing, changing from low to high and high to low.

```python
import os, sys, io
import M5
from M5 import *
from base import AtomicHDriverBase
import time

title0 = None
label0 = None
label1 = None
label_vol = None
label_speed = None
base_hdriver = None
i = None
speed = None

def setup():
    global title0, label0, label1, label_vol, label_speed, base_hdriver, speed, i
    M5.begin()
    title0 = Widgets.Title("Speed Ctrl", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("speed:", 5, 65, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("vol:", 5, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_vol = Widgets.Label("12.0V", 45, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_speed = Widgets.Label("0", 70, 65, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    base_hdriver = AtomicHDriverBase(6, 7, 5, 8, 1000)
    label_vol.setText(str((str((base_hdriver.get_voltage())) + str("V"))))
    speed = 0

def loop():
    global title0, label0, label1, label_vol, label_speed, base_hdriver, speed, i
    M5.update()
    for i in range(50):
        speed = i
        base_hdriver.set_speed(speed)
        label_speed.setText(str(speed))
        time.sleep_ms(40)
    for i in range(50):
        speed = 50 - i
        base_hdriver.set_speed(speed)
        label_speed.setText(str(speed))
        time.sleep_ms(40)
    for i in range(50):
        speed = 1 - i
        base_hdriver.set_speed(speed)
        label_speed.setText(str(speed))
        time.sleep_ms(40)
    for i in range(50):
        speed = i - 50
        base_hdriver.set_speed(speed)
        label_speed.setText(str(speed))
        time.sleep_ms(40)

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

#### AtomicHDriverBase

## `AtomicHDriverBase`
Create an AtomicHDriverBase object.

- Parameter `in1` (`int`): PWM control pin1.
- Parameter `in2` (`int`): PWM control pin2.
- Parameter `fault` (`int`): driver status.
- Parameter `vin` (`int`): driver input voltage detect.
- Parameter `freq` (`int`): The PWM frequency.

```python
from base import AtomicHDriverBase

base_hdriver = AtomicHDriverBase(in1 = 6, in2 = 7, fault = 5, vin = 8, freq = 1000)
```

### `set_freq`
Set PWM frequency.

- Parameter `freq` (`int`): The PWM frequency. Default is 1000.

```python
base_hdriver.set_freq()
```

### `get_freq`
Get PWM frequency.

- Returns: PWM frequency.
- Return type: int

```python
base_hdriver.get_freq()
```

### `set_speed`
Set motor speed.

- Parameter `speed` (`float`): The motor speed. Range -100~100. Default is 0.

```python
base_hdriver.set_speed()
```

### `get_status`
Get driver status.

- Returns: The driver status. Returns True if the driver is operating normally, or False if a fault is detected.
- Return type: bool

```python
base_hdriver.get_status()
```

### `get_voltage`
Get voltage.

- Returns: The driver input voltage. unit: V
- Return type: float

```python
base_hdriver.get_voltage()
```
