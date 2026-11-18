# Chain Pedal

PedalChain is the helper class for Chain Pedal devices on the Chain bus. It
provides access to the physical pedal state, logical switch state, event
callbacks, work modes, and the four RGB LEDs.

Support the following products:

    Chain Pedal

## Product Features

- Read the physical pedal state or the latched logical switch state.
- Use single-click mode or switch mode, and receive click or status-change
  callbacks when event reporting is enabled.
- Control four RGB LEDs independently and select which LEDs show the pedal
  event overlay.
- Configure how long the pedal must be held to enter local configuration mode.
- Optionally save the work mode, configuration-entry time, RGB overlay mask,
  and RGB brightness to flash.

## MicroPython Example

#### Switch status callbacks

This example configures Chain Pedal in switch mode, sets the RGB LEDs, and
prints a message when the switch status changes.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from chain import PedalChain
from chain import ChainBus

page0 = None
bus1 = None
chain_pedal_0 = None

def chain_pedal_0_status_open_event(args):
    global page0, bus1, chain_pedal_0
    print("switch open")

def chain_pedal_0_status_close_event(args):
    global page0, bus1, chain_pedal_0
    print("switch close")

def setup():
    global page0, bus1, chain_pedal_0

    M5.begin()
    Widgets.setRotation(0)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)

    bus1 = ChainBus(1, tx=14, rx=13)
    chain_pedal_0 = PedalChain(bus1, 1)
    chain_pedal_0.set_trigger_callback(PedalChain.STATUS_OPEN, chain_pedal_0_status_open_event)
    chain_pedal_0.set_trigger_callback(PedalChain.STATUS_CLOSE, chain_pedal_0_status_close_event)
    print(chain_pedal_0.set_work_mode(PedalChain.WORK_MODE_SWITCH, save=False))
    chain_pedal_0.fill_rgb_color(0x6600CC)
    chain_pedal_0.set_rgb_overlay(0x0F, save=False)

def loop():
    global page0, bus1, chain_pedal_0
    M5.update()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            bus1.deinit()
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

Example output:

```text
switch open
switch close
```
## **API**

#### PedalChain

## `PedalChain`
Pedal Chain class for interacting with pedal devices over Chain bus.

- Parameter `bus` (`ChainBus`): The Chain bus instance.
- Parameter `device_id` (`int`): The device ID of the pedal on the Chain bus.

```python
from chain import ChainBus, PedalChain

chainbus_0 = ChainBus(2, tx=32, rx=33)
pedalchain_0 = PedalChain(chainbus_0, 1)
```

### `get_button_state`
get button state.

- Returns: Button state, True if pressed, False if released or failed.
- Return type: bool

```python
state = pedalchain_0.get_button_state()
```

### `get_switch_status`
get switch status.

- Returns: Switch status, 0 for close, 1 for open, or -1 if failed.
- Return type: int

```python
status = pedalchain_0.get_switch_status()
```

### `set_click_callback`
set button click callback.

- Parameter `callback`: Callback function accepting one argument, or None to
    disable it.

> Note: Chain related methods cannot be called in the callback function.

```python
def pedal_click_callback(args):
    print("click")

pedalchain_0.set_click_callback(pedal_click_callback)
```

### `set_trigger_callback`
set callback for switch status change events.

- Parameter `trigger_type` (`int`): Trigger type, 0 for close or 1 for open.
- Parameter `callback`: Callback function accepting one argument, or None to
    disable it.

> Note: Chain related methods cannot be called in the callback function.

```python
def pedal_status_callback(args):
    print("switch status changed")

pedalchain_0.set_trigger_callback(
    PedalChain.STATUS_OPEN, pedal_status_callback
)
```

### `set_work_mode`
set pedal work mode.

- Parameter `mode` (`int`): Work mode. Use `WORK_MODE_SINGLE` or
    `WORK_MODE_SWITCH`.
- Parameter `save` (`bool`): Whether to save the setting to flash. Default: False.
- Returns: True if success, False otherwise.
- Return type: bool

```python
pedalchain_0.set_work_mode(PedalChain.WORK_MODE_SWITCH)
```

### `get_work_mode`
get pedal work mode.

- Returns: Work mode, 0 for single click, 1 for switch, or -1 if failed.
- Return type: int

```python
mode = pedalchain_0.get_work_mode()
```

### `set_button_mode`
set button reporting mode.

- Parameter `mode` (`int`): Reporting mode. Use `MODE_POLL` or `MODE_EVENT`.
- Returns: True if success, False otherwise.
- Return type: bool

```python
pedalchain_0.set_button_mode(PedalChain.MODE_EVENT)
```

### `get_button_mode`
get button reporting mode.

- Returns: Reporting mode, 0 for polling, 1 for events, or -1 if failed.
- Return type: int

```python
mode = pedalchain_0.get_button_mode()
```

### `set_enter_config_time`
set local configuration entry time.

- Parameter `seconds` (`int`): Time in seconds from 1 to 30. Use 0 to disable
    local configuration entry.
- Parameter `save` (`bool`): Whether to save the setting to flash. Default: False.
- Returns: True if success, False otherwise.
- Return type: bool

```python
pedalchain_0.set_enter_config_time(10)
```

### `get_enter_config_time`
get local configuration entry time.

- Returns: Time in seconds, 0 if disabled, or -1 if failed.
- Return type: int

```python
seconds = pedalchain_0.get_enter_config_time()
```

### `set_rgb_overlay`
set the pedal event RGB overlay mask.

- Parameter `overlay_mask` (`int`): Bitmask from 0x00 to 0x0F. Bits 0-3 select LEDs
    0-3.
- Parameter `save` (`bool`): Whether to save the setting to flash. Default: False.
- Returns: True if success, False otherwise.
- Return type: bool
    0x00-0x0F.

```python
pedalchain_0.set_rgb_overlay(0x0F)
```

### `get_rgb_overlay`
get the pedal event RGB overlay mask.

- Returns: Bitmask from 0x00 to 0x0F, or -1 if failed.
- Return type: int

```python
overlay_mask = pedalchain_0.get_rgb_overlay()
```
