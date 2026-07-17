# Step16 Unit

This library is the driver for Unit Step16.

Support the following products:

    Unit Step16

## MicroPython Example

#### Read Encoder

This example shows how to read and display encoder readings.

```python
import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import Step16Unit

title0 = None
label1 = None
label_val = None
i2c0 = None
step16_0 = None
val = None

def setup():
    global title0, label1, label_val, i2c0, step16_0, val
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("UnitStep16 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label1 = Widgets.Label(
        "Encoder Value:", 10, 55, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24
    )
    label_val = Widgets.Label("0", 205, 55, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    step16_0 = Step16Unit(i2c0, 0x48)
    print((str("i2c addr: ") + str((step16_0.get_addr()))))
    print((str("version: ") + str((step16_0.get_firmware_version()))))
    step16_0.set_led_mode(Step16Unit.AUTO_OFF, 5)
    step16_0.set_led_brightness(80)
    print((str("rgb brightness: ") + str((step16_0.get_rgb_brightness()))))
    print((str("rgb value: ") + str((step16_0.get_rgb_value()))))
    if step16_0.get_rgb_power():
        print("RGB power on")
    else:
        print("RG B power off")
    step16_0.set_rgb_power(True)
    step16_0.set_rgb_value(0x3333FF)

def loop():
    global title0, label1, label_val, i2c0, step16_0, val
    M5.update()
    val = step16_0.get_encoder_value()
    label_val.setText(str(val))

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

#### Step16Unit

## `Step16Unit`
Create an Step16Unit object.

- Parameter `i2c` (`I2C`): I2C port,
- Parameter ` list  tuple addr` (`int`): Step16Unit Slave Address

```python
from unit import Step16Unit

unit_step16_0 = Step16Unit(i2c0, 0x48)
```

### `get_encoder_value`
Get the current encoder value (0~15).

- Returns: Encoder value.
- Return type: int

```python
value = unit_step16_0.get_encoder_value()
```

### `set_encoder_cw_increase`
Configure whether clockwise rotation increases encoder value.

- Parameter `enable`:
    - True: Clockwise rotation increases the encoder value.
    - False: Clockwise rotation decreases the encoder value.
- Type of `enable`: bool

```python
unit_step16_0.set_encoder_cw_increase(True)
unit_step16_0.set_encoder_cw_increase(False)
```

### `get_encoder_cw_increase`
Get current encoder direction mode.

- Returns: 1 for increasing clockwise, 0 for decreasing.
- Return type: int

```python
direction = unit_step16_0.get_encoder_cw_increase()
```

### `set_led_mode`
Set LED display mode.

- Parameter `mode`: LED mode type.
    0 = always off,
    1 = always on,
    2 = auto-off mode with `seconds` as timeout.
- Type of `mode`: int
- Parameter `seconds`: Timeout in seconds if `mode` is 2 (auto-off).
- Type of `seconds`: int

```python
unit_step16_0.set_led_mode(0)         # Always off
unit_step16_0.set_led_mode(1)         # Always on
unit_step16_0.set_led_mode(2, 10)     # Auto-off after 10 seconds
```

### `get_led_mode`
Get LED display mode.

The LED mode values:

- `0x00` : Always Off.
- `0xFE` : Always On.
- `0x00` ~ `0xFD` : Auto off times in seconds.

- Returns: LED display mode.
- Return type: int

```python
unit_step16_0.get_led_mode()
```

### `set_led_brightness`
Set LED brightness (0~100).

- Parameter `int` (`brightness`): Brightness level.
- Type of `brightness`: int

```python
unit_step16_0.set_led_brightness(80)
```

### `get_led_brightness`
Get current LED brightness.

- Returns: Brightness level.
- Return type: int

```python
brightness = unit_step16_0.get_led_brightness()
print("Brightness:", brightness)
```

### `set_rgb_power`
Turn the RGB light power ON or OFF.

- Parameter `enable`: True to turn on the RGB light, False to turn it off.
- Type of `enable`: bool

```python
unit_step16_0.set_rgb_power(True)   # Turn ON RGB light
unit_step16_0.set_rgb_power(False)  # Turn OFF RGB light
```

### `get_rgb_power`
Get the current power status of the RGB light.

- Returns: True if the RGB light is ON, False if OFF.
- Return type: bool

```python
power_on = unit_step16_0.get_rgb_power()
```

### `set_rgb_brightness`
Set the brightness of the RGB light (0~100%).

- Parameter `brightness`: Brightness percentage (0~100).
- Type of `brightness`: int

```python
unit_step16_0.set_rgb_brightness(80)  # Set RGB brightness to 80%
```

### `get_rgb_brightness`
Get the current RGB brightness level (0~100%).

- Returns: Current RGB brightness percentage (0~100).
- Return type: int

```python
brightness = unit_step16_0.get_rgb_brightness()
print("RGB Brightness:", brightness)
```

### `set_rgb_value`
Set RGB LED color using a 24-bit integer.

- Parameter `color`: A 24-bit integer representing the RGB color (e.g., 0xFF8040 for R=255, G=128, B=64).
              Format is (R << 16) | (G << 8) | B.

```python
unit_step16_0.set_rgb_value()
```

### `get_rgb_value`
Get current RGB LED color.

- Returns: Tuple of (r, g, b)
- Return type: tuple

```python
r, g, b = unit_step16_0.get_rgb_value()
```

### `save_led_config`
Save current LED mode and brightness settings.

```python
unit_step16_0.save_led_config()
```

### `save_rgb_config`
Save current RGB color settings.

```python
unit_step16_0.save_rgb_config()
```

### `set_addr`
Set the device's I2C address.

- Parameter `new_addr`: New I2C address (0x08~0x77).
- Type of `new_addr`: int

```python
unit_step16_0.set_addr(0x49)
```

### `get_addr`
Get the current I2C device address.

- Returns: I2C address.
- Return type: int

```python
addr = unit_step16_0.get_addr()
```

### `get_firmware_version`
Get the firmware version.

- Returns: firmware version.
- Return type: int

```python
addr = unit_step16_0.get_firmware_version()
```
