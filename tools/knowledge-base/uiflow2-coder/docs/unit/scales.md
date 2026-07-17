
# Scales Unit

UNIT Scales is a high precision low-cost I2C port weighing sensor, with a total weighing range of 20kgs. Adopt STM32F030 as the controller, HX711 as sampling chip and 20 kgs weighing sensor. With tare button and programable RGB LED. This Unit offers the customer with a highly integrated weighing solution, suitable for the applications of weighing, item counting, item movement Checking and so on.

Support the following products:

ScalesUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ScalesUnit

title1 = None
label0 = None
label1 = None
i2c0 = None
scales_0 = None

def setup():
    global title1, label0, label1, i2c0, scales_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title1 = Widgets.Title(
        "ScaleUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 3, 89, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 3, 132, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    scales_0 = ScalesUnit(i2c0, 0x26)
    scales_0.set_rgb_led(0x6600CC)

def loop():
    global title1, label0, label1, i2c0, scales_0
    M5.update()
    if not (scales_0.get_button_status(2)):
        scales_0.set_current_raw_offset()
        label0.setText(str("Reset to zero"))
    else:
        label0.setText(str("Press Btn to reset"))
    label1.setText(
        str((str("Current weight:") + str((str((scales_0.get_scale_value(1))) + str("g")))))
    )

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

## class ScalesUnit

## Constructors

### `class ScalesUnit(i2c, address)`

    Initialize the ScalesUnit with I2C communication and an optional I2C address.

    - Parameter `i2c`: The I2C or PAHUBUnit instance for communication.
    - Parameter `address`: The I2C address or a list/tuple of addresses for the scales unit.

## Methods

### `ScalesUnit.get_button_status(status)`

    Retrieve the status of a button on the scales unit.

    - Parameter `status`: The button status identifier.

    - Returns: The current status of the specified button.

### `ScalesUnit.set_button_offset(enable)`

    Enable or disable the button offset for the scales unit.

    - Parameter `enable`: The offset enable value (1 to enable, 0 to disable).

### `ScalesUnit.set_rgbled_sync(control)`

    Set synchronization mode for the RGB LED.

    - Parameter `control`: The control value for synchronization.

### `ScalesUnit.get_rgbled_sync()`

    Retrieve the synchronization mode of the RGB LED.

    - Returns: The synchronization mode value.

### `ScalesUnit.set_rgb_led(rgb)`

    Set the RGB values for the LED.

    - Parameter `rgb`: The RGB value as a 24-bit integer.

### `ScalesUnit.get_rgb_led()`

    Retrieve the current RGB values of the LED.

    - Returns: A list containing the RGB values.

### `ScalesUnit.get_scale_value(scale)`

    Get the scale value for the specified scale type.

    - Parameter `scale`: The scale type identifier.

    - Returns: The scale value as an integer.

### `ScalesUnit.set_raw_offset(value)`

    Set the raw offset for the scales unit.

    - Parameter `value`: The raw offset value as an integer.

### `ScalesUnit.set_current_raw_offset()`

    Set the current raw offset value for the scales unit.

### `ScalesUnit.set_calibration_zero()`

    Calibrate the scales unit for zero weight.

### `ScalesUnit.set_calibration_load(gram)`

    Calibrate the scales unit with a specified weight.

    - Parameter `gram`: The weight value in grams for calibration.

### `ScalesUnit.get_device_inform(mode)`

    Get the device information for a specified mode.

    - Parameter `mode`: The mode identifier for the requested information.

    - Returns: The device information value.

### `ScalesUnit.set_i2c_address(addr)`

    Change the I2C address of the scales unit.

    - Parameter `addr`: The new I2C address value.
