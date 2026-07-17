# Chain PIR

PIRChain is the helper class for PIR (Passive Infrared) sensor devices on the Chain bus. It provides methods to read IR induction values, configure trigger delay, and monitor PIR trigger events.

Support the following products:

    Chain PIR

## MicroPython Example

#### PIR motion detection

This example demonstrates how to use trigger callbacks from the Chain PIR sensor to update motion status on screen. It enables trigger auto-send, configures trigger hold time, and counts the detected duration while motion is active.

```python
import os, sys, io
import M5
from M5 import *
from chain import PIRChain
from chain import ChainBus
import time

title0 = None
label_status = None
label_count = None
bus2 = None
chain_pir_0 = None
detected = None
count = None
last_time = None
trigger_hold_time = None

def chain_pir_0_motion_detected_event(args):
    global \
        title0, \
        label_status, \
        label_count, \
        bus2, \
        chain_pir_0, \
        detected, \
        count, \
        last_time, \
        trigger_hold_time
    print("detect motion")
    detected = True
    count = 0
    label_status.setText(str("Status: detected"))
    label_status.setColor(0x009900, 0x000000)
    label_count.setVisible(True)

def chain_pir_0_motion_ended_event(args):
    global \
        title0, \
        label_status, \
        label_count, \
        bus2, \
        chain_pir_0, \
        detected, \
        count, \
        last_time, \
        trigger_hold_time
    print("not detect")
    detected = False
    label_status.setText(str("Status: no detect"))
    label_status.setColor(0xCCCCCC, 0x000000)
    label_count.setVisible(False)

def setup():
    global \
        title0, \
        label_status, \
        label_count, \
        bus2, \
        chain_pir_0, \
        detected, \
        count, \
        last_time, \
        trigger_hold_time

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("Chain PIR Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_status = Widgets.Label(
        "Status: --", 20, 70, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu24
    )
    label_count = Widgets.Label(
        "Count: --", 20, 165, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.DejaVu24
    )

    bus2 = ChainBus(2, tx=21, rx=22)
    chain_pir_0 = PIRChain(bus2, 1)
    chain_pir_0.set_trigger_callback(
        PIRChain.TRIGGER_MOTION_DETECTED, chain_pir_0_motion_detected_event
    )
    chain_pir_0.set_trigger_callback(PIRChain.TRIGGER_MOTION_ENDED, chain_pir_0_motion_ended_event)
    chain_pir_0.set_trigger(True)
    chain_pir_0.set_trigger_hold_time(5, save=False)
    trigger_hold_time = chain_pir_0.get_trigger_hold_time()
    print((str("trigger hold time: ") + str(trigger_hold_time)))
    detected = chain_pir_0.get_detect_status()
    if detected:
        label_status.setText(str("Status: detected"))
        label_status.setColor(0x009900, 0x000000)

def loop():
    global \
        title0, \
        label_status, \
        label_count, \
        bus2, \
        chain_pir_0, \
        detected, \
        count, \
        last_time, \
        trigger_hold_time
    M5.update()
    if detected:
        if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
            last_time = time.ticks_ms()
            count = (count if isinstance(count, (int, float)) else 0) + 1
            label_count.setText(str((str("Count: ") + str(count))))
    else:
        pass

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

#### PIRChain

## `PIRChain`
PIR Chain class for interacting with PIR (Passive Infrared) sensor devices over Chain bus.

- Parameter `bus` (`ChainBus`): The Chain bus instance.
- Parameter `device_id` (`int`): The device ID of the PIR sensor on the Chain bus.

```python
from chain import ChainBus
from chain import PIRChain

bus2 = ChainBus(2, tx=21, rx=22)
chain_pir_0 = PIRChain(bus2, 1)
```

### `get_detect_status`
Get the motion detection status.

- Returns: Motion detection status. True means motion detected, False means motion ended. Returns False if failed.
- Return type: bool

```python
status = chain_pir_0.get_detect_status()
```

### `set_trigger`
Enable or disable PIR detection reporting.

- Parameter `enable` (`bool`): True to enable PIR detection reporting, False to disable it.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_pir_0.set_trigger(True)
```

### `get_trigger`
Get whether PIR detection reporting is enabled.

- Returns: True if PIR detection reporting is enabled, False if disabled. Returns False if failed.
- Return type: bool

```python
enabled = chain_pir_0.get_trigger()
```

### `set_trigger_hold_time`
Set the hold time before triggering motion ended status.

- Parameter `seconds` (`int`): Hold time in seconds. Range: 0-255.
- Parameter `save` (`bool`): Whether to save the setting to flash. Default: False.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_pir_0.set_trigger_hold_time(5, False)
```

### `get_trigger_hold_time`
Get the hold time before triggering motion ended status.

- Returns: Hold time in seconds, or None if failed.
- Return type: int

```python
hold_time = chain_pir_0.get_trigger_hold_time()
```

### `set_trigger_callback`
Set callback for PIR motion detection events.

- Parameter `trigger_type` (`int`): Trigger type to listen for. Use `PIRChain.TRIGGER_MOTION_DETECTED` (1) for motion detected or `PIRChain.TRIGGER_MOTION_ENDED` (0) for motion ended.
- Parameter `callback`: Callback function that will be called when PIR motion detection changes.

> Note: Chain related methods cannot be called in the callback function.

```python
def motion_detected_callback(args):
    print("Motion detected")

def motion_ended_callback(args):
    print("Motion ended")

# Listen for motion detected only
chain_pir_0.set_trigger_callback(PIRChain.TRIGGER_MOTION_DETECTED, motion_detected_callback)

# Listen for motion ended only
chain_pir_0.set_trigger_callback(PIRChain.TRIGGER_MOTION_ENDED, motion_ended_callback)
```

    For other button and some general methods, please refer to the `ChainKey <chain.key.KeyChain>` class.
