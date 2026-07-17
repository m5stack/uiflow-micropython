# Accel Unit

This is the driver library of Accel Unit, which is used to obtain data from the
acceleration sensor and support motion detection.

Support the following products:

    ACCEL

## MicroPython Example

#### get accel value

This example gets the acceleration value of the Accel Unit and displays it on the screen.

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import AccelUnit

label0 = None
label1 = None
label2 = None
title0 = None
label3 = None
label4 = None
label5 = None
i2c0 = None
accel_0 = None

acc = None

def setup():
    global label0, label1, label2, title0, label3, label4, label5, i2c0, accel_0, acc

    M5.begin()
    label0 = Widgets.Label("x:", 4, 48, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("y:", 4, 88, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("z:", 4, 128, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title("ACCEL UNIT", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 24, 48, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("label4", 24, 88, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("label5", 24, 128, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    accel_0 = AccelUnit(i2c0, 0x53)

def loop():
    global label0, label1, label2, title0, label3, label4, label5, i2c0, accel_0, acc
    M5.update()
    acc = accel_0.get_accel()
    label3.setText(str(acc[0]))
    label4.setText(str(acc[1]))
    label5.setText(str(acc[2]))

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

#### AccelUnit

## `AccelUnit`
Create an AccelUnit object.

- Parameter `i2c` (`I2C`): The I2C bus the Accel Unit is connected to.
- Parameter `address` (`int`): The I2C address of the device. Default is 0x53.

```python
from hardware import I2C
from unit import AccelUnit

acceli2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
accel_0 = AccelUnit(i2c0)
```

### `get_accel`
The x, y, z acceleration values returned in a 3-tuple in :math:`m / s ^ 2`.

- Returns: x, y, z acceleration values in :math:`m / s ^ 2`.
- Return type: tuple[float, float, float]

```python
accel_0.get_accel()
```

### `enable_motion_detection`
The activity detection parameters.

- Parameter `threshold` (`int`): The value that acceleration on any axis must
                      exceed to register as active. The scale factor is
                      62.5 mg/LSB.

If you wish to set them yourself rather than using the defaults,
you must use keyword arguments:
```
accelerometer.enable_motion_detection(threshold=20)
```

```python
accel_0.enable_motion_detection(threshold=18)
```

### `disable_motion_detection`
Disable motion detection.

```python
accel_0.disable_motion_detection()
```

### `get_data_rate`
Get the data rate of the sensor.

- Returns: The data rate of the sensor.
- Return type: int

Rate options are:

    - `0`: 0.1 Hz
    - `1`: 0.20 Hz
    - `2`: 0.39 Hz
    - `3`: 0.78 Hz
    - `4`: 1.56 Hz
    - `5`: 3.13 Hz
    - `6`: 6.25 Hz
    - `7`: 12.5 Hz
    - `8`: 25 Hz
    - `9`: 50 Hz
    - `10`: 100 Hz
    - `11`: 200 Hz
    - `12`: 400 Hz
    - `13`: 800 Hz
    - `14`: 1600 Hz
    - `15`: 3200 Hz

```python
accel_0.get_data_rate()
```

### `set_data_rate`
Set the data rate of the sensor.

- Parameter `rate` (`int`): The data rate of the sensor.

Rate options are:

    - `0`: 0.1 Hz
    - `1`: 0.20 Hz
    - `2`: 0.39 Hz
    - `3`: 0.78 Hz
    - `4`: 1.56 Hz
    - `5`: 3.13 Hz
    - `6`: 6.25 Hz
    - `7`: 12.5 Hz
    - `8`: 25 Hz
    - `9`: 50 Hz
    - `10`: 100 Hz
    - `11`: 200 Hz
    - `12`: 400 Hz
    - `13`: 800 Hz
    - `14`: 1600 Hz
    - `15`: 3200 Hz

```python
accel_0.set_data_rate(accel_0.RATE_3200_HZ)
```

### `get_range`
Get the measurement range of the sensor.

- Returns: The measurement range of the sensor.
- Return type: int

Range options are:

    - `0`: 2G
    - `1`: 4G
    - `2`: 8G
    - `3`: 16G

```python
accel_0.get_range()
```

### `set_range`
The measurement range of the sensor.

- Parameter `range` (`int`): The measurement range of the sensor.

Range options are:

    - `0`: 2G
    - `1`: 4G
    - `2`: 8G
    - `3`: 16G

```python
accel_0.set_range(accel_0.RANGE_2_G)
```

### `is_tap`
Returns True if a tap has been detected.

- Returns: True if a tap has been detected.
- Return type: bool

```python
accel_0.is_tap()
```

### `is_motion`
Returns True if motion has been detected.

- Returns: True if motion has been detected.
- Return type: bool

```python
accel_0.is_motion()
```

### `is_freefall`
Returns True if freefall has been detected.

- Returns: True if freefall has been detected.
- Return type: bool

```python
accel_0.is_freefall()
```

### `enable_freefall_detection`
Freefall detection parameters:

- Parameter `threshold` (`int`): The value that acceleration on all axes must be
                      under to register as dropped. The scale factor
                      is 62.5 mg/LSB.

- Parameter `time` (`int`): The amount of time that acceleration on all axes must be
                 less than `threshold` to register as dropped. The scale
                 factor is 5 ms/LSB. Values between 100 ms and 350 ms
                 (20 to 70) are recommended.

If you wish to set them yourself rather than using the defaults,
you must use keyword arguments:

```python
accelerometer.enable_freefall_detection(time=30)
```

```python
accel_0.enable_freefall_detection()
```

### `disable_freefall_detection`
Disable freefall detection.

```python
accel_0.disable_freefall_detection()
```

### `enable_tap_detection`
The tap detection parameters.

- Parameter `tap_count` (`int`): 1 to detect only single taps, and 2 to detect only
                    double taps.

- Parameter `threshold` (`int`): A threshold for the tap detection. The scale factor is
                    62.5 mg/LSB The higher the value the less sensitive
                    the detection.

- Parameter `duration` (`int`): This caps the duration of the impulse above
                    `threshold`. Anything above `duration` won't
                    register as a tap. The scale factor is 625 µs/LSB.

- Parameter `latency` (`int`): (double tap only) The length of time after the initial
                    impulse falls below `threshold` to start the window
                    looking for a second impulse. The scale factor is
                    1.25 ms/LSB.

- Parameter `window` (`int`): (double tap only) The length of the window in which to
                look for a second tap. The scale factor is 1.25 ms/LSB.

If you wish to set them yourself rather than using the defaults,
you must use keyword arguments:

```python
accelerometer.enable_tap_detection(duration=30, threshold=25)
```

```python
accel_0.enable_tap_detection(tap_count=1, threshold=20, duration=50, latency=20, window=255)
```

### `disable_tap_detection`
Disable tap detection.

```python
accel_0.disable_tap_detection()
```

#### ADXL345

## `ADXL345`
`ADXL345` is an alias of `ADXL345` in `m5stack/libs/driver/adxl34x.py`.

Driver for the ADXL345 3 axis accelerometer.

- Parameter `i2c` (`I2C`): The I2C bus the ADXL345 is connected to.
- Parameter `address` (`int`): The I2C device address for the sensor. Default is

**Quickstart: Importing and using the device**

    Here is an example of using the `ADXL345` class.
    First you will need to import the libraries to use the sensor:

```python
import machine
import adxl34x
```
    Once this is done you can define your `I2C` object and define your
    sensor object:

```python
i2c = machine.I2C(0)  # uses board default SDA and SCL pins
accelerometer = adxl34x.ADXL343(i2c)
```
    Now you have access to the `acceleration` attribute:

```python
acceleration = accelerometer.acceleration
```

### `acceleration`
The x, y, z acceleration values returned in a 3-tuple in :math:`m / s ^ 2`.

### `raw_x`
The raw x value.

### `raw_y`
The raw y value.

### `raw_z`
The raw z value.

### `events`
that has been enabled.

The possible keys are:

 Key         Description                                                                |
| `tap`    | True if a tap was detected recently. Whether it's looking for a single or  |
             double tap is determined by the tap param of `enable_tap_detection`.       |
| `motion`  True if the sensor has seen acceleration above the threshold
             set with `enable_motion_detection`.                                        |
|`freefall` True if the sensor was in freefall. Parameters are set when enabled with
             `enable_freefall_detection`.                                               |

### `enable_motion_detection`
The activity detection parameters.

- Parameter `threshold` (`int`): The value that acceleration on any axis must
                      exceed to register as active. The scale factor
                      is 62.5 mg/LSB.

If you wish to set them yourself rather than using the defaults,
you must use keyword arguments:

```python
accelerometer.enable_motion_detection(threshold=20)
```

### `disable_motion_detection`
Disable motion detection.

### `enable_freefall_detection`
Freefall detection parameters:

- Parameter `threshold` (`int`): The value that acceleration on all axes must be
                      under to register as dropped. The scale factor is
                      62.5 mg/LSB.

- Parameter `time` (`int`): The amount of time that acceleration on all axes must
                 be less than `threshold` to register as dropped. The
                 scale factor is 5 ms/LSB. Values between 100 ms and
                 350 ms (20 to 70) are recommended.

If you wish to set them yourself rather than using the defaults,
you must use keyword arguments:

```python
accelerometer.enable_freefall_detection(time=30)
```

### `disable_freefall_detection`
Disable freefall detection.

### `enable_tap_detection`
The tap detection parameters.

- Parameter `tap_count` (`int`): 1 to detect only single taps, and 2 to detect only
                      double taps.

- Parameter `threshold` (`int`): A threshold for the tap detection. The scale
                      factor is 62.5 mg/LSB The higher the value the
                      less sensitive the detection.

- Parameter `duration` (`int`): This caps the duration of the impulse above
                     `threshold`. Anything above `duration` won't
                     register as a tap. The scale factor is 625 µs/LSB.

- Parameter `latency` (`int`): (double tap only) The length of time after the
                    initial impulse falls below `threshold` to start
                    the window looking for a second impulse. The scale
                    factor is 1.25 ms/LSB.

- Parameter `window` (`int`): (double tap only) The length of the window in which
                   to look for a second tap. The scale factor is
                   1.25 ms/LSB.

If you wish to set them yourself rather than using the defaults,
you must use keyword arguments:

```python
accelerometer.enable_tap_detection(duration=30, threshold=25)
```

### `disable_tap_detection`
Disable tap detection.

### `data_rate`
The data rate of the sensor.

### `data_rate`

### `range`
The measurement range of the sensor.

### `range`

### `offset`
The x, y, z offsets as a tuple of raw count values.

See offset_calibration example for usage.

### `offset`
