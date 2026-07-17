
# Joystick2 Unit

The joystick is an input unit for control, utilizing an I2C communication interface and supporting three-axis control signals (X/Y-axis analog input for displacement and Z-axis digital input for key presses). It is ideal for applications like gaming and robot control.

Support the following products:

Joystick2Unit

Micropython Example:
```python
import os, sys, io
import M5
from M5 import *
from unit import Joystick2Unit
from hardware import *
i2c = I2C(1, scl=22, sda=21)
joystick = Joystick2Unit(i2c)
joystick.read_adc_value()
joystick.read_button_status()
joystick.set_rgb_led(255, 0, 0)
joystick.get_rgb_led()
joystick.set_deadzone_position(200, 200)
while True:
    joystick.read_axis_position()
```

## class Joystick2Unit

## Constructors

### `class Joystick2Unit(i2c, address)`

    Initialize the Joystick Unit.

    - Parameter `i2c` (`I2C`): I2C port to use.
    - Parameter `address` (`int`): I2C address of the Joystick Unit.

## Methods

### `Joystick2Unit.set_axis_x_invert(invert)`

    Invert the X-axis of the joystick.

    - Parameter `invert` (`bool`): Whether to invert the X-axis.

### `Joystick2Unit.set_axis_y_invert(invert)`

    Invert the Y-axis of the joystick.

    - Parameter `invert` (`bool`): Whether to invert the Y-axis.

### `Joystick2Unit.set_axis_swap(swap)`

    Swap the X-axis and Y-axis of the joystick.

    - Parameter `swap` (`bool`): Whether to swap the X-axis and Y-axis.

### `Joystick2Unit.get_adc_value()`

    Read the ADC value of the joystick.

### `Joystick2Unit.get_button_status()`

    Read the button status of the joystick.

### `Joystick2Unit.set_led_brightness(brightness)`

    Set the brightness of the RGB LED.

    - Parameter `brightness` (`float`): The brightness value (0-100).

### `Joystick2Unit.fill_color(v)`

    Set the RGB LED color of the joystick.

    - Parameter `v`: The RGB value (0x000000-0xFFFFFF).

### `Joystick2Unit.fill_color_rgb(r, g, b)`

    Set the RGB LED color of the joystick.

    - Parameter `r` (`int`): The red value (0-255).
    - Parameter `g` (`int`): The green value (0-255).
    - Parameter `b` (`int`): The blue value (0-255).

### `Joystick2Unit.set_axis_x_mapping(adc_neg_min, adc_neg_max, adc_pos_min, adc_pos_max)`

        Set the mapping parameters of the X-axis.

        ADC Raw     0                                                    65536
        Mapped    -4096                   0           0                   4096
                    ----------------------dead zone---------------------
              adc_neg_min        adc_neg_max        adc_pos_min         adc_pos_max

    - Parameter `adc_neg_min` (`int`): The minimum ADC value of the negative range.
    - Parameter `adc_neg_max` (`int`): The maximum ADC value of the negative range.
    - Parameter `adc_pos_min` (`int`): The minimum ADC value of the positive range.
    - Parameter `adc_pos_max` (`int`): The maximum ADC value of the positive range.

### `Joystick2Unit.set_axis_y_mapping(adc_neg_min, adc_neg_max, adc_pos_min, adc_pos_max)`

        Set the mapping parameters of the Y-axis.

        ADC Raw     0                                                    65536
        Mapped    -4096                   0           0                   4096
                    ----------------------dead zone---------------------
              adc_neg_min        adc_neg_max        adc_pos_min         adc_pos_max

    - Parameter `adc_neg_min` (`int`): The minimum ADC value of the negative range.
    - Parameter `adc_neg_max` (`int`): The maximum ADC value of the negative range.
    - Parameter `adc_pos_min` (`int`): The minimum ADC value of the positive range.
    - Parameter `adc_pos_max` (`int`): The maximum ADC value of the positive range.

### `Joystick2Unit.set_deadzone_adc(x_adc_raw, y_adc_raw)`

    Set the dead zone of the joystick.

    - Parameter `x_adc_raw` (`int`): The dead zone of the X-axis. Range is 0 to 32768.
    - Parameter `y_adc_raw` (`int`): The dead zone of the Y-axis. Range is 0 to 32768.

### `Joystick2Unit.set_deadzone_position(x_pos, y_pos)`

    Set the dead zone of the joystick.

    - Parameter `x_pos` (`int`): The dead zone of the X-axis. Range is 0 to 4096.
    - Parameter `y_pos` (`int`): The dead zone of the Y-axis. Range is 0 to 4096.

### `Joystick2Unit.get_axis_position()`

    Read the position of the joystick.

### `Joystick2Unit.set_address(address)`

    Set the I2C address of the Joystick Unit.

    - Parameter `address` (`int`): The I2C address to set.

### `Joystick2Unit.get_firmware_version()`

    Read the firmware version of the Joystick Unit.

### `Joystick2Unit.get_x_raw()`

    Read the raw X-axis value of the joystick.

### `Joystick2Unit.get_y_raw()`

    Read the raw Y-axis value of the joystick.

### `Joystick2Unit.get_x_position()`

    Read the X-axis position of the joystick.

### `Joystick2Unit.get_y_position()`

    Read the Y-axis position of the joystick.
