
# Fader Unit

UNIT FADER is a Slide Potentiometer with color indicator, employ a 35mm slide potentiometer + 14x SK6812 programmable RGB lights. The fader has its own center point positioning, and excellent slide appliances for stable, reliable performance and precise control. The integrated beads support digital addressing, which means you can adjust the brightness and color of each LED light. The product is suitable for lighting, music control, and other applications.

Support the following products:

    FaderUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import FaderUnit

label0 = None
label1 = None
label2 = None
label3 = None
fader_0 = None

def setup():
    global label0, label1, label2, label3, fader_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Voltage:", 50, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("ADC:", 50, 140, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 160, 80, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 160, 140, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    fader_0 = FaderUnit((8, 9))

def loop():
    global label0, label1, label2, label3, fader_0
    M5.update()
    fader_0.update_color()
    label2.setText(str(fader_0.get_voltage()))
    label3.setText(str(fader_0.get_raw()))

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

## class FaderUnit

## Constructors

### `FaderUnit(port: tuple)`

    Initialize the Fader.

    - Parameter `port` (`tuple`): The port to which the Fader is connected. port[0]: adc pin, port[1]: LEDs pin.

## Methods

### `FaderUnit.get_voltage() -> float`

    Get the voltage of the Fader.

    - Returns: The voltage of the Fader.

### `FaderUnit.get_raw() -> int`

    Read the raw value of the ADC.

    - Returns: int from 0 to 65535.

### `FaderUnit.update_color() -> None`

    Update the color based on adc value.

### `FaderUnit.update_brightness() -> None`

    Update the brightness based on adc value.

### `FaderUnit.set_brightness(br: int)`

    This method is used to set the brightness of RGB lamp beads, and the setting range is 0-100.

### `FaderUnit.fill_color(c: int)`

    This method is used to set the color of all RGB lamp beads, and the input value is 3-byte RGB888.

### `FaderUnit.set_color(i, c: int)`

    This method is used to set the specified RGB lamp bead color. The input value is the lamp bead index and 3-byte RGB888.
