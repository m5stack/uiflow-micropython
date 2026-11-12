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

### `class CardKBUnit(*args, mode=CardKBUnit.CardKB_I2C_MODE, **kwargs)`

    Factory returning the driver for the selected communication mode.
    The keyboard firmware and connection must already support that mode;
    selecting `mode` does not reconfigure the keyboard firmware.

    - Parameter `mode` (`int`): `CardKB_I2C_MODE` (0, default), `CardKB_UART_MODE` (1), or `CardKB_ESP_NOW_MODE` (2).
    - Returns: `unit.cardkb.CardKBI2C` for I2C mode,
        `unit.cardkb.CardKBUART` for UART mode, or
        `unit.cardkb.CardKBESPNOW` for ESP-NOW mode.

    These are the concrete returned classes, not subclasses of `CardKBUnit`.
    The methods below belong to the returned instance; for example, call
    `cardkb.get_key()` rather than looking up `CardKBUnit.get_key`.

    **I2C:** pass the I2C object as the first positional argument. The optional
    `address` keyword defaults to `0x5F` and applies only to I2C.

```python
from unit import CardKBUnit
from hardware import I2C, Pin

# Choose GPIO pins for your controller.
i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
cardkb = CardKBUnit(i2c0, address=0x5F, mode=CardKBUnit.CardKB_I2C_MODE)
```
    **UART:** pass the UART ID as the first positional argument and
    `port=(rx_pin, tx_pin)`. The driver uses 115200 baud, 8N1.

```python
cardkb = CardKBUnit(2, port=(33, 32), mode=CardKBUnit.CardKB_UART_MODE)
```
    **ESP-NOW:** no bus argument is needed.

```python
cardkb = CardKBUnit(mode=CardKBUnit.CardKB_ESP_NOW_MODE)
```

## Methods

### `CardKBUnit.get_key()`

    Read the key value.

    - Returns: An integer key code in I2C mode, or a `(key_id, key_state)`
        tuple in UART and ESP-NOW modes. Returns `None` when no key is available.
        The state is `CardKBUnit.KEY_STATE_PRESS` or `CardKBUnit.KEY_STATE_RELEASE`.

### `CardKBUnit.get_string() -> str`

    Read the key string.

    - Returns: key string, str

### `CardKBUnit.is_pressed() -> bool`

    Check if the key is pressed.

    - Returns: True if the key is pressed, False otherwise

### `CardKBUnit.set_callback(handler)`

    Set the key press event callback.

    - Parameter `handler`: Callback function. I2C callbacks receive the CardKB instance;
        UART and ESP-NOW callbacks receive a key tuple.

    Example:

```python
from unit import CardKBUnit

def cb(keyboard):
    print(keyboard.get_key())

cardkb = CardKBUnit(i2c)
cardkb.set_callback(cb)
while True:
    cardkb.tick()
```
### `CardKBUnit.tick()`

    Update the key status.
