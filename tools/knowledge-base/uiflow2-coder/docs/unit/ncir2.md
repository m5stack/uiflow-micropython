# NCIR2 Unit

This library is the driver for Unit NCIR2.

Support the following products:

    Unit NCIR2

## MicroPython Example

#### Infrared Temperature Display

This example uses the M5Stack CoreS3 board with the NCIR2 infrared temperature sensor to measure temperature in real time and display the current value along with the low and high temperature alarm thresholds on screen.

```python
import os, sys, io
import M5
from M5 import *
from hardware import I2C
from hardware import Pin
from unit import NCIR2Unit
import time

title0 = None
label_temp = None
label_la = None
label_ha = None
label_temp_val = None
label_la_val = None
label_ha_val = None
i2c0 = None
ncir2_0 = None
last_time = None

def setup():
    global \
        title0, \
        label_temp, \
        label_la, \
        label_ha, \
        label_temp_val, \
        label_la_val, \
        label_ha_val, \
        i2c0, \
        ncir2_0, \
        last_time
    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title("Temperature meassure", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu24)
    label_temp = Widgets.Label("Temp: ", 10, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label_la = Widgets.Label(
        "low temp alarm value: ", 10, 50, 1.0, 0x0000FF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_ha = Widgets.Label(
        "high temp alarm value: ", 10, 80, 1.0, 0xFF0000, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_temp_val = Widgets.Label(" ", 95, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu24)
    label_la_val = Widgets.Label(" ", 232, 50, 1.0, 0x0000FF, 0x222222, Widgets.FONTS.DejaVu18)
    label_ha_val = Widgets.Label(" ", 239, 80, 1.0, 0xFF0000, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    ncir2_0 = NCIR2Unit(i2c0, 0x5A)
    last_time = time.ticks_ms()
    label_la_val.setText(str(ncir2_0.get_temperature_threshold(0x20)))
    label_ha_val.setText(str(ncir2_0.get_temperature_threshold(0x22)))

def loop():
    global \
        title0, \
        label_temp, \
        label_la, \
        label_ha, \
        label_temp_val, \
        label_la_val, \
        label_ha_val, \
        i2c0, \
        ncir2_0, \
        last_time
    M5.update()
    if (time.ticks_diff((time.ticks_ms()), last_time)) > 500:
        last_time = time.ticks_ms()
        label_temp.setText(str((str((ncir2_0.get_temperature_value)) + str(" C"))))

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

#### NCIR2Unit

### `class unit.hbridge.NCIR2Unit`

    Create an NCIR2Unit object.

    - Parameter `| PAHUBUnit i2c` (`I2C`): I2C port,
    - Parameter `address` (`int`): NCIR2Unit Slave Address, Default is 0x5A.

```python
from unit import NCIR2Unit

unit_ncir2_0 = NCIR2Unit(i2c0, 0x5A)
```
### `get_temperature_value()`

        Get object temperature.

        - Returns: object temperature(unit: ℃)
        - Return type: float

```python
unit_ncir2_0.get_temperature_value()
```
### `get_emissivity_value()`

        Get current emissivity.

        - Returns: emissivity.
        - Return type: float

```python
unit_ncir2_0.get_emissivity_value()
```
### `set_emissivity_value(emissive)`

        Set the emissivity.

        According to the material being measured; it affects temperature measurement accuracy.

        - A black body has an emissivity of 1.00 (ideal emitter).
        - Shiny metals often have low emissivity values (below 0.1).
        - Dark, rough surfaces like electrical tape or human skin typically have high emissivity (above 0.95).

```python
unit_ncir2_0.set_emissivity_value(emissive)
```
### `get_temperature_threshold(alarm_reg)`

        Get temperature alaram threshold.

        - Returns: alarm threshold.
        - Return type: float

```python
unit_ncir2_0.get_temperature_threshold(alarm_reg)
```
### `set_temperature_threshold(alarm_reg, temp)`

        Set temperature alarm threshold.

```python
unit_ncir2_0.set_temperature_threshold(alarm_reg, temp)
```
### `get_temp_alarm_led(alarm_reg)`

        Get temperature alaram RGB LED value.

        - Returns: temperature alarm RGB LED value.
        - Return type: list, RGB color list in the format [R, G, B], values from 0 to 255.

```python
unit_ncir2_0.get_temp_alarm_led(alarm_reg)
```
### `set_temp_alarm_led(alarm_reg, rgb)`

        Set temperature alaram RGB LED value.

        - Parameter `rgb` (`int`): RGB color value (24-bit, range: 0 ~ 0xFFFFFF).

```python
unit_ncir2_0.set_temp_alarm_led(alarm_reg, rgb)
```
### `get_temp_buzzer_freq(alarm_reg)`

        Get the buzzer frequency for temperature alarm.

        - Returns: buzzer frequency.
        - Return type: int

```python
unit_ncir2_0.get_temp_buzzer_freq(alarm_reg)
```
### `set_temp_buzzer_freq(alarm_reg, freq)`

        Set the buzzer frequency for temperature alarm.

```python
unit_ncir2_0.set_temp_buzzer_freq(alarm_reg, freq)
```
### `get_temp_alarm_interval(alarm_reg)`

        Get the buzzer alarm interval.

        - Returns: buzzer alarm interval. (unit: ms)
        - Return type: int

```python
unit_ncir2_0.get_temp_alarm_interval(alarm_reg)
```
### `set_temp_alarm_interval(alarm_reg, interval)`

        Set the buzzer alarm interval.

```python
unit_ncir2_0.set_temp_alarm_interval(alarm_reg, interval)
```
### `get_temp_buzzer_duty(duty_reg)`

        Get the duty cycle of the temperature alarm buzzer signal.

        - Parameter `duty_reg` (`int`): Duty cycle register for the temperature alarm buzzer signal. LOW_ALARM_DUTY_REG: Register for low temperature alarm duty cycle. HIGH_ALARM_DUTY_REG: Register for high temperature alarm duty cycle.
        - Returns: duty cycle.
        - Return type: int

```python
unit_ncir2_0.get_temp_buzzer_duty(duty_reg)
```
### `set_temp_buzzer_duty(duty_reg, duty)`

        Set the duty cycle of the temperature alarm buzzer signal.

        - Parameter `duty_reg` (`int`): Duty cycle register for the temperature alarm buzzer signal. LOW_ALARM_DUTY_REG: Register for low temperature alarm duty cycle. HIGH_ALARM_DUTY_REG: Register for high temperature alarm duty cycle.

```python
unit_ncir2_0.set_temp_buzzer_duty(duty_reg, duty)
```
### `get_buzzer_freq()`

        Get the frequeny of the buzzer signal.

        - Returns: frequeny(Hz)
        - Return type: int

```python
unit_ncir2_0.get_buzzer_freq()
```
### `set_buzzer_freq(freq)`

        Set the frequeny of the buzzer signal.

```python
unit_ncir2_0.set_buzzer_freq(freq)
```
### `get_buzzer_duty()`

        Get the duty cycle of the buzzer signal.

        - Returns: Duty cycle
        - Return type: int

```python
unit_ncir2_0.get_buzzer_duty()
```
### `set_buzzer_duty(duty)`

        Set the duty cycle of the buzzer signal.

```python
unit_ncir2_0.set_buzzer_duty(duty)
```
### `get_buzzer_control()`

        Get the buzzer control status

        - Returns: Returns the current buzzer control status
        - Return type: int

```python
unit_ncir2_0.get_buzzer_control()
```
### `set_buzzer_control(ctrl)`

        Set the buzzer control status

```python
unit_ncir2_0.set_buzzer_control(ctrl)
```
### `get_rgb_led()`

        Get the current RGB LED value

        - Returns: The current RGB LED values in the format [r, g, b]
        - Return type: list

```python
unit_ncir2_0.get_rgb_led()
```
### `set_rgb_led(rgb)`

        Set the RGB LED value

```python
unit_ncir2_0.set_rgb_led(rgb)
```
### `get_button_status()`

        Get the button status

        - Returns: Button status, either 0 (not pressed) or 1 (pressed)
        - Return type: bool

```python
unit_ncir2_0.get_button_status()
```
### `save_config_setting()`

        Save configuration settings

```python
unit_ncir2_0.save_config_setting()
```
### `get_chip_temperature()`

        Get the chip temperature

        - Returns: Chip temperature in Celsius (°C)
        - Return type: float

```python
unit_ncir2_0.get_chip_temperature()
```
### `get_device_spec(mode)`

        Get device specifications

        - Returns: Device specifications
        - Return type: int

```python
unit_ncir2_0.get_device_spec()
```
### `set_i2c_address(addr)`

        Set the I2C address of the device

```python
unit_ncir2_0.set_i2c_address(addr)
```
