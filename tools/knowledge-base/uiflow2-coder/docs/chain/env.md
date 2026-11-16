# Chain ENV

<!-- .. Product SKU: U234. -->

This library is the driver for Chain ENV.

Support the following products:

    Chain ENV

## MicroPython Example

#### Environmental readings

Connect Chain ENV as the first device on M5Stack Basic UART2 (TX=21, RX=22). The screen displays temperature (degrees Celsius), humidity (%), pressure (hPa), and altitude (m), refreshed every 500 ms. Set SEA_LEVEL_PRESSURE_PA to the current local sea-level pressure. The initial Shenzhen test reference is 101330 Pa (1013.3 hPa).

```python
import os, sys, io
import M5
from M5 import *
import time
from chain import ChainBus
from chain import ENVChain

title = None
pressure_caption = None
label_pressure = None
pressure_unit = None
temperature_caption = None
label_temperature = None
temperature_unit = None
humidity_caption = None
label_humidity = None
humidity_unit = None
altitude_caption = None
label_altitude = None
altitude_unit = None
sea_level_caption = None
bus2 = None
chain_env_0 = None

SEA_LEVEL_PRESSURE_PA = None
UPDATE_INTERVAL_MS = None
last_time = None

def setup():
    global \
        title, \
        pressure_caption, \
        label_pressure, \
        pressure_unit, \
        temperature_caption, \
        label_temperature, \
        temperature_unit, \
        humidity_caption, \
        label_humidity, \
        humidity_unit, \
        altitude_caption, \
        label_altitude, \
        altitude_unit, \
        sea_level_caption, \
        bus2, \
        chain_env_0, \
        SEA_LEVEL_PRESSURE_PA, \
        UPDATE_INTERVAL_MS, \
        last_time

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x10171D)
    title = Widgets.Label("Chain ENV", 111, 8, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat18)
    pressure_caption = Widgets.Label(
        "Pressure", 12, 44, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_pressure = Widgets.Label(
        "----.-", 12, 62, 1.0, 0xF2F6F8, 0x10171D, Widgets.FONTS.Montserrat40
    )
    pressure_unit = Widgets.Label(
        "hPa", 170, 84, 1.0, 0x4CD7D0, 0x10171D, Widgets.FONTS.Montserrat18
    )
    temperature_caption = Widgets.Label(
        "Temperature", 12, 118, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_temperature = Widgets.Label(
        "--.-", 12, 137, 1.0, 0xFFB454, 0x10171D, Widgets.FONTS.Montserrat24
    )
    temperature_unit = Widgets.Label(
        "C", 80, 144, 1.0, 0xFFB454, 0x10171D, Widgets.FONTS.Montserrat18
    )
    humidity_caption = Widgets.Label(
        "Humidity", 170, 118, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_humidity = Widgets.Label(
        "--.-", 170, 137, 1.0, 0x63D08C, 0x10171D, Widgets.FONTS.Montserrat24
    )
    humidity_unit = Widgets.Label(
        "%", 225, 144, 1.0, 0x63D08C, 0x10171D, Widgets.FONTS.Montserrat18
    )
    altitude_caption = Widgets.Label(
        "Altitude", 12, 180, 1.0, 0x8FA1AD, 0x10171D, Widgets.FONTS.Montserrat14
    )
    label_altitude = Widgets.Label(
        "----.-", 100, 173, 1.0, 0x63A8FF, 0x10171D, Widgets.FONTS.Montserrat24
    )
    altitude_unit = Widgets.Label(
        "m", 200, 180, 1.0, 0x63A8FF, 0x10171D, Widgets.FONTS.Montserrat18
    )
    sea_level_caption = Widgets.Label(
        "Sea level / Shenzhen: -- hPa",
        12,
        215,
        1.0,
        0x8FA1AD,
        0x10171D,
        Widgets.FONTS.Montserrat14,
    )

    title.setCursor(
        x=(int((320 - (M5.Display.textWidth("Chain ENV", Widgets.FONTS.Montserrat18))) / 2)), y=8
    )
    SEA_LEVEL_PRESSURE_PA = 101330
    UPDATE_INTERVAL_MS = 500
    bus2 = ChainBus(2, tx=21, rx=22)
    chain_env_0 = ENVChain(bus2, 1)
    chain_env_0.set_sea_level_pressure(SEA_LEVEL_PRESSURE_PA)
    sea_level_caption.setText(
        str(
            (
                str((str("Sea level / Shenzhen: ") + str((SEA_LEVEL_PRESSURE_PA / 100))))
                + str(" hPa")
            )
        )
    )
    label_pressure.setText(str(round((chain_env_0.read_pressure()) / 100, 1)))
    label_temperature.setText(
        str(round(chain_env_0.read_temperature(sensor=ENVChain.SENSOR_AHT20), 1))
    )
    label_humidity.setText(str(round(chain_env_0.read_humidity(), 1)))
    label_altitude.setText(str(round(chain_env_0.read_altitude(), 1)))
    last_time = time.ticks_ms()

def loop():
    global \
        title, \
        pressure_caption, \
        label_pressure, \
        pressure_unit, \
        temperature_caption, \
        label_temperature, \
        temperature_unit, \
        humidity_caption, \
        label_humidity, \
        humidity_unit, \
        altitude_caption, \
        label_altitude, \
        altitude_unit, \
        sea_level_caption, \
        bus2, \
        chain_env_0, \
        SEA_LEVEL_PRESSURE_PA, \
        UPDATE_INTERVAL_MS, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= UPDATE_INTERVAL_MS:
        label_pressure.setText(str(round((chain_env_0.read_pressure()) / 100, 1)))
        label_temperature.setText(
            str(round(chain_env_0.read_temperature(sensor=ENVChain.SENSOR_AHT20), 1))
        )
        label_humidity.setText(str(round(chain_env_0.read_humidity(), 1)))
        label_altitude.setText(str(round(chain_env_0.read_altitude(), 1)))
        last_time = time.ticks_ms()
    time.sleep_ms(20)

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

#### ENVChain

## `ENVChain`
Driver for Chain ENV.

### `read_temperature_humidity`
Read one AHT20 temperature and humidity sample.

- Returns: Tuple (temperature, humidity), in degrees Celsius and percent.
- Return type: tuple

```python
temperature, humidity = device.read_temperature_humidity()
```

### `read_pressure_temperature_altitude`
Read one SPA06 sample. Altitude uses the configured sea-level pressure.

- Returns: Tuple (temperature, pressure, altitude), in degrees Celsius, Pa and metres. Pressure resolution is 10 Pa; altitude resolution is 0.01 m.
- Return type: tuple

```python
temperature, pressure, altitude = device.read_pressure_temperature_altitude()
```

### `read_temperature`
Read temperature from the selected sensor.

- Parameter `Temperature source` (`sensor:`): SENSOR_AHT20 (0) or SENSOR_SPA06 (1). Default: SENSOR_AHT20 (0).
- Type of `sensor`: int
- Returns: Temperature in degrees Celsius, resolution 0.01 degrees.
- Return type: float

```python
temperature = device.read_temperature(ENVChain.SENSOR_AHT20)
```

### `read_humidity`
Read humidity.

- Returns: Relative humidity in percent, 0..100.
- Return type: int

```python
value = device.read_humidity()
```

### `read_pressure`
Read pressure.

- Returns: Pressure in Pa, resolution 10 Pa.
- Return type: int

```python
value = device.read_pressure()
```

### `read_altitude`
Read altitude.

- Returns: Altitude in metres, resolution 0.01 m.
- Return type: float

```python
value = device.read_altitude()
```

### `set_temperature_rate`
Set SPA06 temperature sampling rate.

- Parameter `value`: An ODR_* constant in ODR_VALUES, in Hz; applies to SPA06 only.
- Type of `value`: int or float
- Returns: No return value.
- Return type: None

```python
device.set_temperature_rate(ENVChain.ODR_16HZ)
```

### `get_temperature_rate`
Get SPA06 temperature sampling rate.

- Returns: An ODR_* constant in ODR_VALUES, in Hz; applies to SPA06 only.
- Return type: int or float

```python
value = device.get_temperature_rate()
```

### `set_pressure_rate`
Set SPA06 pressure sampling rate.

- Parameter `value`: An ODR_* constant in ODR_VALUES, in Hz; applies to SPA06 only.
- Type of `value`: int or float
- Returns: No return value.
- Return type: None

```python
device.set_pressure_rate(ENVChain.ODR_16HZ)
```

### `get_pressure_rate`
Get SPA06 pressure sampling rate.

- Returns: An ODR_* constant in ODR_VALUES, in Hz; applies to SPA06 only.
- Return type: int or float

```python
value = device.get_pressure_rate()
```

### `set_sea_level_pressure`
Set the reference pressure for altitude calculation.

- Parameter `pressure`: Sea-level pressure in Pa, 70000..120000, in steps of 10 Pa.
- Type of `pressure`: int or float
- Returns: No return value.
- Return type: None

```python
device.set_sea_level_pressure(101330)
```

### `get_sea_level_pressure`
Get the reference pressure for altitude calculation.

- Returns: Sea-level pressure in Pa, resolution 10 Pa.
- Return type: int

```python
pressure = device.get_sea_level_pressure()
```

### `set_alarm_mode`
Select the enabled alarm sources. Zero disables all alarms. Bits: 1 temperature, 2 humidity, 4 pressure, 8 altitude.

- Parameter `mode`: Alarm bitmask, 0..15; combine ALARM_* bits with `|`, use ALARM_NONE to disable or ALARM_ALL to enable all sources.
- Type of `mode`: int
- Returns: No return value.
- Return type: None

```python
device.set_alarm_mode(ENVChain.ALARM_ALL)
```

### `get_alarm_mode`
Get the enabled alarm sources.

- Returns: Alarm bitmask, 0..15; combine ALARM_* bits with `|`, use ALARM_NONE to disable or ALARM_ALL to enable all sources.
- Return type: int

```python
mode = device.get_alarm_mode()
```

### `set_temperature_alarm_thresh`
Set the temperature alarm window and source.

- Parameter `low`: Lower temperature in degrees Celsius, 0..255; less than high.
- Type of `low`: int
- Parameter `high`: Upper temperature in degrees Celsius, 0..255; greater than low.
- Type of `high`: int
- Parameter `Temperature source` (`sensor:`): SENSOR_AHT20 (0) or SENSOR_SPA06 (1). Default: SENSOR_AHT20 (0).
- Type of `sensor`: int
- Returns: No return value.
- Return type: None

```python
device.set_temperature_alarm_thresh(10, 40)
```

### `get_temperature_alarm_thresh`
Get the temperature alarm window and source.

- Returns: Tuple (low, high, sensor); temperatures in degrees Celsius.
- Return type: tuple

```python
low, high, sensor = device.get_temperature_alarm_thresh()
```

### `set_humidity_alarm_thresh`
Set the humidity alarm window.

- Parameter `Relative humidity in percent. Range` (`low:`): 0..100; low must be less than high.
- Type of `low`: int
- Parameter `Relative humidity in percent. Range` (`high:`): 0..100; low must be less than high.
- Type of `high`: int
- Returns: No return value.
- Return type: None

```python
device.set_humidity_alarm_thresh(20, 80)
```

### `get_humidity_alarm_thresh`
Get the humidity alarm window.

- Returns: Tuple (low, high). Relative humidity in percent.
- Return type: tuple

```python
low, high = device.get_humidity_alarm_thresh()
```

### `set_pressure_alarm_thresh`
Set the pressure alarm window.

- Parameter `Pressure in Pa, resolution 10 Pa. Range` (`low:`): 70000..120000; low must be less than high.
- Type of `low`: int or float
- Parameter `Pressure in Pa, resolution 10 Pa. Range` (`high:`): 70000..120000; low must be less than high.
- Type of `high`: int or float
- Returns: No return value.
- Return type: None

```python
device.set_pressure_alarm_thresh(95000, 105000)
```

### `get_pressure_alarm_thresh`
Get the pressure alarm window.

- Returns: Tuple (low, high). Pressure in Pa, resolution 10 Pa.
- Return type: tuple

```python
low, high = device.get_pressure_alarm_thresh()
```

### `set_altitude_alarm_thresh`
Set the altitude alarm window.

- Parameter `Altitude in metres, resolution 0.01 m. Range` (`low:`): -21474836.48..21474836.47; low must be less than high.
- Type of `low`: int or float
- Parameter `Altitude in metres, resolution 0.01 m. Range` (`high:`): -21474836.48..21474836.47; low must be less than high.
- Type of `high`: int or float
- Returns: No return value.
- Return type: None

```python
device.set_altitude_alarm_thresh(0, 1000)
```

### `get_altitude_alarm_thresh`
Get the altitude alarm window.

- Returns: Tuple (low, high). Altitude in metres, resolution 0.01 m.
- Return type: tuple

```python
low, high = device.get_altitude_alarm_thresh()
```

### `deinit`
Detach the device and release its callbacks; the shared bus stays open.

- Returns: None. Repeated calls are safe.
- Return type: None

### `set_event_callback`
Register a high, low, high-clear or low-clear alarm callback.

Use EVENT_<SOURCE>_HIGH, LOW, HIGH_CLEAR or LOW_CLEAR. Each handler
receives its selected event constant. Register before enabling alarms.
Registration does not change hardware settings. Perform I/O in the loop.
HIGH_CLEAR requires only that source enabled via set/get_alarm_mode();
its source cannot be identified with multiple alarms enabled.
Legacy source selectors and the single-callback form receive raw status.

- Parameter `event`: An EVENT_* constant, legacy callback or None. Default None.
    None clears all handlers.
- Type of `event`: int or callable or None
- Parameter `callback`: Handler receiving the selected event constant.
    Default None removes the selected source's handler.
- Type of `callback`: callable or None
- Returns: None. Each source's handler can be replaced independently.
- Return type: None

```python
device.set_event_callback(ENVChain.EVENT_HUMIDITY_HIGH, on_humidity)
```

### `read_i2c_mem`
Read the internal sensor I2C register space through Chain. This may clear sensor status registers.

- Parameter `address`: Seven-bit internal I2C address, 0..127.
- Type of `address`: int
- Parameter `register`: Register address, 0..255 for addrsize=8 or 0..65535 for addrsize=16.
- Type of `register`: int
- Parameter `length`: Number of bytes, 1..32.
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

- Parameter `address`: Seven-bit internal I2C address, 0..127.
- Type of `address`: int
- Parameter `register`: Register address, 0..255 for addrsize=8 or 0..65535 for addrsize=16.
- Type of `register`: int
- Parameter `data`: Buffer containing 1..32 bytes.
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
