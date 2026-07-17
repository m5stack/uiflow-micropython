# MQ Unit

This is the driver library of MQ Unit, which is used to obtain data from the
MQ sensor.

Support the following products:

    MQ

## MicroPython Example

#### get MQ ADC value

This example gets the ADC value of the MQ Unit and displays it on the screen.

```python
import os, sys, io
import M5
from M5 import *
import m5ui
import lvgl as lv
from hardware import I2C
from hardware import Pin
from unit import MQUnit

page0 = None
label0 = None
label1 = None
label2 = None
i2c0 = None
mq_0 = None

valid = None

def setup():
    global page0, label0, label1, label2, i2c0, mq_0, valid

    M5.begin()
    Widgets.setRotation(1)
    m5ui.init()
    page0 = m5ui.M5Page(bg_c=0xFFFFFF)
    label0 = m5ui.M5Label(
        "Valid Flag:",
        x=1,
        y=76,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label1 = m5ui.M5Label(
        "ADC 8bits:0",
        x=1,
        y=111,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )
    label2 = m5ui.M5Label(
        "ADC 12bits:0",
        x=1,
        y=145,
        text_c=0x000000,
        bg_c=0xFFFFFF,
        bg_opa=0,
        font=lv.font_montserrat_16,
        parent=page0,
    )

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    mq_0 = MQUnit(i2c0, 0x11)
    mq_0.set_mq_mode(1)
    page0.screen_load()

def loop():
    global page0, label0, label1, label2, i2c0, mq_0, valid
    M5.update()
    valid = mq_0.get_valid_tags()
    if valid:
        label0.set_text(str((str("Valid Flag:") + str(valid))))
        label1.set_text(str((str("ADC 8bits:") + str((mq_0.get_adc_value(0))))))
        label2.set_text(str((str("ADC 12bits:") + str((mq_0.get_adc_value(1))))))
    else:
        label0.set_text(str("Valid Flag: Wait heating"))

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

#### MQUnit

## `MQUnit`
Create a MQUnit object.

- Parameter `i2c` (`I2C`): The I2C bus the MQ Unit is connected to.
- Parameter `address` (`int`): The I2C address of the device. Default is 0x11.

```python
from hardware import I2C
from unit import MQUnit

i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
tof_0 = MQUnit(i2c0)
```

### `set_mq_mode`
Set the working mode of the MQ sensor.

- Parameter `mode` (`int`): Working mode value.

Option:
    - 0 : Measurement off
    - 1 : Continuous heating mode
    - 2 : Pin Level Switching Mode

```python
mq_0.set_mq_mode(1)
```

### `get_mq_mode`
Get the current working mode of the MQ sensor.

- Returns: Current working mode value.
- Return type: int

```python
mode = mq_0.get_mq_mode()
```

### `set_led_status`
Set the LED status.

- Parameter `status` (`int`): When the LED is set to on, it lights up when a valid tag is detected, and the brightness is proportional to the ADC value, and it turns off when no tag is detected.

```python
mq_0.set_led_status(1)
```

### `get_led_status`
Get the LED status.

- Returns: True if LED status is on, False otherwise.
- Return type: bool

```python
led_on = mq_0.get_led_status()
```

### `set_heat_time`
Set heater high and low level time.

- Parameter `high_level_time` (`int`): Time for high heating level.
- Parameter `low_level_time` (`int`): Time for low heating level.

```python
mq_0.set_heat_time(30, 5)
```

### `get_heat_time`
Get heater high and low level time.

- Returns: [high_level_time, low_level_time]
- Return type: [int, int]

```python
times = mq_0.get_heat_time()
```

### `get_adc_value`
Get ADC value.

- Parameter `precision` (`int`): 0 for 8-bit, 1 for 12-bit.
- Returns: ADC value.
- Return type: int

```python
value = mq_0.get_adc_value(1)
```

### `get_valid_tags`
Check if valid tags are detected.

- Returns: True if valid tags detected, False otherwise.
- Return type: bool

```python
valid = mq_0.get_valid_tags()
```

### `get_ntc_adc_value`
Get internal NTC ADC value.

- Parameter `precision` (`int`): 0 for 8-bit, 1 for 12-bit.
- Returns: NTC ADC value.
- Return type: int

```python
ntc = mq_0.get_ntc_adc_value(1)
```

### `get_ntc_res_value`
Get internal NTC resistance value.

- Returns: Resistance value.
- Return type: int

```python
res = mq_0.get_ntc_res_value()
```

### `get_voltage`
Get voltage value from a specific channel.

- Parameter `channle` (`int`): Channel number.
- Returns: Voltage value.
- Return type: int

```python
voltage = mq_0.get_voltage(0)
```

### `get_firmware_version`
Get firmware version.

- Returns: Firmware version.
- Return type: int

```python
ver = mq_0.get_firmware_version()
```

### `get_i2c_address`
Get current I2C address.

- Returns: MQ Unit I2C address, Default is 0x11.
- Return type: int

```python
addr = mq_0.get_i2c_address()
```

### `set_i2c_address`
Set new I2C address.

- Parameter `addr` (`int`): New I2C address (0x08~0x77).

```python
mq_0.set_i2c_address(0x3A)
```
