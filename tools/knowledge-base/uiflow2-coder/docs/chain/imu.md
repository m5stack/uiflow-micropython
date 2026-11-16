# Chain IMU

<!-- .. Product SKU: U235. -->

This library is the driver for Chain IMU.

Support the following products:

    Chain IMU

## MicroPython Example

#### IMU sensor display

Connect Chain IMU as the first device on M5Stack Basic UART2 (TX=21, RX=22). The screen has a centered "Chain IMU" title, three X/Y/Z columns for acceleration (m/s2) and angular velocity (rad/s), and a temperature reading (degrees Celsius) at the bottom. Readings refresh every 100 ms. Acceleration and angular velocity are rounded to two decimal places, and temperature to one decimal place.

```python
import os, sys, io
import M5
from M5 import *
from chain import ChainBus
from chain import IMUChain
import time

title = None
accel_caption = None
accel_unit = None
x_caption = None
accel_x = None
y_caption = None
accel_y = None
z_caption = None
accel_z = None
gyro_caption = None
gyro_unit = None
gyro_x = None
gyro_y = None
gyro_z = None
temperature = None
bus2 = None
chain_imu_0 = None
accel = None
gyro = None
last_time = None

def setup():
    global \
        title, \
        accel_caption, \
        accel_unit, \
        x_caption, \
        accel_x, \
        y_caption, \
        accel_y, \
        z_caption, \
        accel_z, \
        gyro_caption, \
        gyro_unit, \
        gyro_x, \
        gyro_y, \
        gyro_z, \
        temperature, \
        bus2, \
        chain_imu_0, \
        accel, \
        gyro, \
        last_time

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x10171D)
    title = Widgets.Label("Chain IMU", 112, 8, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat18)
    accel_caption = Widgets.Label(
        "Acceleration", 12, 43, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    accel_unit = Widgets.Label(
        "m/s2", 200, 43, 1.0, 0x63A8FF, 0x10171D, Widgets.FONTS.Montserrat14
    )
    x_caption = Widgets.Label("X", 12, 65, 1.0, 0xFFB454, 0x10171D, Widgets.FONTS.Montserrat14)
    accel_x = Widgets.Label("--.--", 12, 86, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat24)
    y_caption = Widgets.Label("Y", 113, 65, 1.0, 0x63D08C, 0x10171D, Widgets.FONTS.Montserrat14)
    accel_y = Widgets.Label("--.--", 113, 86, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat24)
    z_caption = Widgets.Label("Z", 214, 65, 1.0, 0x63A8FF, 0x10171D, Widgets.FONTS.Montserrat14)
    accel_z = Widgets.Label("--.--", 214, 86, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat24)
    gyro_caption = Widgets.Label(
        "Angular velocity", 12, 131, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    gyro_unit = Widgets.Label(
        "rad/s", 200, 131, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat14
    )
    gyro_x = Widgets.Label("--.--", 12, 157, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat24)
    gyro_y = Widgets.Label("--.--", 113, 157, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat24)
    gyro_z = Widgets.Label("--.--", 214, 157, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat24)
    temperature = Widgets.Label(
        "Temperature  --.- C", 12, 212, 1.0, 0xFFB454, 0x10171D, Widgets.FONTS.Montserrat14
    )

    bus2 = ChainBus(2, tx=21, rx=22)
    chain_imu_0 = IMUChain(bus2, 1)
    title.setCursor(
        x=(int((320 - (M5.Display.textWidth("Chain IMU", Widgets.FONTS.Montserrat18))) / 2)), y=8
    )
    last_time = 0

def loop():
    global \
        title, \
        accel_caption, \
        accel_unit, \
        x_caption, \
        accel_x, \
        y_caption, \
        accel_y, \
        z_caption, \
        accel_z, \
        gyro_caption, \
        gyro_unit, \
        gyro_x, \
        gyro_y, \
        gyro_z, \
        temperature, \
        bus2, \
        chain_imu_0, \
        accel, \
        gyro, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        accel = chain_imu_0.read_accel()
        gyro = chain_imu_0.read_gyro()
        accel_x.setText(str(round(accel[0], 2)))
        gyro_x.setText(str(round(gyro[0], 2)))
        accel_y.setText(str(round(accel[1], 2)))
        gyro_y.setText(str(round(gyro[1], 2)))
        accel_z.setText(str(round(accel[2], 2)))
        gyro_z.setText(str(round(gyro[2], 2)))
        temperature.setText(
            str(
                (
                    str((str("Temperature  ") + str((round(chain_imu_0.read_temperature(), 1)))))
                    + str(" C")
                )
            )
        )
        last_time = time.ticks_ms()
    time.sleep_ms(10)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

## **API**

#### IMUChain

## `IMUChain`
Driver for Chain IMU.

### `read_accel`
Read three-axis acceleration in m/s^2, using standard gravity 9.80665 m/s^2.

- Returns: Tuple (x, y, z) of floats in m/s^2, resolution 0.00980665 m/s^2.
- Return type: tuple

```python
x, y, z = device.read_accel()
```

### `read_gyro`
Read the latest IMU sample. Firmware refreshes the sensor but can return the previous sample if that refresh fails.

- Returns: Tuple (x, y, z) of floats in rad/s, resolution pi/180 rad/s (about 0.0174533 rad/s).
- Return type: tuple

```python
xyz = device.read_gyro()
```

### `read_accel_raw`
Read the latest IMU sample. Firmware refreshes the sensor but can return the previous sample if that refresh fails.

- Returns: Tuple (x, y, z) of signed 16-bit raw sensor counts.
- Return type: tuple

```python
xyz = device.read_accel_raw()
```

### `read_gyro_raw`
Read the latest IMU sample. Firmware refreshes the sensor but can return the previous sample if that refresh fails.

- Returns: Tuple (x, y, z) of signed 16-bit raw sensor counts.
- Return type: tuple

```python
xyz = device.read_gyro_raw()
```

### `read_temperature`
Read IMU temperature. Firmware clamps temperatures below zero to 0 degrees Celsius; negative temperatures cannot be recovered through this command.

- Returns: Temperature in degrees Celsius, 0..655.35, resolution 0.01 degrees.
- Return type: float

```python
temperature = device.read_temperature()
```

### `set_accel_range`
Set acceleration full-scale range. The setting is volatile.

- Parameter `accel_scale`: An ACCEL_RANGE_* constant in ACCEL_RANGES, in g (2, 4, 8 or 16). Samples from read_accel() remain in m/s^2.
- Type of `accel_scale`: int or float
- Returns: No return value.
- Return type: None

```python
device.set_accel_range(IMUChain.ACCEL_RANGE_2G)
```

### `get_accel_range`
Get acceleration full-scale range.

- Returns: An ACCEL_RANGE_* constant in ACCEL_RANGES, in g (2, 4, 8 or 16). Samples from read_accel() remain in m/s^2.
- Return type: int or float

```python
value = device.get_accel_range()
```

### `set_gyro_range`
Set the gyroscope full-scale range. The setting is volatile.

- Parameter `gyro_scale`: A GYRO_RANGE_* constant in GYRO_RANGES, in degrees/s (125, 250, 500, 1000 or 2000). Samples from read_gyro() remain in rad/s.
- Type of `gyro_scale`: int
- Returns: No return value.
- Return type: None

```python
device.set_gyro_range(IMUChain.GYRO_RANGE_500DPS)
```

### `get_gyro_range`
Get the gyroscope full-scale range.

- Returns: Full-scale magnitude in degrees per second.
- Return type: int

```python
value = device.get_gyro_range()
```

### `set_accel_odr`
Set acceleration sampling rate. The setting is volatile.

- Parameter `accel_odr`: An ODR_* constant in ACCEL_ODR_VALUES, in Hz; ODR_POWER_DOWN (0) disables this channel.
- Type of `accel_odr`: int or float
- Returns: No return value.
- Return type: None

```python
device.set_accel_odr(IMUChain.ODR_104HZ)
```

### `get_accel_odr`
Get acceleration sampling rate.

- Returns: An ODR_* constant in ACCEL_ODR_VALUES, in Hz; ODR_POWER_DOWN (0) disables this channel.
- Return type: int or float

```python
value = device.get_accel_odr()
```

### `set_gyro_odr`
Set gyroscope sampling rate. The setting is volatile.

- Parameter `gyro_odr`: An ODR_* constant in GYRO_ODR_VALUES, in Hz; ODR_POWER_DOWN (0) disables this channel.
- Type of `gyro_odr`: int or float
- Returns: No return value.
- Return type: None

```python
device.set_gyro_odr(IMUChain.ODR_104HZ)
```

### `get_gyro_odr`
Get gyroscope sampling rate.

- Returns: An ODR_* constant in GYRO_ODR_VALUES, in Hz; ODR_POWER_DOWN (0) disables this channel.
- Return type: int or float

```python
value = device.get_gyro_odr()
```

### `set_alarm_mode`
Select the enabled alarm sources. Zero disables all alarms. The setting is volatile. Bits: 1 acceleration, 2 gyroscope, 4 temperature.

- Parameter `mode`: Alarm bitmask, 0..7; combine ALARM_* bits with `|`, use ALARM_NONE to disable or ALARM_ALL to enable all sources.
- Type of `mode`: int
- Returns: No return value.
- Return type: None

```python
device.set_alarm_mode(IMUChain.ALARM_ALL)
```

### `get_alarm_mode`
Get the enabled alarm sources.

- Returns: Alarm bitmask, 0..7; combine ALARM_* bits with `|`, use ALARM_NONE to disable or ALARM_ALL to enable all sources.
- Return type: int

```python
mode = device.get_alarm_mode()
```

### `set_motion_alarm_thresh`
Set motion delta thresholds. Firmware compares each axis against its moving reference and debounces transitions over five samples. The setting is volatile.

- Parameter `accel_mg`: Acceleration delta in mg, 0..255.
- Type of `accel_mg`: int
- Parameter `gyro_dps`: Angular velocity delta in degrees per second, 0..255.
- Type of `gyro_dps`: int
- Returns: No return value.
- Return type: None

```python
device.set_motion_alarm_thresh(100, 20)
```

### `get_motion_alarm_thresh`
Get motion delta thresholds.

- Returns: Tuple (accel_mg, gyro_dps), each 0..255.
- Return type: tuple

```python
accel_mg, gyro_dps = device.get_motion_alarm_thresh()
```

### `set_temperature_alarm_thresh`
Set the temperature alarm window. The setting is volatile.

- Parameter `Temperature in degrees Celsius. Range` (`low:`): 0..255; low must be less than high.
- Type of `low`: int
- Parameter `Temperature in degrees Celsius. Range` (`high:`): 0..255; low must be less than high.
- Type of `high`: int
- Returns: No return value.
- Return type: None

```python
device.set_temperature_alarm_thresh(10, 40)
```

### `get_temperature_alarm_thresh`
Get the temperature alarm window.

- Returns: Tuple (low, high). Temperature in degrees Celsius.
- Return type: tuple

```python
low, high = device.get_temperature_alarm_thresh()
```

### `deinit`
Detach the device and release all event callbacks; the shared bus stays open.

- Returns: No return value.
- Return type: None

### `set_event_callback`
Register a specific IMU alarm or recovery callback.

Use EVENT_ACCEL_TRIGGER/CLEAR, EVENT_GYRO_TRIGGER/CLEAR, or
EVENT_TEMPERATURE_HIGH/LOW/HIGH_CLEAR/LOW_CLEAR. Each handler receives
its selected event constant. None removes only that event handler.
Registration does not change alarm reporting. Enable alarms afterwards.
State tracking starts at zero when the first source is registered.
Recovery requires a prior alarm report, except explicit low recovery.
Legacy source selectors and the single-callback form receive raw status.
set_event_callback(None) removes all handlers.

- Parameter `An EVENT_* constant, legacy callback or None. Default` (`event:`): None.
- Type of `event`: int or callable or None
- Parameter `Handler receiving the selected event constant. Default` (`callback:`): None.
- Type of `callback`: callable or None
- Returns: No return value.
- Return type: None

```python
def on_accel(event):
    print(event)

device.set_event_callback(IMUChain.EVENT_ACCEL_TRIGGER, on_accel)
```

### `read_i2c_mem`
Read the internal sensor I2C register space through Chain. This may clear sensor status registers.

- Parameter `address`: Seven-bit internal I2C address, 0x08..0x77.
- Type of `address`: int
- Parameter `register`: Register address, 0..255 for addrsize=8 or 0..65535 for addrsize=16.
- Type of `register`: int
- Parameter `length`: Number of bytes, 1..64.
- Type of `length`: int
- Parameter `Register address width in bits, 8 or 16. Default` (`addrsize:`): 8.
- Type of `addrsize`: int
- Returns: Requested register bytes.
- Return type: bytes

```python
data = device.read_i2c_mem(address, register, 1)
```

### `write_i2c_mem`
Write the internal sensor I2C register space through Chain. Direct register writes can change measurement and alarm configuration; use sensor-specific configuration methods for normal operation.

- Parameter `address`: Seven-bit internal I2C address, 0x08..0x77.
- Type of `address`: int
- Parameter `register`: Register address, 0..255 for addrsize=8 or 0..65535 for addrsize=16.
- Type of `register`: int
- Parameter `data`: Buffer containing 1..64 bytes.
- Type of `data`: bytes or bytearray or memoryview
- Parameter `Register address width in bits, 8 or 16. Default` (`addrsize:`): 8.
- Type of `addrsize`: int
- Returns: No return value.
- Return type: None

```python
device.write_i2c_mem(address, register, data)
```

### `get_uid`
Read the device UID as bytes.

- Parameter `uid_type` (`int`): 0 for four bytes, 1 for twelve bytes. Default: 0.
- Returns: UID bytes, or empty bytes if communication fails.
- Return type: bytes
