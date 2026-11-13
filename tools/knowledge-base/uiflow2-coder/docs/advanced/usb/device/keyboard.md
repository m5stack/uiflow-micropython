# keyboard

usb device keyboard

> Note: This module is only applicable to the CoreS3 Controller
Key codes are imported from `usb.device.hid`, not `unit` or
`usb.device.keyboard`. See [Keyboard key codes](../../../hardware/keycode.md) for the
complete `usb.device.hid.KeyCode` list and the distinction from CardKB
character codes. In this namespace, Enter is `KeyCode.ENTER` (40) and
Escape is `KeyCode.ESCAPE` (41); `KeyCode.KEYCODE_ENTER` does not exist.

```python
from usb.device.keyboard import Keyboard
from usb.device.hid import KeyCode

keyboard = Keyboard()
```
The examples below use this `keyboard` instance.

## Micropython Example

### USB keyboard

```python
import os, sys, io
import M5
from M5 import *
from unit import CardKBUnit
from usb.device.keyboard import Keyboard
from hardware import I2C
from hardware import Pin

label = None
keyboard = None
i2c0 = None
cardkb_0 = None
key = None
update = None

def cardkb_0_pressed_event(kb):
    global label, keyboard, i2c0, cardkb_0, key, update
    key = cardkb_0.get_key()
    update = True

def setup():
    global label, keyboard, i2c0, cardkb_0, key, update
    M5.begin()
    Widgets.fillScreen(0x222222)
    label = Widgets.Label("USB Keyboard", 73, 6, 1.0, 0x3CC7F1, 0x222222, Widgets.FONTS.DejaVu24)
    keyboard = Keyboard()
    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    cardkb_0 = CardKBUnit(i2c0)
    cardkb_0.set_callback(cardkb_0_pressed_event)
    update = False

def loop():
    global label, keyboard, i2c0, cardkb_0, key, update
    M5.update()
    cardkb_0.tick()
    if keyboard.is_open():
        if update:
            keyboard.input(str(chr(key)))
            update = False

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

## class Keyboard

### `class usb.device.keyboard.Keyboard()`

    Create Keyboard object

    UIFlow2.0

### `Keyboard.set_modifiers(right_gui: bool = False, right_alt: bool = False, right_shift: bool = False, right_ctrl: bool = False, \`
                       left_gui: bool = False, left_alt: bool = False, left_shift: bool = False, left_ctrl: bool = False)

    Set modifier keys

    - `right_gui` The state of the right-side GUI key. True indicates that the key is pressed.
    - `right_alt` The state of the right-side Alt key. True indicates that the key is pressed.
    - `right_shift` The state of the right-side Shift key. True indicates that the key is pressed.
    - `right_ctrl` The state of the right-side Ctrl key. True indicates that the key is pressed.
    - `left_gui` The state of the left-side GUI key. True indicates that the key is pressed.
    - `left_alt` The state of the left-side Alt key. True indicates that the key is pressed.
    - `left_shift` The state of the left-side Shift key. True indicates that the key is pressed.
    - `left_ctrl`  The state of the left-side Ctrl key. True indicates that the key is pressed.

    UIFlow2.0

### `Keyboard.set_keys(k0: int = 0, k1: int = 0, k2: int = 0, k3: int = 0, k4: int = 0, k5: int = 0)`

    Press specified keys (up to 6 key values at a time)

    - `k0~k5` The input is a standard HID key value. For details, see [Keyboard key codes](../../../hardware/keycode.md). Use nonnegative HID usage IDs here; set modifiers separately with `set_modifiers()`.

    example: Press the lowercase 'a'

        keyboard.set_keys(k0=KeyCode.A)
        keyboard.send_report()
        keyboard.set_keys(k0=0)
        keyboard.send_report()

    example: Press the uppercase 'A'

        keyboard.set_modifiers(right_shift=True)
        keyboard.set_keys(k0=KeyCode.A)
        keyboard.send_report()
        keyboard.set_modifiers(right_shift=False)
        keyboard.set_keys(k0=0)
        keyboard.send_report()

    UIFlow2.0

### `Keyboard.send_report()`

    Send keyboard status report

    UIFlow2.0

### `Keyboard.input(key)`

    input key

    - `key` A supported ASCII string, or a nonnegative USB HID usage ID from `usb.device.hid.KeyCode`. An integer is a HID ID, not an ASCII character code. For modifiers, use `set_modifiers()` or `send_keys()` instead.

    example:
```
keyboard.input("Hello M5")
keyboard.input(KeyCode.A)
```
    UIFlow2.0

### `Keyboard.send_keys(down_keys, timeout_ms=100)`

    Send a report for an iterable of HID key values. Nonnegative values
    occupy the six key slots; negative `KeyCode` modifier constants
    contribute their mask to the modifier byte. This method sends its
    own report and does not use the state set by `set_keys()` or
    `set_modifiers()`.

    - Parameter `down_keys`: Iterable of USB HID usage IDs and/or negative modifiers.
    - Parameter `timeout_ms` (`int`): Maximum wait for a previous pending report.
    - Returns: `True` when queued, or `False` on timeout/failure.

```python
keyboard.send_keys([KeyCode.LEFT_SHIFT, KeyCode.A])
keyboard.send_keys([])  # Release all keys.
```
