# Relay2 Unit

This is the driver library of Relay2 Unit, which is used to control the relay.

Support the following products:

    RELAY2

## MicroPython Example

#### control relay

This example controls the relay of the Relay2 Unit and displays it on the screen.

```python
import os, sys, io
import M5
from M5 import *
from unit import Relay2Unit

title0 = None
label2 = None
label0 = None
label3 = None
label1 = None
relay2_0 = None

def setup():
    global title0, label2, label0, label3, label1, relay2_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "Relay2Unit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("Relay1", 38, 214, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label("label0", 2, 91, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Relay2", 220, 214, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 2, 136, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    relay2_0 = Relay2Unit((33, 32))

def loop():
    global title0, label2, label0, label3, label1, relay2_0
    M5.update()
    label0.setText(str((str("Relay1 State:") + str((relay2_0.get_relay_status(1))))))
    label1.setText(str((str("Relay2 State:") + str((relay2_0.get_relay_status(2))))))
    if BtnA.wasPressed():
        relay2_0.set_relay_cntrl(1, not (relay2_0.get_relay_status(1)))
    elif BtnC.wasPressed():
        relay2_0.set_relay_cntrl(2, not (relay2_0.get_relay_status(2)))

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

#### Relay2Unit

## `Relay2Unit`
Create an Relay2Unit object.

- Parameter `port` (`tuple`): The port of the relay.

```python
from unit import Relay2Unit

relay2_0 = Relay2Unit((32, 26))
```

### `set_relay_cntrl`
Set the on/off status of a relay

- Parameter `num` (`int`): The relay number(the range is 1-2).
- Parameter `control` (`int`): The control value(0: off, 1: on).

```python
relay2_0.set_relay_cntrl(1, 1)
```

### `get_relay_status`
Getting the on/off status of a relay

- Parameter `num` (`int`): The relay number.
- Returns: relay status.
- Return type: bool

```python
relay2_0.get_relay_status()
```
