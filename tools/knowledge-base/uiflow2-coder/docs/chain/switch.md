# Chain Switch

SwitchChain is the helper class for switch devices on the Chain bus. It provides methods to read ADC values (12-bit and 8-bit), configure switch thresholds, set slip mode, and monitor switch status changes.

Support the following products:

    Chain Switch

## MicroPython Example

#### Switch status monitoring

This example demonstrates how to read ADC values and switch status from the Chain Switch sensor and display them on screen. It registers open/close trigger callbacks and updates the status label when the switch state changes.

```python
import os, sys, io
import M5
from M5 import *
from chain import SwitchChain
from chain import ChainBus

title0 = None
label_adc = None
label_state = None
bus2 = None
chain_switch_0 = None

def chain_switch_0_open_event(args):
    global title0, label_adc, label_state, bus2, chain_switch_0
    label_state.setText(str("State: Open"))

def chain_switch_0_close_event(args):
    global title0, label_adc, label_state, bus2, chain_switch_0
    label_state.setText(str("State: Close"))

def setup():
    global title0, label_adc, label_state, bus2, chain_switch_0

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("Chain Switch Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_adc = Widgets.Label("ADC: --", 20, 70, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu24)
    label_state = Widgets.Label(
        "State: --", 20, 113, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu24
    )

    bus2 = ChainBus(2, tx=21, rx=22)
    chain_switch_0 = SwitchChain(bus2, 1)
    chain_switch_0.set_trigger_callback(SwitchChain.STATUS_OPEN, chain_switch_0_open_event)
    chain_switch_0.set_trigger_callback(SwitchChain.STATUS_CLOSE, chain_switch_0_close_event)
    chain_switch_0.set_trigger(True)
    if chain_switch_0.get_switch_status():
        label_state.setText(str("State: Open"))
    else:
        label_state.setText(str("State: Close"))

def loop():
    global title0, label_adc, label_state, bus2, chain_switch_0
    M5.update()
    label_adc.setText(str((str("ADC: ") + str((chain_switch_0.get_adc12())))))

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

#### SwitchChain

## `SwitchChain`
Switch Chain class for interacting with switch devices over Chain bus.

- Parameter `bus` (`ChainBus`): The Chain bus instance.
- Parameter `device_id` (`int`): The device ID of the switch on the Chain bus.

```python
from chain import ChainBus
from chain import SwitchChain

bus2 = ChainBus(2, tx=21, rx=22)
chain_switch_0 = SwitchChain(bus2, 1)
```

### `get_adc12`
Get the 12-bit ADC value of the switch.

- Returns: 12-bit ADC value (0-4095), or None if failed.
- Return type: int

```python
value = chain_switch_0.get_adc12()
```

### `get_adc8`
Get the 8-bit ADC value of the switch.

- Returns: 8-bit ADC value (0-255), or None if failed.
- Return type: int

```python
value = chain_switch_0.get_adc8()
```

### `set_slip_mode`
Set the slider change mode.

- Parameter `mode` (`int`): Slider change mode. Use `SwitchChain.SLIP_MODE_DOWNUP_DEC` (0) for decreasing or `SwitchChain.SLIP_MODE_DOWNUP_INC` (1) for increasing.
- Parameter `save` (`bool`): Whether to save the setting to flash. Default: False.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_switch_0.set_slip_mode(SwitchChain.SLIP_MODE_DOWNUP_INC, True)
```

### `get_slip_mode`
Get the slider change mode.

- Returns: Slider change mode. `SwitchChain.SLIP_MODE_DOWNUP_DEC` (0) for decreasing or `SwitchChain.SLIP_MODE_DOWNUP_INC` (1) for increasing. Returns None if failed.
- Return type: int

```python
mode = chain_switch_0.get_slip_mode()
```

### `set_switch_thresh`
Set the switch open and close thresholds.

- Parameter `open_threshold` (`int`): Open threshold value (0-4095). Must be greater than close_threshold.
- Parameter `close_threshold` (`int`): Close threshold value (0-4095). Must be less than open_threshold.
- Parameter `save` (`bool`): Whether to save the threshold to flash. Default: False.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_switch_0.set_switch_thresh(3000, 1000, True)
```

### `get_open_thresh`
Get the switch open threshold.

- Returns: Open threshold value (0-4095), or None if failed.
- Return type: int

```python
open_th = chain_switch_0.get_open_thresh()
```

### `get_close_thresh`
Get the switch close threshold.

- Returns: Close threshold value (0-4095), or None if failed.
- Return type: int

```python
close_th = chain_switch_0.get_close_thresh()
```

### `get_switch_status`
Get the switch status.

- Returns: Switch status. 0 means close, 1 means open. Returns None if failed.
- Return type: int

```python
status = chain_switch_0.get_switch_status()
```

### `set_trigger`
Enable or disable status change reporting.

- Parameter `enable` (`bool`): True to enable status change reporting, False to disable it.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_switch_0.set_trigger(True)
```

### `get_trigger`
Get whether status change reporting is enabled.

- Returns: True if status change reporting is enabled, False if disabled. Returns False if failed.
- Return type: bool

```python
enabled = chain_switch_0.get_trigger()
```

### `set_trigger_callback`
Set callback for switch status change events.

- Parameter `trigger_type` (`int`): Trigger type to listen for. Use `SwitchChain.STATUS_CLOSE` (0) or `SwitchChain.STATUS_OPEN` (1).
- Parameter `callback`: Callback function that will be called when switch status changes.

> Note: Chain related methods cannot be called in the callback function.

```python
def switch_status_callback():
    print("Switch opened")

# Listen for open status only
chain_switch_0.set_trigger_callback(SwitchChain.STATUS_OPEN, switch_status_callback)

# Listen for close status only
chain_switch_0.set_trigger_callback(SwitchChain.STATUS_CLOSE, switch_status_callback)
```

    For other button and some general methods, please refer to the `ChainKey <chain.key.KeyChain>` class.
