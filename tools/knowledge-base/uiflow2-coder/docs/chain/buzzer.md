# Chain Buzzer

BuzzerChain is the helper class for buzzer devices on the Chain bus. It provides methods to control buzzer frequency, duty cycle, play modes (auto play, manual play, note play), and play musical notes.

Support the following products:

    Chain Buzzer

## MicroPython Example

#### Button tone playback

This example demonstrates how to use the Chain Buzzer in auto play mode. It initializes the buzzer RGB indicator, then plays 500 Hz, 1000 Hz, or 1500 Hz tones when button A, B, or C is clicked.

```python
import os, sys, io
import M5
from M5 import *
from chain import BuzzerChain
from chain import ChainBus

title0 = None
label_freq = None
label_tip = None
bus2 = None
chain_buzzer_0 = None

def btna_was_clicked_event(state):
    global title0, label_freq, label_tip, bus2, chain_buzzer_0
    label_freq.setText(str("Freq: 500 Hz"))
    chain_buzzer_0.tone(500, 50, 100)

def btnb_was_clicked_event(state):
    global title0, label_freq, label_tip, bus2, chain_buzzer_0
    label_freq.setText(str("Freq: 1000 Hz"))
    chain_buzzer_0.tone(1000, 50, 100)

def btnc_was_clicked_event(state):
    global title0, label_freq, label_tip, bus2, chain_buzzer_0
    label_freq.setText(str("Freq: 1500 Hz"))
    chain_buzzer_0.tone(1500, 50, 100)

def setup():
    global title0, label_freq, label_tip, bus2, chain_buzzer_0

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title(
        "Chain Buzzer Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18
    )
    label_freq = Widgets.Label(
        "Freq: -- Hz", 107, 90, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_tip = Widgets.Label(
        "Press button tone", 78, 205, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    bus2 = ChainBus(2, tx=21, rx=22)
    chain_buzzer_0 = BuzzerChain(bus2, 1)
    chain_buzzer_0.tone(2700, 50, 100)
    chain_buzzer_0.set_rgb_color(0x33FFFF)
    chain_buzzer_0.set_rgb_brightness(100, save=False)
    chain_buzzer_0.set_mode(BuzzerChain.MODE_AUTO_PLAY)

def loop():
    global title0, label_freq, label_tip, bus2, chain_buzzer_0
    M5.update()

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

#### BuzzerChain

## `BuzzerChain`
Buzzer Chain class for interacting with buzzer devices over Chain bus.

- Parameter `bus` (`ChainBus`): The Chain bus instance.
- Parameter `device_id` (`int`): The device ID of the buzzer on the Chain bus.

```python
from chain import ChainBus
from chain import BuzzerChain

bus2 = ChainBus(2, tx=21, rx=22)
chain_buzzer_0 = BuzzerChain(bus2, 1)
```

### `set_mode`
Set the buzzer mode.

- Parameter `mode` (`int`): Buzzer mode. Use `BuzzerChain.MODE_AUTO_PLAY` (0), `BuzzerChain.MODE_MANUAL_PLAY` (1), or `BuzzerChain.MODE_NOTE_PLAY` (2).
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_buzzer_0.set_mode(BuzzerChain.MODE_AUTO_PLAY)
```

### `get_mode`
Get the buzzer mode.

- Returns: Buzzer mode. `BuzzerChain.MODE_AUTO_PLAY` (0), `BuzzerChain.MODE_MANUAL_PLAY` (1), or `BuzzerChain.MODE_NOTE_PLAY` (2). Returns None if failed.
- Return type: int

```python
mode = chain_buzzer_0.get_mode()
```

### `tone`
Play tone (only works in AUTO_PLAY mode).

- Parameter `freq` (`int`): Frequency in Hz. Range: 100-10000. Default: 2700.
- Parameter `duty` (`int`): Duty cycle (0-100). Default: 50.
- Parameter `duration_ms` (`int`): Duration in milliseconds. Default: 100.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_buzzer_0.tone(2700, 50, 1000)
success = chain_buzzer_0.tone()  # Use default values: 2700Hz, 50% duty, 100ms
```

### `set_freq`
Set the buzzer frequency.

- Parameter `freq` (`int`): Frequency in Hz. Range: 100-10000. Default: 2700.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_buzzer_0.set_freq(2700)
success = chain_buzzer_0.set_freq()  # Use default: 2700Hz
```

### `get_freq`
Get the buzzer frequency.

- Returns: Frequency in Hz, or None if failed.
- Return type: int

```python
freq = chain_buzzer_0.get_freq()
```

### `set_duty`
Set the buzzer duty cycle.

- Parameter `duty` (`int`): Duty cycle (0-100). Default: 50.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_buzzer_0.set_duty(50)
success = chain_buzzer_0.set_duty()  # Use default: 50%
```

### `get_duty`
Get the buzzer duty cycle.

- Returns: Duty cycle (0-100), or None if failed.
- Return type: int

```python
duty = chain_buzzer_0.get_duty()
```

### `set_status`
Set the buzzer status (only works in MANUAL_PLAY mode).

- Parameter `status` (`int`): Buzzer status. Use `BuzzerChain.STATUS_OFF` (0) or `BuzzerChain.STATUS_ON` (1).
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_buzzer_0.set_status(BuzzerChain.STATUS_ON)
```

### `get_status`
Get the buzzer status.

- Returns: Buzzer status. `BuzzerChain.STATUS_OFF` (0) or `BuzzerChain.STATUS_ON` (1). Returns None if failed.
- Return type: int

```python
status = chain_buzzer_0.get_status()
```

### `note`
Play note (only works in NOTE_PLAY mode).

- Parameter `note_index` (`int`): Note index (0-61). 0 is rest (silence), 13 is C4, and 61 is C8.
- Parameter `duration_ms` (`int`): Duration in milliseconds. Default: 100.
- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = chain_buzzer_0.note(25, 500)  # Play C5 for 500ms
success = chain_buzzer_0.note(25)  # Play C5 for 100ms (default duration)
```

    For other button and some general methods, please refer to the `ChainKey <chain.key.KeyChain>` class.
