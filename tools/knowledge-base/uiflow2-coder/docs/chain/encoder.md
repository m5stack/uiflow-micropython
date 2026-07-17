# Chain Encoder

EncoderChain is the helper class for encoder devices on the Chain bus. It provides methods to read encoder values and increments, reset the encoder, configure the clockwise rotation direction, and handle button events with RGB LED feedback.

Support the following products:

    Chain Encoder

## MicroPython Example

#### Encoder reading with brightness control

This example demonstrates how to read encoder values and increments, handle button click events, and control RGB LED brightness based on encoder rotation. The encoder value is displayed on screen and updated in real-time.

```python
import os, sys, io
import M5
from M5 import *
from chain import EncoderChain
from chain import ChainBus
import time

title0 = None
label_brightness = None
label_val = None
label_count = None
bus2 = None
chain_encoder_0 = None
count = None
last_time = None
value = None
brightness = None

def chain_encoder_0_click_event(args):
    global title0, label_brightness, label_val, label_count, bus2, chain_encoder_0, count, last_time, value, brightness
    count = (count if isinstance(count, (int, float)) else 0) + 1
    label_count.setText(str((str('Button Count: ') + str(count))))

def setup():
    global title0, label_brightness, label_val, label_count, bus2, chain_encoder_0, count, last_time, value, brightness
    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Title", 3, 0xffffff, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_brightness = Widgets.Label("Brightness:", 5, 100, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu24)
    label_val = Widgets.Label("Value:", 5, 60, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu24)
    label_count = Widgets.Label("Button Count:", 5, 140, 1.0, 0xffffff, 0x222222, Widgets.FONTS.DejaVu24)
    bus2 = ChainBus(2, tx=21, rx=22)
    chain_encoder_0 = EncoderChain(bus2, 1)
    chain_encoder_0.set_click_callback(chain_encoder_0_click_event)
    chain_encoder_0.set_button_mode(chain_encoder_0.MODE_EVENT)
    chain_encoder_0.set_rgb_color(0x00ff00)
    chain_encoder_0.set_rgb_brightness(80, save=False)
    chain_encoder_0.set_cw_increase(True, save=False)
    print(chain_encoder_0.get_encoder_increment())
    brightness = 0

def loop():
    global title0, label_brightness, label_val, label_count, bus2, chain_encoder_0, count, last_time, value, brightness
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 100:
        last_time = time.ticks_ms()
        value = chain_encoder_0.get_encoder_value()
        label_val.setText(str((str('Value: ') + str(value))))
        brightness = min(max(brightness + (chain_encoder_0.get_encoder_increment()), 0), 100)
        label_brightness.setText(str((str('Brightness: ') + str(brightness))))
        chain_encoder_0.set_rgb_brightness(brightness, save=False)

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

#### EncoderChain

## `EncoderChain`
Encoder Chain class for interacting with encoder devices over Chain bus.

- Parameter `bus` (`ChainBus`): The Chain bus instance.
- Parameter `device_id` (`int`): The device ID of the encoder on the Chain bus.

```python
from chain import ChainBus
from chain import EncoderChain

chainbus_0 = ChainBus(2, 32, 33, verbose=True)
encoder_0 = EncoderChain(chainbus_0, 1)
```

### `get_encoder_value`
Get the encoder value.

- Returns: Encoder value as int16_t (-32768 to 32767), or None if failed.
- Return type: int

```python
value = encoder_0.get_encoder_value()
```

### `get_encoder_increment`
Get the encoder increment value.

- Returns: Encoder increment value as int16_t (-32768 to 32767), or None if failed.
- Return type: int

```python
increment = encoder_0.get_encoder_increment()
```

### `reset_encoder_value`
Reset the encoder value.

- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = encoder_0.reset_encoder_value()
```

### `reset_encoder_increment`
Reset the encoder increment value.

- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
success = encoder_0.reset_increment()
```

### `set_cw_increase`
Set whether clockwise rotation increases the encoder value.

- Parameter `clockwise_increase` (`bool`): Whether clockwise rotation increases. True means clockwise increases (sends 0), False means clockwise decreases (sends 1).
- Parameter `save` (`bool`): Whether to save to flash. False means don't save, True means save.
- Returns: True if the setting was set successfully, False otherwise.
- Return type: bool

```python
success = encoder_0.set_cw_increase(True, True)
```

### `get_cw_increase`
Get whether clockwise rotation increases the encoder value.

- Returns: Whether clockwise rotation increases. True means clockwise increases, False means clockwise decreases. Returns False if failed.
- Return type: bool

```python
increase = encoder_0.get_cw_increase()
```

    For other button and some general methods, please refer to the `ChainKey <chain.key.KeyChain>` class.
