
# NECO Unit

The Neco Unit is a unique RGB light board unit that features an adorable cat ear shape. It is designed with precision and comprises 35 WS2812C-2020 RGB lamp beads, providing vibrant and customizable lighting effects.

Support the following products:

NECOUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import NECOUnit

title0 = None
i2c0 = None
neco_0 = None

def setup():
    global title0, i2c0, neco_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "NECOUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    neco_0 = NECOUnit((1, 2), 70, True)
    neco_0.set_brightness(3)

def loop():
    global title0, i2c0, neco_0
    M5.update()
    neco_0.set_random_color_random_led_from(0, 70)

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

## class NECOUnit

## Constructors

### `class NECOUnit(port, number, active_low)`

    Initialize the NECOUnit with a specific port, LED count, and active low configuration for the button.

    - Parameter `port` (`tuple`): A tuple containing the port information, where the first element is for the button and the second is for the WS2812 LEDs.
    - Parameter `number` (`int`): The number of LEDs in the WS2812 strip. Default is 70.
    - Parameter `active_low` (`bool`): Boolean flag indicating whether the button is active low. Default is True.

## Methods

### `NECOUnit.set_color_from(begin, end, rgb, per_delay)`

    Set the color for a range of LEDs from the begin index to the end index with a specified color.

    - Parameter `begin` (`int`): The starting LED index.
    - Parameter `end` (`int`): The ending LED index.
    - Parameter `rgb` (`int`): The color to set, in RGB format.
    - Parameter `per_delay` (`int`): The delay between setting each LED's ;s color, in milliseconds. Default is 0.

### `NECOUnit.set_color_saturation_from(begin, end, rgb, per_delay)`

    Set the color saturation for a range of LEDs from the begin index to the end index with a specified color and saturation.

    - Parameter `begin` (`int`): The starting LED index.
    - Parameter `end` (`int`): The ending LED index.
    - Parameter `rgb` (`int`): The base color in RGB format.
    - Parameter `per_delay` (`int`): The delay between setting each LED's ;s color, in milliseconds. Default is 0.

### `NECOUnit.color_saturation(rgb, saturation)`

    Adjust the color saturation of an RGB color.

    - Parameter `rgb` (`int`): The base color in RGB format.
    - Parameter `saturation` (`float`): The desired saturation level (0 to 100).

    - Returns: The new color with adjusted saturation, in RGB format.

### `NECOUnit.set_color_running_from(begin, end, rgb, per_delay)`

    Set the color for a range of LEDs from the begin index to the end index, then clear them one by one, creating a running effect.

    - Parameter `begin` (`int`): The starting LED index.
    - Parameter `end` (`int`): The ending LED index.
    - Parameter `rgb` (`int`): The color to set, in RGB format.
    - Parameter `per_delay` (`int`): The delay between setting and clearing each LED's ;s color, in milliseconds. Default is 0.

### `NECOUnit.set_random_color_random_led_from(begin, end)`

    Set a random color to each LED in a random order within the specified range.

    - Parameter `begin` (`int`): The starting LED index.
    - Parameter `end` (`int`): The ending LED index.

### `NECOUnit.fill(v)`

    Fill the entire NECOUnit strip with the specified color.

    - Parameter `v` (`int`): A tuple containing the RGB (or RGBW) values to fill the strip with.

### `NECOUnit.set_color(i, c)`

    Set the color of the LED at the specified index.

    - Parameter `i`: The index of the LED to set.
    - Parameter `c` (`int`): The color value to set the LED to (in RGB or RGBW format).

### `NECOUnit.fill_color(c)`

    Fill the entire NECOUnit strip with the specified color.

    - Parameter `c` (`int`): The color value to fill the strip with (in RGB or RGBW format).

### `NECOUnit.set_brightness(br)`

    Set the brightness for the NECOUnit strip.

    - Parameter `br` (`int`): The brightness level as a percentage (0-100).
