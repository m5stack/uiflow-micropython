# Relay4 Unit

4-Relay unit is an integrated 4-way relay module which can be controlled by I2C
protocol. The maximum control voltage of each relay is AC-250V/DC-28V, the rated
current is 10A and the instantaneous current can hold up to 16A. Each relay can
be controlled independently, each on it's own. Each relay has status (LED)
indictor as well to show the state of the relay at any given time.

Support the following products:

    Relay4Unit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import Relay4Unit
import time

i2c0 = None
relay4_0 = None

def setup():
    global i2c0, relay4_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    relay4_0 = Relay4Unit(i2c0, 0x26)

def loop():
    global i2c0, relay4_0
    M5.update()
    relay4_0.set_relay_all(1)
    time.sleep(1)
    relay4_0.set_relay_all(0)
    time.sleep(1)

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

## class Relay4Unit

## Constructors

### `class Relay4Unit(i2c: I2C, address: int  list  tuple = 0x26)`

    Initialize the Relay4Unit object.

    - Parameter `i2c` (`I2C`): I2C port to use.
    - Parameter `address` (`int`): I2C address of the Relay4Unit.

## Methods

### `Relay4Unit.set_mode(mode: int)`

    Set the mode of the relay.

    - Parameter `mode` (`int`): The mode of the relay

        Options:
        - `Relay4Unit.ASYNC_MODE`: async
        - `Relay4Unit.SYNC_MODE`: sync

### `Relay4Unit.get_mode() -> int`

    Get the mode of the relay.

    - Returns: The mode of the relay

        Options:
        - `Relay4Unit.ASYNC_MODE`: async
        - `Relay4Unit.SYNC_MODE`: sync

### `Relay4Unit.get_led_state(n: int) -> int`

    Get the state of the LED.

    - Parameter `n` (`int`): The number of the LED.

### `Relay4Unit.set_led_state(n: int, state: int) -> None`

    Set the state of the LED.

    - Parameter `n` (`int`): The number of the LED.
    - Parameter `state` (`int`): The state of the LED.

### `Relay4Unit.get_relay_state(n: int) -> int`

    Get the state of the relay.

    - Parameter `n` (`int`): The number of the relay.

    - Returns: The state of the relay.

### `Relay4Unit.set_relay_state(n: int, state: int) -> None`

    Set the state of the relay.

    - Parameter `n` (`int`): The number of the relay.
    - Parameter `state` (`int`): The state of the relay.

### `Relay4Unit.set_relay_all(state: int) -> None`

    Set the state of all the relay.

    - Parameter `state` (`int`): The state of the relay.
