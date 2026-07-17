# Chain Key

Chain Key is a key module that can be connected to the M5Chain series devices. This module provides functions to read the key states.

Support the following products:

    Chain Key

## MicroPython Example

#### USB Keyboard

This example demonstrates how to use the Chain Key as a USB keyboard.

```python
import os, sys, io
import M5
from M5 import *
from chain import KeyChain
from chain import ChainBus
from usb.device.keyboard import Keyboard
from usb.device.hid import KeyCode

bus2 = None
keyboard = None
chain_key_0 = None

key_press = None

def chain_key_0_click_event(args):
    global bus2, keyboard, chain_key_0, key_press
    key_press = True

def setup():
    global bus2, keyboard, chain_key_0, key_press

    M5.begin()
    bus2 = ChainBus(2, tx=6, rx=5)
    keyboard = Keyboard()
    chain_key_0 = KeyChain(bus2, 1)
    chain_key_0.set_click_callback(chain_key_0_click_event)
    key_press = False

def loop():
    global bus2, keyboard, chain_key_0, key_press
    M5.update()
    if keyboard.is_open():
        if key_press:
            keyboard.input(KeyCode.A)
            key_press = False

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

#### KeyChain

## `KeyChain`
Create a KeyChain object.

- Parameter `bus` (`ChainBus`): ChainBus object.
- Parameter `device_id` (`int`): Device ID.

```python
from chain import ChainBus
from chain import KeyChain

chainbus_0 = ChainBus(2, 32, 33, verbose=True)
keychain_0 = KeyChain(chainbus_0, 1)
```

### `get_button_state`
get button state.

- Returns: Button state, True if pressed, False otherwise.
- Return type: bool

```python
keychain_0.get_button_state()
```

### `set_click_callback`
set button click callback.

- Parameter `callback`: Callback function.

> Note: Chain related methods cannot be called in the callback function.

```python
def keychain_0_click_callback(args):
    print("click")

keychain_0.set_click_callback(keychain_0_click_callback)
```

### `set_double_click_callback`
set button double click callback.

- Parameter `callback`: Callback function.

> Note: Chain related methods cannot be called in the callback function.

```python
def keychain_0_double_click_callback(args):
    print("double click")

keychain_0.set_double_click_callback(keychain_0_double_click_callback)
```

### `set_long_press_callback`
set button long press callback.

- Parameter `callback`: Callback function.

> Note: Chain related methods cannot be called in the callback function.

```python
def keychain_0_long_press_callback(args):
    print("long press")

keychain_0.set_long_press_callback(keychain_0_long_press_callback)
```

### `set_button_double_click_trigger_interval`
set button double click trigger interval.

- Parameter `interval_ms` (`int`): Interval time in milliseconds. range: 100-1000
- Returns: True if success, False otherwise.
- Return type: bool

```python
keychain_0.set_button_double_click_trigger_interval(100)
```

### `set_button_long_press_trigger_interval`
set button long press trigger interval.

- Parameter `interval_ms` (`int`): Interval time in milliseconds. range: 3000-30000
- Returns: True if success, False otherwise.
- Return type: bool

```python
keychain_0.set_button_long_press_trigger_interval(3000)
```

### `get_button_double_click_trigger_interval`
get button double click trigger interval.

- Returns: Interval time in milliseconds.
- Return type: int

```python
interval = keychain_0.get_button_double_click_trigger_interval()
```

### `get_button_long_press_trigger_interval`
get button long press trigger interval.

- Returns: Interval time in milliseconds.
- Return type: int

```python
interval = keychain_0.get_button_long_press_trigger_interval()
```

### `set_button_mode`
set button mode.

- Parameter `mode` (`int`): Button mode. Use `KeyChain.MODE_POLL` or `KeyChain.MODE_EVENT`.
- Returns: True if success, False otherwise.
- Return type: bool

```python
keychain_0.set_button_mode(KeyChain.MODE_EVENT)
```

### `get_button_mode`
get button mode.

- Returns: Button mode. `KeyChain.MODE_POLL` or `KeyChain.MODE_EVENT`.
- Return type: int

```python
mode = keychain_0.get_button_mode()
```

### `set_rgb_color`
set RGB color.

- Parameter `color` (`int`): RGB color value.
- Returns: True if success, False otherwise.
- Return type: bool

```python
keychain_0.set_rgb_color(0xFF0000)
```

### `get_rgb_color`
get RGB color.

- Parameter `index`: Index of the RGB LED.
- Returns: RGB color value.
- Return type: int

```python
color = keychain_0.get_rgb_color()
```

### `set_rgb_brightness`
set RGB brightness.

- Parameter `brightness` (`int`): Brightness value (0-100).
- Parameter `save` (`bool`): Whether to save the brightness setting to flash.
- Returns: True if success, False otherwise.
- Return type: bool

```python
keychain_0.set_rgb_brightness(80)
```

### `get_rgb_brightness`
get RGB brightness.

- Returns: Brightness value (0-100).
- Return type: int

```python
brightness = keychain_0.get_rgb_brightness()
```

### `get_bootloader_version`
get bootloader version.

- Returns: Bootloader version.
- Return type: int

```python
version = keychain_0.get_bootloader_version()
```

### `get_firmware_version`
get firmware version.

- Returns: Firmware version.
- Return type: int

```python
version = keychain_0.get_firmware_version()
```

### `get_device_type`
get device type.

- Returns: Device type. Returns -1 if failed.
- Return type: int

```python
device_type = keychain_0.get_device_type()
```

### `get_device_uid`
get device UID.

- Parameter `uid_type` (`int`): UID type, 0 for 4-byte UID, 1 for 12-byte UID.
- Returns: Tuple of UID bytes (4 bytes or 12 bytes). Returns empty tuple on error.
- Return type: tuple

```python
uid = keychain_0.get_device_uid(0)  # 4-byte UID
uid = keychain_0.get_device_uid(1)  # 12-byte UID
```
