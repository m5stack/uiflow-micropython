# Relay Unit

Support the following products:

    RELAY

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import RelayUnit
import time

relay_0 = None

def setup():
    global relay_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    relay_0 = RelayUnit((36, 26))
    print(relay_0.get_status())
    relay_0.on()
    time.sleep(1)
    relay_0.off()
    time.sleep(1)
    relay_0.set_status(True)
    time.sleep(1)

def loop():
    global relay_0
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

## class RelayUnit

## Constructors

### `class RelayUnit(io)`

    Create a RelayUnit object.

    The parameters is:
        - `io` Define the control pin.

## Methods

### `RelayUnit.get_status()`

    Gets the relay switch status.

### `RelayUnit.on()`

    Turn on the relay.

### `RelayUnit.off()`

    Turn off the relay.

### `RelayUnit.set_status(x: bool)`

    Set the relay status.

    - Parameter `x` (`bool`): `True` turns the relay on; `False` turns it off.
