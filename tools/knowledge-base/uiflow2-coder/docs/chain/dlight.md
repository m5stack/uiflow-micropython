# Chain DLight

<!-- .. Product SKU: U236. -->

This library is the driver for Chain DLight.

Support the following products:

    Chain DLight

## MicroPython Example

#### DLight illuminance display

Connect Chain DLight as the first device on M5Stack Basic UART2 (TX=21, RX=22). The screen displays the live illuminance in lux.

```python
import os, sys, io
import M5
from M5 import *
from chain import ChainBus
from chain import DLightChain
import time

label_title = None
label_lux = None
bus2 = None
chain_dlight_0 = None
reading = None

def setup():
    global label_title, label_lux, bus2, chain_dlight_0, reading

    M5.begin()
    Widgets.setRotation(1)
    label_title = Widgets.Label(
        "Chain DLight", 83, 12, 1.0, 0x33CCFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_lux = Widgets.Label(
        "-- Lux", 96, 100, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat40
    )

    label_title.setCursor(
        x=(int((320 - (M5.Display.textWidth("Chain DLight", Widgets.FONTS.Montserrat24))) / 2)),
        y=12,
    )
    bus2 = ChainBus(2, tx=21, rx=22)
    chain_dlight_0 = DLightChain(bus2, 1)

def loop():
    global label_title, label_lux, bus2, chain_dlight_0, reading
    M5.update()
    reading = str((chain_dlight_0.read_lux())) + str(" Lux")
    label_lux.setText(str(""))
    label_lux.setCursor(
        x=(int((320 - (M5.Display.textWidth(reading, Widgets.FONTS.Montserrat40))) / 2)),
        y=(int((240 - (M5.Display.fontHeight(Widgets.FONTS.Montserrat40))) / 2)),
    )
    label_lux.setText(str(reading))
    time.sleep_ms(250)

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

#### DLightChain

## `DLightChain`
Driver for Chain DLight.

### `deinit`
Detach the device and release all callbacks; the shared bus stays open.

Repeated calls are safe. Returns None.

### `read_lux`
Read the most recent illuminance sample. The firmware returns its cached sample.

- Returns: Illuminance in lux, 0..2516580.
- Return type: int

```python
lux = device.read_lux()
```

### `enable_threshold_detection`
Enable sensor threshold detection; changing this gate resets the firmware threshold history. Repeated calls are safe. The setting is volatile.

- Returns: No return value.
- Return type: None

```python
device.enable_threshold_detection()
```

### `disable_threshold_detection`
Disable sensor threshold detection; changing this gate resets the firmware threshold history. Repeated calls are safe. The setting is volatile.

- Returns: No return value.
- Return type: None

```python
device.disable_threshold_detection()
```

### `is_threshold_detection_enabled`
Check whether sensor threshold detection is enabled.

- Returns: True if enabled, otherwise False.
- Return type: bool

```python
enabled = device.is_threshold_detection_enabled()
```

### `set_alarm_thresh`
Set the illuminance alarm threshold window. The firmware briefly restarts measurement and resets the threshold history. The setting is volatile.

- Parameter `low`: Lower threshold in lux, 0..2516580; must be less than high.
- Type of `low`: int
- Parameter `high`: Upper threshold in lux, 0..2516580; must be greater than low.
- Type of `high`: int
- Returns: No return value.
- Return type: None

```python
device.set_alarm_thresh(100, 1000)
```

### `get_alarm_thresh`
Get the configured illuminance alarm threshold window.

- Returns: Tuple (low, high), in lux.
- Return type: tuple

```python
low, high = device.get_alarm_thresh()
```

### `set_gain`
Set measurement gain. The setting is volatile. Measurement restarts and thresholds are reapplied.

- Parameter `Gain multiplier` (`value:`): GAIN_1X, GAIN_3X, GAIN_6X, GAIN_9X or GAIN_18X.
- Type of `value`: int or float
- Returns: No return value.
- Return type: None

```python
device.set_gain(DLightChain.GAIN_1X)
```

### `get_gain`
Get measurement gain.

- Returns: Gain multiplier: GAIN_1X, GAIN_3X, GAIN_6X, GAIN_9X or GAIN_18X.
- Return type: int

```python
value = device.get_gain()
```

### `set_resolution`
Set measurement resolution. The setting is volatile. The current interval must strictly exceed the conversion time: 16/17/18/19/20 bits require 25/50/100/200/400 ms respectively. The firmware rejects incompatible combinations.

- Parameter `A RESOLUTION_*BIT constant, in bits` (`value:`): 16, 17, 18, 19 or 20.
- Type of `value`: int or float
- Returns: No return value.
- Return type: None

```python
device.set_measurement_interval_ms(DLightChain.MEASUREMENT_INTERVAL_500MS)
device.set_resolution(DLightChain.RESOLUTION_20BIT)
```

### `get_resolution`
Get measurement resolution.

- Returns: A RESOLUTION_*BIT constant, in bits: 16, 17, 18, 19 or 20.
- Return type: int

```python
value = device.get_resolution()
```

### `set_measurement_interval_ms`
Set measurement interval. The setting is volatile. The interval must strictly exceed the conversion time: 20/19/18/17/16 bits require 400/200/100/50/25 ms respectively. Use 500 ms or longer for any resolution. The unsupported 25 ms setting is rejected before I/O.

- Parameter `A MEASUREMENT_INTERVAL_*MS constant` (`value:`): 50, 100, 500, 1000 or 2000 ms.
- Type of `value`: int or float
- Returns: No return value.
- Return type: None

```python
device.set_measurement_interval_ms(DLightChain.MEASUREMENT_INTERVAL_500MS)
```

### `get_measurement_interval_ms`
Get measurement interval.

- Returns: Interval in milliseconds. Allowed: (25, 50, 100, 500, 1000, 2000).
- Return type: int

```python
value = device.get_measurement_interval_ms()
```

### `enable_event_reporting`
Enable threshold event reporting; sensor threshold detection must also be enabled. Repeated calls are safe. The setting is volatile.

- Returns: No return value.
- Return type: None

```python
device.enable_event_reporting()
```

### `disable_event_reporting`
Disable threshold event reporting. Repeated calls are safe. The setting is volatile.

- Returns: No return value.
- Return type: None

```python
device.disable_event_reporting()
```

### `is_event_reporting_enabled`
Check whether threshold event reporting is enabled. Events require both reporting and threshold detection to be enabled.

- Returns: True if enabled, otherwise False.
- Return type: bool

```python
enabled = device.is_event_reporting_enabled()
```

### `set_event_callback`
Register a threshold callback without changing hardware reporting gates.

set_event_callback(EVENT_LOW/HIGH, callback) replaces only that event's
handler; None removes it. Callbacks receive the event integer. The legacy
set_event_callback(callback) form replaces all handlers with one handler
for both events; set_event_callback(None) removes all handlers. The two
forms replace one another. Do not call Chain methods inside a callback.

- Parameter `event`: EVENT_LOW (0), EVENT_HIGH (1), or a legacy callback/None.
- Type of `event`: int or callable or None
- Parameter `callback`: Event handler, or the legacy keyword handler when event is None.
- Type of `callback`: callable or None
- Returns: No return value.
- Return type: None

```python
device.set_event_callback(lambda event: print(event))
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
