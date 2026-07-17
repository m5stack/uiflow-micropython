
# EXTIO2 Unit

EXT.IO2 is an IO extended unit, based on STM32F030 main controller, using I2C communication interface and providing 8 IO expansion. Each IO supports independent configuration of digital I/O, ADC, SERVO control, RGB LED control modes. Supports configuration of device I2C address, which means that users can mount multiple EXT.IO2 UNITs on the same I2C BUS to extend more IO resources. Suitable for multiple digital/analog signal acquisition, with lighting/servo control applications.

Support the following products:

EXTIO2Unit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import EXTIO2Unit

title0 = None
label0 = None
i2c0 = None
extio2_0 = None

def setup():
    global title0, label0, i2c0, extio2_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "ExtIO2Unit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("IO6 State:", 2, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    extio2_0 = EXTIO2Unit(i2c0)
    extio2_0.set_config_mode(0, 1)
    extio2_0.set_config_mode(6, 2)
    extio2_0.set_config_mode(3, 4)
    extio2_0.write_rgb_led(3, 0xFF0000)

def loop():
    global title0, label0, i2c0, extio2_0
    M5.update()
    label0.setText(str((str("IO6 State:") + str((extio2_0.read_adc12_pin(0))))))

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

## class EXTIO2Unit

## Constructors

### `class EXTIO2Unit(i2c, address)`

    Initialize EXTIO2Unit with I2C or PAHUBUnit and address for communication.

    - Parameter `i2c`: The I2C or PAHUBUnit interface for communication with the EXTIO2Unit.
    - Parameter `address` (`int`): The I2C address for the unit, default is _DEFAULT_ADDRESS.

## Methods

### `EXTIO2Unit.set_config_mode(id, mode)`

    Set the configuration mode for a specific channel.

    - Parameter `id` (`int`): The channel ID to set the mode for.
    - Parameter `mode`: The mode to set, defined by the EXTIO2Unit. Can be 0, 1, 2, 3, or 4.

### `EXTIO2Unit.write_output_pin(id, value)`

    Write a value to an output pin of the EXTIO2Unit.

    - Parameter `id` (`int`): The pin ID to write the value to.
    - Parameter `value`: The value to write, either 0 or 1.

### `EXTIO2Unit.write_servo_angle(id, angle)`

    Write an angle to a servo connected to the EXTIO2Unit.

    - Parameter `id` (`int`): The servo ID to set the angle for.
    - Parameter `angle` (`int`): The angle to set the servo to (0-255).

### `EXTIO2Unit.write_servo_pulse(id, pulse)`

    Write a pulse width to a servo connected to the EXTIO2Unit.

    - Parameter `id` (`int`): The servo ID to set the pulse for.
    - Parameter `pulse` (`int`): The pulse width to set the servo to, in microseconds.

### `EXTIO2Unit.write_rgb_led(id, value)`

    Write an RGB color value to a NeoPixel LED.

    - Parameter `id` (`int`): The NeoPixel ID to set the color for.
    - Parameter `value`: The RGB value to set, represented as a 24-bit integer.

### `EXTIO2Unit.set_address(address)`

    Set the I2C address for the EXTIO2Unit.

    - Parameter `address` (`int`): The new I2C address to set for the unit.

### `EXTIO2Unit.get_config_mode(id)`

    Get the current configuration mode of a specific channel.

    - Parameter `id` (`int`): The channel ID to get the mode for.

### `EXTIO2Unit.read_input_pin(id)`

    Read the value of an input pin.

    - Parameter `id` (`int`): The pin ID to read the value from.

### `EXTIO2Unit.read_adc8_pin(id)`

    Read the 8-bit ADC value of a pin.

    - Parameter `id` (`int`): The pin ID to read the ADC value from.

### `EXTIO2Unit.read_adc12_pin(id)`

    Read the 12-bit ADC value of a pin.

    - Parameter `id` (`int`): The pin ID to read the ADC value from.

### `EXTIO2Unit.read_servo_angle(id)`

    Read the angle of a servo.

    - Parameter `id` (`int`): The servo ID to read the angle from.

### `EXTIO2Unit.read_servo_pulse(id)`

    Read the pulse width of a servo.

    - Parameter `id` (`int`): The servo ID to read the pulse width from.

### `EXTIO2Unit.read_rgb_led(id)`

    Read the RGB color value of a NeoPixel LED.

    - Parameter `id` (`int`): The NeoPixel ID to read the color from.

### `EXTIO2Unit.pin(id, mode, value)`

    Create and return a Pin object with the specified mode and value.

    - Parameter `id`: The pin ID to create the Pin object for.
    - Parameter `mode` (`int`): The mode to set for the pin (default is input).
    - Parameter `value`: The value to set for the pin, if applicable.
