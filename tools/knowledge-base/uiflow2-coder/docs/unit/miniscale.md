# Miniscale Unit

The `Miniscale` class is designed for interfacing with a mini scale weight sensor, which includes a HX711 22-bit ADC. This sensor is capable of measuring weight and also includes additional functionalities like LED control and various filters.

Support the following products:

MINISCALE

## MicroPython Example

#### Basic Example

This example demonstrates how to read and display weight values from the MiniScale unit. It sets up an average filter level of 10 for smoother readings and updates the weight display every second.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import I2C
from hardware import Pin
from unit import MiniScaleUnit
import time

page0 = None
label_title = None
label_weight = None
i2c0 = None
miniscales_0 = None
last_time = None
weight = None

def setup():
    global page0, label_title, label_weight, i2c0, miniscales_0, last_time, weight

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label_title = m5ui.M5Label(
        "MiniScales",
        x=94,
        y=5,
        text_c=0x0000FF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    label_weight = m5ui.M5Label(
        "Weights: -- g",
        x=81,
        y=90,
        text_c=0x0000FF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    miniscales_0 = MiniScaleUnit(i2c0)
    miniscales_0.set_average_filter_level(10)
    page0.screen_load()

def loop():
    global page0, label_title, label_weight, i2c0, miniscales_0, last_time, weight
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
        last_time = time.ticks_ms()
        weight = int(miniscales_0.weight)
        label_weight.set_text(str((str("Weight: ") + str((str(weight) + str(" g"))))))

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

#### Calibration Example

This example demonstrates the complete calibration process for the MiniScale unit. It guides users through a three-step calibration: first removing all items and recording the zero-point ADC value, then placing a 100g weight and recording that ADC value, and finally performing tare operation to set the zero point. After calibration, the weight is displayed with an average filter level of 5.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import I2C
from hardware import Pin
from unit import MiniScaleUnit
import time

page0 = None
label_weight = None
button0 = None
label_tip = None
label_title = None
i2c0 = None
miniscales_0 = None
state = None
adc_0 = None
adc_100 = None
last_time = None
weight = None

def button0_short_clicked_event(event_struct):
    global \
        page0, \
        label_weight, \
        button0, \
        label_tip, \
        label_title, \
        i2c0, \
        miniscales_0, \
        state, \
        adc_0, \
        adc_100, \
        last_time, \
        weight
    Speaker.tone(888, 200)
    if state == 0:
        state = 1
        adc_0 = miniscales_0.adc
        print((str("ADC0 Value: ") + str(adc_0)))
        label_tip.set_text(str("Put 100g weight, then press button."))
    elif state == 1:
        state = 2
        adc_100 = miniscales_0.adc
        print((str("ADC100 Value: ") + str(adc_100)))
        print("do calibrate")
        miniscales_0.calibration(0, adc_0, 100, adc_100)
        label_tip.set_text(str("Remove all items, then press button."))
    elif state == 2:
        state = 3
        print("tare the scale")
        print((str("Tare: ") + str((str((miniscales_0.weight)) + str(" g")))))
        miniscales_0.tare()
        label_tip.set_text(str("Weight"))
        label_tip.set_flag(lv.obj.FLAG.HIDDEN, True)
        button0.set_flag(lv.obj.FLAG.HIDDEN, True)
        miniscales_0.set_average_filter_level(5)

def button0_event_handler(event_struct):
    global \
        page0, \
        label_weight, \
        button0, \
        label_tip, \
        label_title, \
        i2c0, \
        miniscales_0, \
        state, \
        adc_0, \
        adc_100, \
        last_time, \
        weight
    event = event_struct.code
    if event == lv.EVENT.SHORT_CLICKED and True:
        button0_short_clicked_event(event_struct)
    return

def setup():
    global \
        page0, \
        label_weight, \
        button0, \
        label_tip, \
        label_title, \
        i2c0, \
        miniscales_0, \
        state, \
        adc_0, \
        adc_100, \
        last_time, \
        weight

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label_weight = m5ui.M5Label(
        "Weight: ",
        x=14,
        y=90,
        text_c=0x0000FF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )
    button0 = m5ui.M5Button(
        text="Button",
        x=116,
        y=160,
        bg_c=0x2196F3,
        text_c=0xFFFFFF,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_tip = m5ui.M5Label(
        "Tip:",
        x=10,
        y=50,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label_title = m5ui.M5Label(
        "MiniScales",
        x=93,
        y=5,
        text_c=0x0000FF,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_24,
        parent=page0,
    )

    button0.add_event_cb(button0_event_handler, lv.EVENT.ALL, None)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    miniscales_0 = MiniScaleUnit(i2c0)
    page0.screen_load()
    label_tip.set_text(str("Remove all items, then press button."))
    label_weight.set_text(str("Weight: -- g"))
    label_weight.align_to(page0, lv.ALIGN.CENTER, 0, 0)
    state = 0
    button0.set_size(100, 50)
    button0.align_to(page0, lv.ALIGN.CENTER, 0, 60)
    Speaker.begin()
    Speaker.setVolumePercentage(0.6)
    Speaker.tone(888, 200)

def loop():
    global \
        page0, \
        label_weight, \
        button0, \
        label_tip, \
        label_title, \
        i2c0, \
        miniscales_0, \
        state, \
        adc_0, \
        adc_100, \
        last_time, \
        weight
    M5.update()
    if state == 3:
        if (time.ticks_diff((time.ticks_ms()), last_time)) >= 1000:
            last_time = time.ticks_ms()
            weight = int(miniscales_0.weight)
            label_weight.set_text(str((str("Weight:  ") + str((str(weight) + str(" g"))))))
            label_weight.align_to(page0, lv.ALIGN.CENTER, 0, 0)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            m5ui.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

## **API**

#### class MiniScaleUnit

### `class unit.miniscale.MiniScaleUnit(i2c, address=0x26)`

    Create a MiniScaleUnit object.

    - Parameter `| PAHUBUnit i2c` (`I2C`): The I2C or PAHUBUnit instance for communication.
    - Parameter `address` (`int`): The I2C address of the MiniScale unit, default is 0x26.

```python
from unit import MiniScaleUnit
from hardware import I2C, Pin

i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
miniscale_0 = MiniScaleUnit(i2c0)
```
### `adc`

        Read raw ADC value (unprocessed).

        - Returns: Raw ADC value (integer).
        - Return type: int

```python
adc_value = miniscale_0.adc
```
### `weight`

        Read current weight (grams).

        - Returns: Actual weight (float after subtracting tare value).
        - Return type: float

```python
weight_value = miniscale_0.weight
```
### `button`

        Read button state.

        - Returns: True if pressed, False if not pressed.
        - Return type: bool

```python
button_state = miniscale_0.button
```
### `tare()`

        Tare operation. Record current weight as offset value, so subsequent weight readings use current as zero point.

```python
miniscale_0.tare()
```
### `set_led(r, g, b)`

        Set RGB indicator color.

        - Parameter `r` (`int`): Red component (0~255).
        - Parameter `g` (`int`): Green component (0~255).
        - Parameter `b` (`int`): Blue component (0~255).

```python
miniscale_0.set_led(255, 0, 0)
```
### `reset()`

        Reset module internal weight register (clear to zero).

```python
miniscale_0.reset()
```
### `calibration(weight1_g, weight1_adc, weight2_g, weight2_adc)`

        Calibrate module gain (GAP value).

        Calibration process example:
        1. Reset offset
        2. Read no-load ADC (RawADC_0g)
        3. Place known weight (e.g., 100g) and read ADC (RawADC_100g)
        4. Calculate GAP = (RawADC_100g - RawADC_0g) / 100
        5. Write to module to save calibration coefficient

        - Parameter `weight1_g` (`float`): Weight at first point (unit: g).
        - Parameter `weight1_adc` (`int`): ADC value at first point.
        - Parameter `weight2_g` (`float`): Weight at second point (unit: g).
        - Parameter `weight2_adc` (`int`): ADC value at second point.

```python
miniscale_0.calibration(0, adc_0, 100, adc_100)
```
### `set_low_pass_filter(enabled)`

        Enable or disable low-pass filter.

        - Parameter `enabled` (`bool`): True to enable filter, False to disable filter.

```python
miniscale_0.set_low_pass_filter(True)
```
### `get_low_pass_filter()`

        Get low-pass filter status.

        - Returns: True if filter is enabled.
        - Return type: bool

```python
filter_enabled = miniscale_0.get_low_pass_filter()
```
### `set_average_filter_level(level)`

        Set average filter level.

        - Parameter `level` (`int`): Average count level (0~50), higher value means smoother but more delay.

```python
miniscale_0.set_average_filter_level(10)
```
### `get_average_filter_level()`

        Get average filter level.

        - Returns: Current average filter level (integer).
        - Return type: int

```python
filter_level = miniscale_0.get_average_filter_level()
```
### `set_ema_filter_alpha(alpha)`

        Set exponential moving average (EMA) filter parameter.

        The EMA (Exponential Moving Average) filter is more sensitive to changes in data compared to the average filter.

        - Parameter `alpha` (`int`): EMA filter coefficient (0~99), smaller value means smoother but more response delay.

```python
miniscale_0.set_ema_filter_alpha(50)
```
### `get_ema_filter_alpha()`

        Get EMA filter coefficient.

        - Returns: Current EMA alpha value (integer).
        - Return type: int

```python
ema_alpha = miniscale_0.get_ema_filter_alpha()
```
