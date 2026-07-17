# CardKB Unit

Support the following products:

    CardKB Unit      CardKB Unit v1.1

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import CardKBUnit
from hardware import *

label0 = None
i2c0 = None
cardkb_0 = None

def cardkb_0_pressed_event(kb):
    global label0, i2c0, cardkb_0
    label0.setText(str(cardkb_0.get_string()))

def setup():
    global label0, i2c0, cardkb_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 132, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    cardkb_0 = CardKBUnit(i2c0)
    cardkb_0.set_callback(cardkb_0_pressed_event)

def loop():
    global label0, i2c0, cardkb_0
    M5.update()
    cardkb_0.tick()

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

## class CardKBUnit

## Constructors

### `class CardKBUnit(i2c: I2C, address: int  list  tuple = 0x5F)`

    Create a CardKBUnit object.

    - Parameter `i2c`: I2C object
    - Parameter `address`: I2C address, 0x5F by default

## Methods

### `CardKBUnit.get_key() -> int`

    Read the key value.

    - Returns: key value, int

### `CardKBUnit.get_string() -> str`

    Read the key string.

    - Returns: key string, str

### `CardKBUnit.is_pressed() -> bool`

    Check if the key is pressed.

    - Returns: True if the key is pressed, False otherwise

### `CardKBUnit.set_callback(handler)`

    Set the key press event callback.

    - Parameter `handler`: callback function

    Example:

```python
from cardkb_unit import CardKBUnit

def cb(key):
    print(key)

cardkb = CardKBUnit(i2c)
cardkb.set_callback(cb)
while True:
    cardkb.tick()
```
### `CardKBUnit.tick()`

    Update the key status.
