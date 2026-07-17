# Chain Mic

MicChain is the helper class for microphone devices on the Chain bus. It provides methods to read ADC values, configure threshold values, set trigger cycle, and monitor microphone trigger events.

Support the following products:

    Chain Mic

## MicroPython Example

#### Microphone sound detection

This example demonstrates how to read ADC values from the Chain Mic sensor and monitor sound detection.

```python
import os, sys, io
import M5
from M5 import *
from chain import MicChain
import time
from chain import ChainBus

title0 = None
label_adc = None
label_status = None
bus2 = None
chain_mic_0 = None
last_trigger_time = None

def chain_mic_0_low_to_high_event(args):
    global title0, label_adc, label_status, bus2, chain_mic_0, last_trigger_time
    last_trigger_time = time.ticks_ms()
    label_status.setVisible(True)

def chain_mic_0_high_to_low_event(args):
    global title0, label_adc, label_status, bus2, chain_mic_0, last_trigger_time
    last_trigger_time = time.ticks_ms()
    label_status.setVisible(True)

def setup():
    global title0, label_adc, label_status, bus2, chain_mic_0, last_trigger_time

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("Chain MIC Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_adc = Widgets.Label("ADC: --", 95, 76, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu24)
    label_status = Widgets.Label(
        "voice trigger", 82, 158, 1.0, 0x4CEB18, 0x000000, Widgets.FONTS.DejaVu24
    )
    bus2 = ChainBus(2, tx=21, rx=22)
    chain_mic_0 = MicChain(bus2, 1)
    chain_mic_0.set_trigger_callback(MicChain.TRIGGER_LOW_TO_HIGH, chain_mic_0_low_to_high_event)
    chain_mic_0.set_trigger_callback(MicChain.TRIGGER_HIGH_TO_LOW, chain_mic_0_high_to_low_event)
    chain_mic_0.set_trigger(True)
    chain_mic_0.set_rgb_color(0x000064)
    label_status.setVisible(False)

def loop():
    global title0, label_adc, label_status, bus2, chain_mic_0, last_trigger_time
    M5.update()
    label_adc.setText(str((str("ADC: ") + str((chain_mic_0.get_adc12())))))
    time.sleep_ms(100)
    if (time.ticks_diff((time.ticks_ms()), last_trigger_time)) > 3000:
        label_status.setVisible(False)

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

#### MicChain

## `MicChain`
Mic Chain class for interacting with microphone devices over Chain bus.

- Parameter `bus` (`ChainBus`): The Chain bus instance.
- Parameter `device_id` (`int`): The device ID of the microphone on the Chain bus.

```python
from chain import ChainBus
from chain import MicChain

bus2 = ChainBus(2, tx=21, rx=22)
chain_mic_0 = MicChain(bus2, 1)
```

### `get_adc8`
Get the 8-bit ADC value of the microphone.

- Returns: 8-bit ADC value (0-255), or None if failed.
- Return type: int

```python
value = chain_mic_0.get_adc8()
```

### `get_adc12`
Get the 12-bit ADC value of the microphone.

- Returns: 12-bit ADC value (0-4095), or None if failed.
- Return type: int

```python
value = chain_mic_0.get_adc12()
```

### `set_trigger`
Enable or disable threshold-triggered reporting.

- Parameter `enable` (`bool`): True to enable threshold-triggered reporting, False to disable it.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_mic_0.set_trigger(True)
```

### `get_trigger`
Get whether threshold-triggered reporting is enabled.

- Returns: True if threshold-triggered reporting is enabled, False if disabled. Returns False if failed.
- Return type: bool

```python
enabled = chain_mic_0.get_trigger()
```

### `set_trigger_thresh`
Set the microphone trigger threshold.

- Parameter `threshold` (`int`): Threshold value (0-4095).
- Parameter `save` (`bool`): Whether to save the threshold to flash. Default: False.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_mic_0.set_trigger_thresh(2000, True)
```

### `get_trigger_thresh`
Get the microphone trigger threshold.

- Returns: Threshold value (0-4095), or None if failed.
- Return type: int

```python
threshold = chain_mic_0.get_trigger_thresh()
```

### `set_trigger_interval`
Set the minimum trigger interval (debounce time).

- Parameter `interval_ms` (`int`): Minimum time interval between triggers in milliseconds. Range: 300-1000.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_mic_0.set_trigger_interval(500)  # Set 500ms minimum interval between triggers
```

### `get_trigger_interval`
Get the minimum trigger interval (debounce time).

- Returns: Minimum trigger interval in milliseconds, or None if failed.
- Return type: int

```python
interval = chain_mic_0.get_trigger_interval()
```

### `set_trigger_callback`
Set callback for microphone trigger events.

- Parameter `trigger_type` (`int`): Trigger type to listen for. Use `MicChain.TRIGGER_LOW_TO_HIGH` (0) or `MicChain.TRIGGER_HIGH_TO_LOW` (1).
- Parameter `callback`: Callback function that will be called when microphone triggers.

> Note: Chain related methods cannot be called in the callback function.

```python
def mic_trigger_callback():
    print("Sound detected")

# Listen for low-to-high trigger only
chain_mic_0.set_trigger_callback(MicChain.TRIGGER_LOW_TO_HIGH, mic_trigger_callback)

# Listen for high-to-low trigger only
chain_mic_0.set_trigger_callback(MicChain.TRIGGER_HIGH_TO_LOW, mic_trigger_callback)
```

    For other button and some general methods, please refer to the `ChainKey <chain.key.KeyChain>` class.
