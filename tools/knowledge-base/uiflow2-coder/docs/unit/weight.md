
# Weight Unit

Weight unit integrates a HX711 24 bits A/D chip that is specifically designed for electronic weighing device.

Support the following products:

WEIGHTUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from unit import WeightUnit
import time

title0 = None
label0 = None
weight_0 = None

def setup():
    global title0, label0, weight_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "WeightUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label(
        "weight value:", 4, 113, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    weight_0 = WeightUnit(port=(8, 9))
    weight_0.set_tare()

def loop():
    global title0, label0, weight_0
    M5.update()
    label0.setText(str((str("weight value:") + str((weight_0.get_scale_weight)))))
    time.sleep_ms(100)

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

## class WEIGHTUnit

## Constructors

### `class WEIGHTUnit(port)`

    Initialize the WEIGHTUnit with specified port pins.

    - Parameter `port`: A tuple containing data and clock pin numbers.

## Methods

### `WEIGHTUnit.get_raw_weight()`

    Read the raw weight value from the HX711.

### `WEIGHTUnit.get_scale_weight()`

    Get the scaled weight value based on calibration.

### `WEIGHTUnit.set_tare()`

    Set the tare weight to zero out the scale.

### `WEIGHTUnit.set_calibrate_scale(weight)`

    Calibrate the scale with a known weight.

    - Parameter `weight`: The known weight used for calibration.

### `WEIGHTUnit.is_ready_wait()`

    Check if the HX711 is ready to provide data.

### `WEIGHTUnit.set_channel(chan)`

    Set the channel for the HX711.

    - Parameter `chan` (`int`): The channel to set (1, 2, or 3).
