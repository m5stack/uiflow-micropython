# DoF10 Unit

This library is the driver for Unit DoF10.

Support the following products:

    Unit DoF10

## MicroPython Example

#### Read Acceleration

This example shows how to read and display X, Y, and Z acceleration.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import Pin
from hardware import I2C
from unit import DoF10Unit
import time

page0 = None
title = None
unit_label = None
range_label = None
axis_x = None
axis_y = None
axis_z = None
slider_x = None
slider_y = None
slider_z = None
label_x_value = None
label_y_value = None
label_z_value = None
scale_low = None
scale_zero = None
scale_high = None
i2c0 = None
dof10_0 = None

last_time = None
UPDATE_DURATION_MS = None
accel = None

def setup():
    global \
        page0, \
        title, \
        unit_label, \
        range_label, \
        axis_x, \
        axis_y, \
        axis_z, \
        slider_x, \
        slider_y, \
        slider_z, \
        label_x_value, \
        label_y_value, \
        label_z_value, \
        scale_low, \
        scale_zero, \
        scale_high, \
        i2c0, \
        dof10_0, \
        last_time, \
        UPDATE_DURATION_MS, \
        accel

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0x10171D)
    title = m5ui.M5Label(
        "DoF10 / Accel Vector",
        x=12,
        y=8,
        text_c=0xF2F6F8,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    unit_label = m5ui.M5Label(
        "m/s2",
        x=274,
        y=11,
        text_c=0x4CD7D0,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_14,
        parent=page0,
    )
    range_label = m5ui.M5Label(
        "Range  -20.0 ~ +20.0",
        x=12,
        y=34,
        text_c=0x8FA1AD,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_12,
        parent=page0,
    )
    axis_x = m5ui.M5Label(
        "X",
        x=11,
        y=69,
        text_c=0xFF6B6B,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    axis_y = m5ui.M5Label(
        "Y",
        x=11,
        y=115,
        text_c=0x63D08C,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    axis_z = m5ui.M5Label(
        "Z",
        x=11,
        y=159,
        text_c=0x63A8FF,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_18,
        parent=page0,
    )
    slider_x = m5ui.M5Slider(
        x=44,
        y=70,
        w=200,
        h=10,
        mode=lv.slider.MODE.NORMAL,
        min_value=-200,
        max_value=200,
        value=0,
        bg_c=0x27323A,
        color=0xFF6B6B,
        parent=page0,
    )
    slider_y = m5ui.M5Slider(
        x=44,
        y=115,
        w=200,
        h=10,
        mode=lv.slider.MODE.NORMAL,
        min_value=-200,
        max_value=200,
        value=0,
        bg_c=0x27323A,
        color=0x63D08C,
        parent=page0,
    )
    slider_z = m5ui.M5Slider(
        x=44,
        y=160,
        w=200,
        h=10,
        mode=lv.slider.MODE.NORMAL,
        min_value=-200,
        max_value=200,
        value=0,
        bg_c=0x27323A,
        color=0x63A8FF,
        parent=page0,
    )
    label_x_value = m5ui.M5Label(
        "0.00",
        x=260,
        y=70,
        text_c=0xF2F6F8,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_y_value = m5ui.M5Label(
        "0.00",
        x=260,
        y=115,
        text_c=0xF2F6F8,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_z_value = m5ui.M5Label(
        "0.00",
        x=260,
        y=160,
        text_c=0xF2F6F8,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    scale_low = m5ui.M5Label(
        "-20",
        x=55,
        y=211,
        text_c=0x8FA1AD,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_12,
        parent=page0,
    )
    scale_zero = m5ui.M5Label(
        "0",
        x=153,
        y=211,
        text_c=0xF2F6F8,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_12,
        parent=page0,
    )
    scale_high = m5ui.M5Label(
        "+20",
        x=235,
        y=211,
        text_c=0x8FA1AD,
        bg_c=0x10171D,
        bg_opa=0,
        font=lv.font_montserrat_12,
        parent=page0,
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    dof10_0 = DoF10Unit(i2c0, addr=0x68)
    page0.screen_load()
    UPDATE_DURATION_MS = 100
    last_time = time.ticks_ms()

def loop():
    global \
        page0, \
        title, \
        unit_label, \
        range_label, \
        axis_x, \
        axis_y, \
        axis_z, \
        slider_x, \
        slider_y, \
        slider_z, \
        label_x_value, \
        label_y_value, \
        label_z_value, \
        scale_low, \
        scale_zero, \
        scale_high, \
        i2c0, \
        dof10_0, \
        last_time, \
        UPDATE_DURATION_MS, \
        accel
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= UPDATE_DURATION_MS:
        last_time = time.ticks_ms()
        accel = dof10_0.get_accel()
        slider_x.set_value(int(accel[0] * 10), True)
        label_x_value.set_text(str(round(accel[0], 2)))
        slider_y.set_value(int(accel[1] * 10), True)
        label_y_value.set_text(str(round(accel[1], 2)))
        slider_z.set_value(int(accel[2] * 10), True)
        label_z_value.set_text(str(round(accel[2], 2)))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### Read Barometer

This example shows how to read and display pressure, altitude, and temperature.

```python
import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from unit import DoF10Unit
import time

title = None
live = None
pressure_caption = None
label_pressure = None
pressure_unit = None
altitude_caption = None
label_altitude = None
altitude_unit = None
temperature_caption = None
label_temperature = None
temperature_unit = None
sea_level_caption = None
i2c0 = None
dof10_0 = None

UPDATE_DURATION_MS = None
last_time = None

def setup():
    global \
        title, \
        live, \
        pressure_caption, \
        label_pressure, \
        pressure_unit, \
        altitude_caption, \
        label_altitude, \
        altitude_unit, \
        temperature_caption, \
        label_temperature, \
        temperature_unit, \
        sea_level_caption, \
        i2c0, \
        dof10_0, \
        UPDATE_DURATION_MS, \
        last_time

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x10171D)
    title = Widgets.Label(
        "DoF10 / Barometer", 12, 8, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat18
    )
    live = Widgets.Label("Live", 272, 11, 1.0, 0x63D08C, 0x10171D, Widgets.FONTS.Montserrat14)
    pressure_caption = Widgets.Label(
        "Pressure", 12, 44, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_pressure = Widgets.Label(
        "----.--", 12, 62, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat40
    )
    pressure_unit = Widgets.Label(
        "hPa", 170, 84, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat18
    )
    altitude_caption = Widgets.Label(
        "Altitude", 12, 132, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_altitude = Widgets.Label(
        "---.-", 12, 151, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat24
    )
    altitude_unit = Widgets.Label(
        "m", 116, 158, 1.0, 0x63A8FF, 0x10171D, Widgets.FONTS.Montserrat18
    )
    temperature_caption = Widgets.Label(
        "SPL06 Temp", 170, 132, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_temperature = Widgets.Label(
        "--.-", 170, 151, 1.0, 0xFFB454, 0x10171D, Widgets.FONTS.Montserrat24
    )
    temperature_unit = Widgets.Label(
        "DEG C", 244, 158, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    sea_level_caption = Widgets.Label(
        "SEA LEVEL  1013.25 hPa", 12, 211, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=400000)
    dof10_0 = DoF10Unit(i2c0, addr=0x68)
    dof10_0.set_sea_level_pressure(1013.25)
    UPDATE_DURATION_MS = 100
    last_time = time.ticks_ms()

def loop():
    global \
        title, \
        live, \
        pressure_caption, \
        label_pressure, \
        pressure_unit, \
        altitude_caption, \
        label_altitude, \
        altitude_unit, \
        temperature_caption, \
        label_temperature, \
        temperature_unit, \
        sea_level_caption, \
        i2c0, \
        dof10_0, \
        UPDATE_DURATION_MS, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= UPDATE_DURATION_MS:
        last_time = time.ticks_ms()
        label_pressure.setText(str(round(dof10_0.get_pressure(), 2)))
        label_altitude.setText(str(round(dof10_0.get_altitude(), 1)))
        label_temperature.setText(str(round(dof10_0.get_temperature("pressure"), 1)))

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

#### DoF10Unit

## Constructors

### `class DoF10Unit(i2c, addr=0x68)`

    Create a DoF10Unit on the host I2C bus. The BMI270 address can be `0x68` or `0x69` (default: `0x68`). The BMM350 and SPL06-001 addresses remain `0x14` and `0x76`.

    - Parameter `i2c`: Initialized I2C or PAHUBUnit interface.
    - Type of `i2c`: I2C or PAHUBUnit
    - Parameter `addr` (`int`): BMI270 I2C address, 0x68 or 0x69. Defaults to 0x68.

```python
dof = DoF10Unit(i2c)  # Default BMI270 address: 0x68
# Use this instead when the BMI270 is configured at 0x69:
# dof = DoF10Unit(i2c, addr=0x69)
```
## Methods

The complete DoF10 interface is listed below.

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

### `get_temperature(sensor="pressure")`

    Return temperature in degrees Celsius. `sensor` accepts `"imu"`,
    `"magnetometer"`, or `"pressure"`; the default is `"pressure"`.

    - Parameter `sensor`: Temperature source.
    - Type of `sensor`: str
    - Returns: Temperature in degrees Celsius.
    - Return type: float

### `get_pressure()`

    Return compensated atmospheric pressure in `hPa`.

    - Returns: Pressure in hPa.
    - Return type: float

### `get_altitude()`

    Return barometric altitude in meters using the configured sea-level
    pressure.

    - Returns: Altitude in meters.
    - Return type: float

### `set_sea_level_pressure(pressure)`

    Set the sea-level reference pressure in `hPa`. The default is 1013.25.

    - Parameter `pressure`: Reference pressure in hPa.
    - Type of `pressure`: float

### `get_heading()`

    Sample motion and magnetic data and return tilt-compensated heading from 0
    to less than 360 degrees.

    - Returns: Heading in degrees.
    - Return type: float

### `get_attitude()`

    Sample motion and magnetic data and return `(yaw, pitch, roll)` in
    degrees.

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

    Set BMI270 output data rates using `ACCEL_ODR_VALUES` and
    `GYRO_ODR_VALUES`.

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
