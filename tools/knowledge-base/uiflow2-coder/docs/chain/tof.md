# Chain ToF

ToFChain is the helper class for ToF (Time of Flight) sensor devices on the Chain bus. It provides methods to read distance measurements, configure measurement parameters (time, mode, status), and check measurement completion status.

Support the following products:

    Chain ToF

## MicroPython Example

#### Distance measurement display

This example demonstrates how to read distance measurements from the Chain ToF sensor and display them on screen. The example configures the sensor for continuous measurement mode and updates the distance value in real-time.

```python
import os, sys, io
import M5
from M5 import *
from chain import ChainBus
from chain import ToFChain
import time

title0 = None
label_dis = None
bus2 = None
chain_tof_0 = None
last_time = None
distance = None

def setup():
    global title0, label_dis, bus2, chain_tof_0, last_time, distance

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Chain ToF Example", 3, 0xffffff, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_dis = Widgets.Label("Distance: --", 20, 92, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu24)

    bus2 = ChainBus(2, tx=21, rx=22)
    chain_tof_0 = ToFChain(bus2, 1)
    chain_tof_0.set_rgb_color(0x33ccff)
    chain_tof_0.set_rgb_brightness(10, save=False)
    chain_tof_0.set_measure_mode(ToFChain.MODE_CONTINUOUS)

def loop():
    global title0, label_dis, bus2, chain_tof_0, last_time, distance
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 200:
        last_time = time.ticks_ms()
        distance = chain_tof_0.get_distance()
        label_dis.setText(str((str('Distance: ') + str(((str(distance) + str(' mm')))))))

if __name__ == '__main__':
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

#### ToFChain

## `ToFChain`
ToF Chain class for interacting with ToF (Time of Flight) devices over Chain bus.

- Parameter `bus` (`ChainBus`): The Chain bus instance.
- Parameter `device_id` (`int`): The device ID of the ToF sensor on the Chain bus.

```python
from chain import ChainBus
from chain import ToFChain

bus2 = ChainBus(2, tx=21, rx=22)
chain_tof_0 = ToFChain(bus2, 1)
```

### `get_distance`
Get the distance measurement.

- Returns: Distance in millimeters, or None if failed.
- Return type: int

```python
distance = chain_tof_0.get_distance()
```

### `set_measure_time`
Set the measurement time.

- Parameter `time_ms` (`int`): Measurement time in milliseconds. Range: 20-200, default: 33.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_tof_0.set_measure_time(33)
```

### `get_measure_time`
Get the measurement time.

- Returns: Measurement time in milliseconds, or None if failed.
- Return type: int

```python
time = chain_tof_0.get_measure_time()
```

### `set_measure_mode`
Set the measurement mode.

- Parameter `mode` (`int`): Measurement mode. Use `ToFChain.MODE_STOP` (0), `ToFChain.MODE_SINGLE` (1), or `ToFChain.MODE_CONTINUOUS` (2). Default: 2.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_tof_0.set_measure_mode(ToFChain.MODE_CONTINUOUS)
```

### `get_measure_mode`
Get the measurement mode.

- Returns: Measurement mode. `ToFChain.MODE_STOP` (0), `ToFChain.MODE_SINGLE` (1), or `ToFChain.MODE_CONTINUOUS` (2). Returns None if failed.
- Return type: int

```python
mode = chain_tof_0.get_measure_mode()
```

### `set_measure_status`
Set the measurement status.

- Parameter `status` (`int`): Measurement status. 0 means not measuring, 1 means measuring.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_tof_0.set_measure_status(1)
```

### `get_measure_status`
Get the measurement status.

- Returns: Measurement status. 0 means not measuring, 1 means measuring. Returns None if failed.
- Return type: int

```python
status = chain_tof_0.get_measure_status()
```

### `get_measure_complete_flag`
Get the measurement complete flag.

- Returns: Measurement complete flag. 0 means measurement not complete, 1 means measurement complete. Returns None if failed.
- Return type: int

```python
flag = chain_tof_0.get_measure_complete_flag()
```
