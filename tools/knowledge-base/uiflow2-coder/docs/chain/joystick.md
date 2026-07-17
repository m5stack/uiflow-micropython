# Chain Joystick

Chain Joystick is a joystick module that can be connected to the M5Chain series devices. This module provides functions to read the joystick position and button states.

Support the following products:

    Chain Joystick

## MicroPython Example

#### USB Mouse

This example demonstrates how to use the Chain Joystick as a USB mouse.

```python
import os, sys, io
import M5
from M5 import *
from chain import JoystickChain
from chain import ChainBus
from usb.device.mouse import Mouse
import m5utils

bus2 = None
mouse = None
chain_joystick_0 = None

key_press = None
x = None
y = None

def chain_joystick_0_click_event(args):
    global bus2, mouse, chain_joystick_0, key_press, x, y
    key_press = True

def setup():
    global bus2, mouse, chain_joystick_0, key_press, x, y

    M5.begin()
    bus2 = ChainBus(2, tx=6, rx=5)
    chain_joystick_0 = JoystickChain(bus2, 1)
    chain_joystick_0.set_click_callback(chain_joystick_0_click_event)
    print(chain_joystick_0.get_firmware_version())
    mouse = Mouse()
    key_press = False

def loop():
    global bus2, mouse, chain_joystick_0, key_press, x, y
    M5.update()
    if mouse.is_open():
        x = int(m5utils.remap(chain_joystick_0.get_x(), -128, 127, -64, 64))
        y = int(m5utils.remap(chain_joystick_0.get_y(), -128, 127, 64, -64))
        mouse.move(x, y)
        if key_press:
            mouse.click_left(True)
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

#### JoystickChain

## `JoystickChain`
Joystick Chain class for interacting with joystick devices over Chain bus.

- Parameter `bus` (`ChainBus`): The Chain bus instance.
- Parameter `device_id` (`int`): The device ID of the joystick on the Chain bus.

```python
from chain import ChainBus
from chain import JoystickChain

chainbus_0 = ChainBus(2, 32, 33, verbose=True)
joystick_0 = JoystickChain(chainbus_0, 1)
```

### `get_x`
Get the X position of the joystick.

- Returns: X position (-128 to 127).
- Return type: int

```python
x = joystick_0.get_x()
```

### `get_y`
Get the Y position of the joystick.

- Returns: Y position (-128 to 127).
- Return type: int

```python
y = joystick_0.get_y()
```

### `get_x_16bit`
Get the X position of the joystick in 16-bit resolution.

- Returns: X position (-4095 to 4095).
- Return type: int

```python
x = joystick_0.get_x_16bit()
```

### `get_y_16bit`
Get the Y position of the joystick in 16-bit resolution.

- Returns: Y position (-4095 to 4095).
- Return type: int

```python
y = joystick_0.get_y_16bit()
```

### `get_x_raw`
Get the raw X ADC value of the joystick.

- Returns: Raw X ADC value (0-255).
- Return type: int

```python
x = joystick_0.get_x_raw()
```

### `get_y_raw`
Get the raw Y ADC value of the joystick.

- Returns: Raw Y ADC value (0-255).
- Return type: int

```python
y = joystick_0.get_y_raw()
```

### `get_x_16bit_raw`
Get the raw X ADC value of the joystick in 16-bit resolution.

- Returns: Raw X ADC value (0-65535).
- Return type: int

```python
x = joystick_0.get_x_16bit_raw()
```

### `get_y_16bit_raw`
Get the raw Y ADC value of the joystick in 16-bit resolution.

- Returns: Raw Y ADC value (0-65535).
- Return type: int

```python
y = joystick_0.get_y_16bit_raw()
```

### `get_mapping_value`
Get the mapping values of the joystick.

- Returns: A tuple containing the mapping values (x_negative_min, x_negative_max, x_positive_min, x_positive_max, y_negative_min, y_negative_max, y_positive_min, y_positive_max).
- Return type: tuple

```python
mapping = joystick_0.get_mapping_value()
```

### `set_mapping_value`
Set the mapping values of the joystick.

- Parameter `value` (`tuple`): A tuple containing the mapping values (x_negative_min, x_negative_max, x_positive_min, x_positive_max, y_negative_min, y_negative_max, y_positive_min, y_positive_max).
- Parameter `save` (`bool`): Whether to save the mapping values to non-volatile memory.
- Returns: True if the mapping values were set successfully, False otherwise.
- Return type: bool

```python
success = joystick_0.set_mapping_value((100, 200, 300, 400, 100, 200, 300, 400), True)
```

    For other button and some general methods, please refer to the `ChainKey <chain.key.KeyChain>` class.
