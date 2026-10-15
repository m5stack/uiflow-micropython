# DoF6 Unit

This library is the driver for Unit DoF6.

Support the following products:

    Unit DoF6

## MicroPython Example

#### Read Attitude

This example shows how to read and display yaw, pitch, and roll.

```python
import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from unit import DoF6Unit
import time

title = None
live = None
yaw_caption = None
pitch_caption = None
roll_caption = None
label_yaw = None
label_pitch = None
label_roll = None
orientation_caption = None
degree_unit = None
sensor_caption = None
i2c0 = None
dof6_0 = None

last_time = None
UPDATE_DURATION_MS = None
attitude = None

def setup():
    global \
        title, \
        live, \
        yaw_caption, \
        pitch_caption, \
        roll_caption, \
        label_yaw, \
        label_pitch, \
        label_roll, \
        orientation_caption, \
        degree_unit, \
        sensor_caption, \
        i2c0, \
        dof6_0, \
        last_time, \
        UPDATE_DURATION_MS, \
        attitude

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x10171D)
    title = Widgets.Label(
        "DoF6 / Attitude", 12, 8, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat18
    )
    live = Widgets.Label("Live", 272, 11, 1.0, 0x63D08C, 0x10171D, Widgets.FONTS.Montserrat14)
    yaw_caption = Widgets.Label("Yaw", 12, 60, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14)
    pitch_caption = Widgets.Label(
        "Pitch", 113, 60, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    roll_caption = Widgets.Label(
        "Roll", 212, 60, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_yaw = Widgets.Label("---.-", 12, 84, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat24)
    label_pitch = Widgets.Label(
        "---.-", 112, 84, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat24
    )
    label_roll = Widgets.Label(
        "---.-", 212, 84, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat24
    )
    orientation_caption = Widgets.Label(
        "FUSED ORIENTATION", 12, 151, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    degree_unit = Widgets.Label(
        "DEG", 212, 151, 1.0, 0xFFB454, 0x10171D, Widgets.FONTS.Montserrat14
    )
    sensor_caption = Widgets.Label(
        "BMI270  /  6-AXIS", 12, 207, 1.0, 0x63A8FF, 0x10171D, Widgets.FONTS.Montserrat14
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    dof6_0 = DoF6Unit(i2c0, addr=0x68)
    UPDATE_DURATION_MS = 20
    last_time = time.ticks_ms()

def loop():
    global \
        title, \
        live, \
        yaw_caption, \
        pitch_caption, \
        roll_caption, \
        label_yaw, \
        label_pitch, \
        label_roll, \
        orientation_caption, \
        degree_unit, \
        sensor_caption, \
        i2c0, \
        dof6_0, \
        last_time, \
        UPDATE_DURATION_MS, \
        attitude
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= UPDATE_DURATION_MS:
        last_time = time.ticks_ms()
        attitude = dof6_0.get_attitude()
        label_yaw.setText(str(round(attitude[0], 1)))
        label_pitch.setText(str(round(attitude[1], 1)))
        label_roll.setText(str(round(attitude[2], 1)))

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

#### DoF6Unit

## Constructors

### `class DoF6Unit(i2c, addr=0x68)`

    Create a DoF6Unit on the host I2C bus. The BMI270 address can be `0x68` or `0x69` (default: `0x68`).

    - Parameter `i2c`: Initialized I2C or PAHUBUnit interface.
    - Type of `i2c`: I2C or PAHUBUnit
    - Parameter `addr` (`int`): BMI270 I2C address, 0x68 or 0x69. Defaults to 0x68.

```python
dof = DoF6Unit(i2c)  # Default BMI270 address: 0x68
# Use this instead when the BMI270 is configured at 0x69:
# dof = DoF6Unit(i2c, addr=0x69)
```
## Methods

### `get_accel()`

    Return mapped acceleration as `(x, y, z)` in `m/s2`. The full scale is
    selected by `set_accel_range`.

    - Returns: Acceleration tuple in m/s2.
    - Return type: tuple[float, float, float]

### `get_accel_raw()`

    Return signed 16-bit BMI270 counts from `-32768` to `32767`.

    - Returns: Raw acceleration counts.
    - Return type: tuple[int, int, int]

### `get_gyro()`

    Return mapped, offset-corrected angular velocity as `(x, y, z)` in
    `rad/s`.

    - Returns: Angular velocity tuple in rad/s.
    - Return type: tuple[float, float, float]

### `get_gyro_raw()`

    Return signed 16-bit BMI270 gyroscope counts from `-32768` to `32767`.

    - Returns: Raw gyroscope counts.
    - Return type: tuple[int, int, int]

### `get_temperature()`

    Return BMI270 temperature in degrees Celsius.

    - Returns: IMU temperature.
    - Return type: float

### `get_attitude()`

    Sample BMI270 and return fused `(yaw, pitch, roll)` in degrees.

    - Returns: Attitude angles in degrees.
    - Return type: tuple[float, float, float]

### `set_accel_range(accel_scale)`

    Set full scale to one of `ACCEL_RANGE_2G`, `ACCEL_RANGE_4G`,
    `ACCEL_RANGE_8G`, or `ACCEL_RANGE_16G`.

    - Parameter `accel_scale`: Full-scale range in g.
    - Type of `accel_scale`: int

### `set_gyro_range(gyro_scale)`

    Set full scale to one of `GYRO_RANGE_125DPS`, `GYRO_RANGE_250DPS`,
    `GYRO_RANGE_500DPS`, `GYRO_RANGE_1000DPS`, or `GYRO_RANGE_2000DPS`.

    - Parameter `gyro_scale`: Full-scale range in deg/s.
    - Type of `gyro_scale`: int

### `set_accel_gyro_odr(accel_odr, gyro_odr)`

    Set BMI270 ODR. `ACCEL_ODR_VALUES` is ``(0.78, 1.5, 3.1, 6.25, 12.5,
    25, 50, 100, 200, 400, 800, 1600)` Hz; `GYRO_ODR_VALUES` is `(25,
    50, 100, 200, 400, 800, 1600, 3200)`` Hz.

    - Parameter `accel_odr`: Accelerometer output data rate in Hz.
    - Type of `accel_odr`: float
    - Parameter `gyro_odr`: Gyroscope output data rate in Hz.
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

### `set_fusion_time_constant(seconds)`

    Set the non-negative complementary-filter time constant in seconds.

    - Parameter `seconds`: Non-negative filter time constant.
    - Type of `seconds`: float

### `reset_fusion()`

    Reset the attitude filter; the next attitude sample reinitializes it.

### `set_axis_mapping(sensor, x_axis, y_axis, z_axis)`

    Map `accelerometer` or `gyroscope` axes. Values `1/-1`, `2/-2`,
    and `3/-3` select source X/Y/Z with sign; source axes cannot repeat.

    - Parameter `sensor`: `"accelerometer"` or `"gyroscope"`.
    - Type of `sensor`: str
    - Parameter `x_axis`: Source axis for output X.
    - Type of `x_axis`: int
    - Parameter `y_axis`: Source axis for output Y.
    - Type of `y_axis`: int
    - Parameter `z_axis`: Source axis for output Z.
    - Type of `z_axis`: int
