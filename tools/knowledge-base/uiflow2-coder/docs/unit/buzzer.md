# Buzzer Unit

Support the following products:

    Buzzer

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import BuzzerUnit

buzzer_0 = None

def setup():
    global buzzer_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    buzzer_0 = BuzzerUnit((8, 9))

def loop():
    global buzzer_0
    M5.update()
    if M5.Touch.getCount():
        buzzer_0.once(freq=4000, duty=50, duration=50)

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

## class BuzzerUnit

## Constructors

### `class BuzzerUnit(port)`

    Create an BuzzerUnit object.

    The parameters are:
        - `port` Is the pin number of the port

## Methods

### `BuzzerUnit.once(freq=10, duty=50, duration=50)`

    Play buzzer once.

    - Parameter `freq` (`int`): The frequency of the vibration, range is 100 - 10000Hz.
    - Parameter `duty` (`int`): The duty cycle of the vibration, range is 0 - 100.
    - Parameter `duration` (`int`): The duration of the vibration, range is 0 - 10000ms.

### `BuzzerUnit.set_freq(freq: int)`

    Set the frequency of the buzzer.

    - Parameter `freq` (`int`): The frequency of the vibration, range is 100 - 10000Hz.

### `BuzzerUnit.set_duty(duty: int)`

    Set the duty cycle of the buzzer.

    - Parameter `duty` (`int`): The duty cycle of the vibration, range is 0 - 100.

### `BuzzerUnit.turn_off()`

    Turn off the buzzer.

### `BuzzerUnit.deint()`

    Deinitialize the buzzer.
