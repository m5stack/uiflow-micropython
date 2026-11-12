# IR Unit

Support the following products:

    IR

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import IRUnit
import time

ir_0 = None

def setup():
    global ir_0

    M5.begin()
    Widgets.fillScreen(0x222222)

    ir_0 = IRUnit((36, 26))

def loop():
    global ir_0
    M5.update()
    ir_0.tx(0, 0)
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

## class IRUnit

## Constructors

### `class IRUnit(port)`

    Create an IRUnit object.

    - Parameter `port` (`tuple`): The port to which the IR unit is connected. the tuple is a pair of values, the first value is the receive pin, and the second value is the transmit pin.

## Methods

### `IRUnit.tx(cmd, data)`

    Sends an ir signal value to an address.

    - Parameter `cmd` (`int`): NEC address byte (0-255).
    - Parameter `data` (`int`): NEC command byte (0-255).

### `IRUnit.rx_cb(cb)`

    Register a callback for received NEC infrared data.

    - Parameter `cb` (`callable`): Called as `cb(data, addr, ctrl)` with the command byte,
        address byte, and control value (0 for a normal frame or -1 for a repeat).
