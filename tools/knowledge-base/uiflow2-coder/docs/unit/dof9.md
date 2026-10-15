# DoF9 Unit

This library is the driver for Unit DoF9.

Support the following products:

    Unit DoF9

## MicroPython Example

#### Read Heading

This example shows how to read and display the heading.

```python
import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from unit import DoF9Unit
import time

title = None
live = None
heading_caption = None
label_heading = None
degree_unit = None
compensation_caption = None
sensor_caption = None
i2c0 = None
dof9_0 = None

last_time = None
UPDATE_DURATION_MS = None

def setup():
    global \
        title, \
        live, \
        heading_caption, \
        label_heading, \
        degree_unit, \
        compensation_caption, \
        sensor_caption, \
        i2c0, \
        dof9_0, \
        last_time, \
        UPDATE_DURATION_MS

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x10171D)
    title = Widgets.Label(
        "DoF9 / Compass", 12, 8, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat18
    )
    live = Widgets.Label("Live", 272, 11, 1.0, 0x63D08C, 0x10171D, Widgets.FONTS.Montserrat14)
    heading_caption = Widgets.Label(
        "Magnetic Heading", 12, 48, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_heading = Widgets.Label(
        "---.-", 12, 70, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat40
    )
    degree_unit = Widgets.Label(
        "DEG", 174, 91, 1.0, 0xFFB454, 0x10171D, Widgets.FONTS.Montserrat18
    )
    compensation_caption = Widgets.Label(
        "TILT COMPENSATED", 12, 153, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    sensor_caption = Widgets.Label(
        "BMI270 + BMM350", 12, 207, 1.0, 0x63A8FF, 0x10171D, Widgets.FONTS.Montserrat14
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    dof9_0 = DoF9Unit(i2c0, addr=0x68)
    UPDATE_DURATION_MS = 100
    last_time = time.ticks_ms()

def loop():
    global \
        title, \
        live, \
        heading_caption, \
        label_heading, \
        degree_unit, \
        compensation_caption, \
        sensor_caption, \
        i2c0, \
        dof9_0, \
        last_time, \
        UPDATE_DURATION_MS
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= UPDATE_DURATION_MS:
        last_time = time.ticks_ms()
        label_heading.setText(str(round(dof9_0.get_heading(), 1)))

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

#### DoF9Unit

## Constructors

### `class DoF9Unit(i2c, addr=0x68)`

    Create a DoF9Unit on the host I2C bus. The BMI270 address can be `0x68` or `0x69` (default: `0x68`). The BMM350 address remains `0x14`.

    - Parameter `i2c`: Initialized I2C or PAHUBUnit interface.
    - Type of `i2c`: I2C or PAHUBUnit
    - Parameter `addr` (`int`): BMI270 I2C address, 0x68 or 0x69. Defaults to 0x68.

```python
dof = DoF9Unit(i2c)  # Default BMI270 address: 0x68
# Use this instead when the BMI270 is configured at 0x69:
# dof = DoF9Unit(i2c, addr=0x69)
```
## Methods

The complete DoF9 interface is listed below.

### `get_accel()`

    Return mapped acceleration as `(x, y, z)` in `m/s2`.

    - Returns: Acceleration tuple.
    - Return type: tuple[float, float, float]

### `get_accel_raw()`

    Return signed 16-bit BMI270 counts from `-32768` to `32767`.

    - Returns: Raw acceleration counts.
    - Return type: tuple[int, int, int]

### `get_gyro()`

    Return mapped, offset-corrected angular velocity as `(x, y, z)` in
    `rad/s`.

    - Returns: Angular velocity tuple.
    - Return type: tuple[float, float, float]

### `get_gyro_raw()`

    Return signed 16-bit BMI270 gyroscope counts from `-32768` to `32767`.

    - Returns: Raw gyroscope counts.
    - Return type: tuple[int, int, int]

### `get_mag()`

    Return mapped and calibrated magnetic field as `(x, y, z)` in `uT`.

    - Returns: Magnetic field tuple.
    - Return type: tuple[float, float, float]

### `get_mag_raw()`

    Return signed 24-bit BMM350 counts from `-8388608` to `8388607`.

    - Returns: Raw magnetic field counts.
    - Return type: tuple[int, int, int]

### `get_temperature(sensor="imu")`

    Return BMI270 or BMM350 temperature in degrees Celsius. `sensor` is
    `"imu"` or `"magnetometer"`.

    - Parameter `sensor`: Temperature source.
    - Type of `sensor`: str
    - Returns: Temperature in degrees Celsius.
    - Return type: float

### `get_heading()`

    Sample the sensors and return tilt-compensated heading from 0 to less than
    360 degrees.

    - Returns: Heading in degrees.
    - Return type: float

### `get_attitude()`

    Sample the sensors and return `(yaw, pitch, roll)` in degrees.

    - Returns: Attitude angles in degrees.
    - Return type: tuple[float, float, float]

### `set_accel_range(accel_scale)`

    Set one of `ACCEL_RANGE_2G`, `ACCEL_RANGE_4G`, `ACCEL_RANGE_8G`, or
    `ACCEL_RANGE_16G`.

    - Parameter `accel_scale`: Full-scale range in g.
    - Type of `accel_scale`: int

### `set_gyro_range(gyro_scale)`

    Set one of `GYRO_RANGE_125DPS`, `GYRO_RANGE_250DPS`, `GYRO_RANGE_500DPS`,
    `GYRO_RANGE_1000DPS`, or `GYRO_RANGE_2000DPS`.

    - Parameter `gyro_scale`: Full-scale range in deg/s.
    - Type of `gyro_scale`: int

### `set_accel_gyro_odr(accel_odr, gyro_odr)`

    Set BMI270 ODR using `ACCEL_ODR_VALUES` and `GYRO_ODR_VALUES`.

    - Parameter `accel_odr`: Accelerometer ODR in Hz.
    - Type of `accel_odr`: float
    - Parameter `gyro_odr`: Gyroscope ODR in Hz.
    - Type of `gyro_odr`: int

### `set_gyro_offsets(x, y, z)`

    Set mapped gyroscope offsets in `rad/s`.

    - Parameter `x`: X-axis offset in rad/s.
    - Type of `x`: float
    - Parameter `y`: Y-axis offset in rad/s.
    - Type of `y`: float
    - Parameter `z`: Z-axis offset in rad/s.
    - Type of `z`: float

### `calibrate_gyro(samples=32)`

    Estimate offsets while stationary and return `True` on success.

    - Parameter `samples`: Number of samples.
    - Type of `samples`: int
    - Returns: Whether calibration succeeded.
    - Return type: bool

### `set_magnetometer_calibration(offsets, scales)`

    Set hard-iron offsets in `uT` and unitless soft-iron scale factors.

    - Parameter `offsets`: Three hard-iron offsets in uT.
    - Type of `offsets`: tuple[float, float, float]
    - Parameter `scales`: Three positive scale factors.
    - Type of `scales`: tuple[float, float, float]

### `set_axis_mapping(sensor, x_axis, y_axis, z_axis)`

    Map `accelerometer`, `gyroscope`, or `magnetometer` axes. Values
    `1/-1`, `2/-2`, and `3/-3` select source X/Y/Z with sign; source axes
    cannot repeat.

    - Parameter `sensor`: Sensor name.
    - Type of `sensor`: str
    - Parameter `x_axis`: Source axis for output X.
    - Type of `x_axis`: int
    - Parameter `y_axis`: Source axis for output Y.
    - Type of `y_axis`: int
    - Parameter `z_axis`: Source axis for output Z.
    - Type of `z_axis`: int

### `set_fusion_time_constant(seconds)`

    Set the non-negative complementary-filter time constant in seconds.

    - Parameter `seconds`: Non-negative filter time constant.
    - Type of `seconds`: float

### `reset_fusion()`

    Reset the attitude filter; the next attitude sample reinitializes it.
