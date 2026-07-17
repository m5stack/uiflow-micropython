# StamPLC

`StamPLC` is the board-level helper for the built-in PLC I/O on StamPLC.

Supported Products:

    StamPLC

Create one `StamPLC` object, then access relay outputs, digital inputs, and the
built-in RGB LED from that object.

Channels are 1-based:

- `relay[1]` to `relay[4]` control the four relay outputs.
- `input[1]` to `input[8]` read the eight digital inputs.
- `led.red`, `led.green`, and `led.blue` control the built-in RGB LED.

## MicroPython Examples

#### Relay control

This example uses button A to toggle relay output 1 and turns on the built-in blue LED.

```python
import os, sys, io
import M5
from M5 import *
from stamplc import StamPLC

title0 = None
label_tip = None
label_state = None
stamplc_0 = None

def btna_was_clicked_event(state):
    global title0, label_tip, label_state, stamplc_0
    stamplc_0.relay[1].toggle()
    if stamplc_0.relay[1].value():
        label_state.setText(str("Realy1: ON"))
        label_state.setCursor(x=55, y=53)
        label_state.setColor(0x009900, 0x000000)
    else:
        label_state.setText(str("Realy1: OFF"))
        label_state.setCursor(x=50, y=53)
        label_state.setColor(0xFFFFFF, 0x000000)

def setup():
    global title0, label_tip, label_state, stamplc_0

    M5.begin()
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("Relay Control", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat24)
    label_tip = Widgets.Label(
        "BtnA control relay1", 33, 103, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_state = Widgets.Label(
        "Realy1: OFF", 50, 53, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)

    stamplc_0 = StamPLC()
    stamplc_0.led.blue.on()

def loop():
    global title0, label_tip, label_state, stamplc_0
    M5.update()

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

#### Digital input control

This example reads digital inputs 1-3 and uses them to control relay outputs 1-3.

```python
import os, sys, io
import M5
from M5 import *
import time
from stamplc import StamPLC

title0 = None
label_relay1_state = None
label_relay2_state = None
label_relay3_state = None
stamplc_0 = None

last_time = None
state1 = None
laste_state1 = None
state2 = None
last_state2 = None
state3 = None
last_state3 = None

def setup():
    global \
        title0, \
        label_relay1_state, \
        label_relay2_state, \
        label_relay3_state, \
        stamplc_0, \
        last_time, \
        state1, \
        laste_state1, \
        state2, \
        last_state2, \
        state3, \
        last_state3

    M5.begin()
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title(
        "Input control relay", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat24
    )
    label_relay1_state = Widgets.Label(
        "Relay1: OFF", 10, 35, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_relay2_state = Widgets.Label(
        "Relay2: OFF", 10, 65, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )
    label_relay3_state = Widgets.Label(
        "Relay3: OFF", 10, 95, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat18
    )

    stamplc_0 = StamPLC()
    stamplc_0.led.red.value(1)

def loop():
    global \
        title0, \
        label_relay1_state, \
        label_relay2_state, \
        label_relay3_state, \
        stamplc_0, \
        last_time, \
        state1, \
        laste_state1, \
        state2, \
        last_state2, \
        state3, \
        last_state3
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 200:
        last_time = time.ticks_ms()
        state1 = stamplc_0.input[1].value()
        if state1 != laste_state1:
            laste_state1 = state1
            if state1:
                stamplc_0.relay[1].value(1)
                label_relay1_state.setText(str("Relay1: ON"))
                label_relay1_state.setColor(0x009900, 0x000000)
            else:
                stamplc_0.relay[1].value(0)
                label_relay1_state.setText(str("Relay1: OFF"))
                label_relay1_state.setColor(0xFFFFFF, 0x000000)
        state2 = stamplc_0.input[2].value()
        if state2 != last_state2:
            last_state2 = state2
            if state2:
                stamplc_0.relay[2].value(1)
                label_relay2_state.setText(str("Relay2: ON"))
                label_relay2_state.setColor(0x009900, 0x000000)
            else:
                stamplc_0.relay[2].value(0)
                label_relay2_state.setText(str("Relay2: OFF"))
                label_relay2_state.setColor(0xFFFFFF, 0x000000)
        state3 = stamplc_0.input[3].value()
        if state3 != last_state3:
            last_state3 = last_state3
            if state3:
                stamplc_0.relay[3].value(1)
                label_relay3_state.setText(str("Relay3: ON"))
                label_relay3_state.setColor(0x009900, 0x000000)
            else:
                stamplc_0.relay[3].value(0)
                label_relay3_state.setText(str("Relay3: OFF"))
                label_relay3_state.setColor(0xFFFFFF, 0x000000)

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

## **API**

#### StamPLC

### `class StamPLC()`

    Create a StamPLC board helper.

```python
from stamplc import StamPLC

plc = StamPLC()
```
### `relay`

        Relay output bank. Relay channels are indexed from 1 to 4.
        Relays are initialized to `False`/off when `StamPLC()` is created.

### `relay[channel].on()`

            Turn one relay output on.

            - Parameter `channel` (`int`): Relay channel, 1-4.

```python
plc.relay[1].on()
```
### `relay[channel].off()`

            Turn one relay output off.

            - Parameter `channel` (`int`): Relay channel, 1-4.

```python
plc.relay[1].off()
```
### `relay[channel].toggle()`

            Toggle one relay output.

            - Parameter `channel` (`int`): Relay channel, 1-4.

```python
plc.relay[1].toggle()
```
### `relay[channel].value(state=None)`

            Get or set one relay output.

            - Parameter `channel` (`int`): Relay channel, 1-4.
            - Parameter `state` (`bool`): Optional output state. `True` turns the relay on, `False` turns it off.
            - Returns: Relay state when `state` is omitted.
            - Return type: bool or None

```python
plc.relay[1].value(True)
state = plc.relay[1].value()
```
### `input`

        Digital input bank. All digital input channels are initialized as inputs
        when `StamPLC()` is created. Input channels are indexed from 1 to 8.

### `input[channel].value()`

            Read one input channel.

            - Parameter `channel` (`int`): Input channel, 1-8.
            - Returns: The selected input value, `0` or `1`.
            - Return type: int

```python
input_1 = plc.input[1].value()
```
### `input[channel].irq(handler, trigger)`

            Set an interrupt handler for one input channel.
            The callback receives the input pin object; use `pin.channel` to get the channel number.

            - Parameter `channel` (`int`): Input channel, 1-8.
            - Parameter `handler` (`function`): Interrupt callback.
            - Parameter `trigger` (`int`): `plc.input.IRQ_FALLING` or `plc.input.IRQ_RISING`.

```python
def input_1_falling_event(pin):
    print("input", pin.channel, "falling")

plc.input[1].irq(input_1_falling_event, plc.input.IRQ_FALLING)
```
### `led`

        Built-in RGB LED controller. The LED is driven by PI4IOE5V6408:
        red maps to P6, green maps to P5, and blue maps to P4.

        `led.red`, `led.green`, and `led.blue` provide the same methods.

### `led.red.on()`

            Turn the red LED on.

```python
plc.led.red.on()
```
### `led.red.off()`

            Turn the red LED off.

```python
plc.led.red.off()
```
### `led.red.toggle()`

            Toggle the red LED.

```python
plc.led.red.toggle()
```
### `led.red.value(state=None)`

            Get or set the red LED state.

            - Parameter `state` (`bool`): Optional LED state. `True` turns the LED on, `False` turns it off.
            - Returns: LED state when `state` is omitted.
            - Return type: bool or None

```python
plc.led.red.value(True)
state = plc.led.red.value()
```

```python
plc.led.green.on()
plc.led.blue.off()
plc.led.blue.toggle()
```
