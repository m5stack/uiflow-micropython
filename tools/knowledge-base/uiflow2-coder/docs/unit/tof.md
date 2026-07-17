# ToF Unit

Support the following products:

    ToFUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ToFUnit

label0 = None
i2c0 = None
tof_0 = None

def setup():
    global label0, i2c0, tof_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 132, 109, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    tof_0 = ToFUnit(i2c0)

def loop():
    global label0, i2c0, tof_0
    M5.update()
    label0.setText(str((str((tof_0.get_range())) + str("mm"))))

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

## class ToFUnit

## Constructors

### `class ToFUnit(i2c: I2C, address: int = 0x29, io_timeout_ms: int = 0)`

    Create a DLight object.

    - Parameter `i2c`: the I2C object.
    - Parameter `address`: the I2C address of the device. Default is 0x23.
    - Parameter `io_timeout_ms`: the timeout of I2C communication. Default is 0ms.

## Methods

### `ToFUnit.get_distance() -> float`

    Get distance in centimeters.

    - Returns: distance in millimeters.

### `ToFUnit.get_data_ready() -> bool`

    Get data ready status.

    - Returns: data ready status.

### `ToFUnit.get_range() -> int`

    Get distance in millimeters.

    - Returns: distance in millimeters.

### `ToFUnit.is_continuous_mode() -> bool`

    Get continuous mode status.

    - Returns: continuous mode status.

### `ToFUnit.get_measurement_timing_budget() -> int`

    Get measurement timing budget. The budget is in microseconds.

    - Returns: measurement timing budget. The budget is in microseconds.

### `ToFUnit.set_measurement_timing_budget(budget_us: int) -> None`

    Set measurement timing budget. The budget_us is in microseconds.

    - Parameter `budget_us`: measurement timing budget in microseconds.

### `ToFUnit.get_signal_rate_limit() -> float`

    Get signal rate limit.

    - Returns: signal rate limit.

### `ToFUnit.set_signal_rate_limit(val: float) -> None`

    Set signal rate limit.

    - Parameter `val`: signal rate limit.

### `ToFUnit.start_continuous() -> None`

    Start continuous mode.

### `ToFUnit.stop_continuous() -> None`

    Stop continuous mode.

### `ToFUnit.set_address(new_address: int) -> None`

    Set I2C address.

    - Parameter `new_address`: new I2C address.
