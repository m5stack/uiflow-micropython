# Atomic PWM Base

Support the following products:

    Atomic PWM Base

## MicroPython Example:

#### PWM output control

The example demonstrates controlling the PWM signal's duty cycle to fluctuate between low to high and high to low.

```python
import os, sys, io
import M5
from M5 import *
from base import AtomicPWMBase
import time

title0 = None
label0 = None
label1 = None
label_freq = None
label_duty = None
base_pwm = None
i = None

def setup():
    global title0, label0, label1, label_freq, label_duty, base_pwm, i
    M5.begin()
    title0 = Widgets.Title("PWM Control", 0, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("freq:", 1, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("duty:", 2, 65, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_freq = Widgets.Label("1000Hz", 47, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    label_duty = Widgets.Label("0", 55, 65, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu18)
    base_pwm = AtomicPWMBase(5, 1000)
    label_freq.setText(str((str((base_pwm.get_freq())) + str("Hz"))))

def loop():
    global title0, label0, label1, label_freq, label_duty, base_pwm, i
    M5.update()
    for i in range(100):
        base_pwm.set_duty_u16(i * 150)
        label_duty.setText(str(base_pwm.get_duty_u16()))
        time.sleep_ms(40)
    for i in range(100):
        base_pwm.set_duty_u16(15000 - i * 150)
        label_duty.setText(str(base_pwm.get_duty_u16()))
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

#### PWM

## `AtomicPWMBase`
Create an AtomicPWMBase object.

- Parameter `out_pin` (`int`): The PWM output pin. Default is 5.
- Parameter `freq` (`int`): The PWM frequency. Default is 1000.

```python
from base import AtomicPWMBase

base_pwm = AtomicPWMBase(out_pin=5, freq=1000)
```

### `set_freq`
Set PWM frequency.

- Parameter `freq` (`int`): The PWM frequency. Default is 1000.

```python
base_pwm.set_freq()
```

### `get_freq`
Get PWM frequency.

- Returns: PWM frequency.
- Return type: int

```python
base_pwm.get_freq()
```

### `set_duty_u16`
Set PWM duty cycle.

set the current duty cycle of the PWM output, as an unsigned 16-bit value in the range 0 to 65535 inclusive.

- Parameter `duty` (`int`): The PWM duty cycle. Range: 0 ~ 65535. Default is 0.

```python
base_pwm.set_duty_u16()
```

### `get_duty_u16`
Get PWM duty cycle.

- Returns: PWM duty cycle. Range: 0~65535.
- Return type: int

```python
base_pwm.get_duty_u16()
```
