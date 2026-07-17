
# Color Unit

Support the following products:

ColorUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ColorUnit

title0 = None
label0 = None
label1 = None
label2 = None
i2c0 = None
color_0 = None

def setup():
    global title0, label0, label1, label2, i2c0, color_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "ColorUnit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("lux:", 2, 59, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("color:", 2, 114, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("saturation:", 2, 166, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    color_0 = ColorUnit(i2c0)

def loop():
    global title0, label0, label1, label2, i2c0, color_0
    M5.update()
    label0.setText(str((str("Iux:") + str((color_0.get_lux())))))
    label1.setText(str((str("color:") + str((color_0.get_color_rgb_bytes())))))
    label2.setText(str((str("saturation:") + str((color_0.get_color_s())))))

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

## class ColorUnit

## Constructors

### `class ColorUnit(i2c, address= _TCS3472_DEFAULT_ADDR)`

    Initialize ColorUnit sensor with the given I2C interface and address.

    - Parameter `i2c` (`I2C`): The I2C bus instance for communication.
    - Parameter `address` (`int`): The I2C address of the sensor, default is _TCS3472_DEFAULT_ADDR(0x29).

## Methods

### `ColorUnit.get_lux() -> float`

    Get the lux value computed from the color channels.

    - Returns: The computed lux value as a float.

### `ColorUnit.get_color_temperature() -> float`

    Get the color temperature in degrees Kelvin.

    - Returns: The color temperature as a float in Kelvin.

### `ColorUnit.get_color_rgb_bytes() -> tuple`

    Get the RGB color detected by the sensor.

    - Returns: A tuple of red, green, and blue component values as bytes (0-255).

### `ColorUnit.get_color_r() -> int`

    Get the red component of the RGB color.

    - Returns: The red component value (0-255).

### `ColorUnit.get_color_g() -> int`

    Get the green component of the RGB color.

    - Returns: The green component value (0-255).

### `ColorUnit.get_color_b() -> int`

    Get the blue component of the RGB color.

    - Returns: The blue component value (0-255).

### `ColorUnit.get_color_h() -> int`

    Get the hue (H) value of the color in degrees.

    - Returns: The hue value as an integer in the range [0, 360].

### `ColorUnit.get_color_s() -> float`

    Get the saturation (S) value of the color.

    - Returns: The saturation value as a float in the range [0, 1].

### `ColorUnit.get_color_v() -> float`

    Get the value (V) of the color (brightness).

    - Returns: The value as a float in the range [0, 1].

### `ColorUnit.get_color() -> int`

    Get the RGB color as an integer value.

    - Returns: An integer representing the RGB color, with 8 bits per channel.

### `ColorUnit.get_color565() -> int`

    Get the RGB color in 5-6-5 format as an integer.
    - Returns: An integer representing the RGB color in 5-6-5 format.

### `ColorUnit.get_active() -> bool`

    Get the active state of the sensor.

    - Returns: True if the sensor is active, False if it is inactive.

### `ColorUnit.set_active(val)`

    Set the active state of the sensor.

    - Parameter `val` (`bool`): : True to activate the sensor, False to deactivate it.

### `ColorUnit.get_integration_time() -> float`

    Get the integration time of the sensor in milliseconds.

    - Returns: The integration time as a float.

### `ColorUnit.set_integration_time(val)`

    Set the integration time of the sensor.

    - Parameter `val` (`float`): : The desired integration time in milliseconds.

### `ColorUnit.get_gain() -> int`

    Get the gain of the sensor.

    - Returns: The gain value, which should be one of 1, 4, 16, or 60.

### `ColorUnit.set_gain(val)`

    Set the gain of the sensor.

    - Parameter `val` (`int`): : The desired gain value (1, 4, 16, or 60).

### `ColorUnit.read_interrupt() -> bool`

    Read the interrupt status.

    - Returns: True if the interrupt is set, False otherwise.

### `ColorUnit.clear_interrupt()`

    Clear the interrupt status of the sensor by writing to the interrupt register.

### `ColorUnit.get_color_raw()`

    Read the raw RGBC color detected by the sensor.

    - Returns: A tuple containing raw red, green, blue, and clear color data.

### `ColorUnit.get_cycles()`

    Get the persistence cycles of the sensor.

    - Returns: The persistence cycles or -1 if interrupts are disabled.

### `ColorUnit.set_cycles(val)`

    Set the persistence cycles for the sensor.

    - Parameter `val` (`int`): : The number of persistence cycles, or -1 to disable interrupts.

### `ColorUnit.get_min_value()`

    Get the minimum threshold value (AILT register) of the sensor.

    - Returns: The minimum threshold value.

### `ColorUnit.set_min_value(val)`

    Set the minimum threshold value (AILT register) of the sensor.

    - Parameter `val` (`int`): : The minimum threshold value to set.

### `ColorUnit.get_max_value()`

    Get the maximum threshold value (AIHT register) of the sensor.

    - Returns: The maximum threshold value.

### `ColorUnit.set_max_value(val)`

    Set the maximum threshold value (AIHT register) of the sensor.

    - Parameter `val` (`int`): : The maximum threshold value to set.

### `ColorUnit.get_glass_attenuation()`

    Get the Glass Attenuation factor used to compensate for lower light levels due to glass presence.

    - Returns: The glass attenuation factor (ga).

### `ColorUnit.set_glass_attenuation(value)`

    Set the Glass Attenuation factor used to compensate for lower light levels due to glass presence.

    - Parameter `value` (`float`): : The glass attenuation factor to set. Must be greater than or equal to 1.
