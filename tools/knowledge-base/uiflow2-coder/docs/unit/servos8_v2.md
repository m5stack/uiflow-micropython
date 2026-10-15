
# 8Servos2 Unit

The `Servos8V2Unit` class controls the Unit 8Servos2-I2C over I2C. The
device provides eight configurable channels for GPIO input, GPIO output, ADC,
servo, RGB, and PWM operation. It also provides power monitoring and device
information APIs.

Support the following products:

    Unit 8Servos2-I2C

## Constants

Use the following constants with `set_channel_mode()`:

- `MODE_INPUT`: GPIO input mode.
- `MODE_OUTPUT`: GPIO output mode.
- `MODE_ADC`: ADC input mode.
- `MODE_SERVO`: Servo control mode.
- `MODE_RGB`: RGB output mode for WS2812 LEDs.
- `MODE_PWM`: PWM duty output mode.

Use `PULL_NONE`, `PULL_UP`, or `PULL_DOWN` with
`set_input_pull()`.

> Note: Channels 0-3 share one PWM frequency, and channels 4-7 share another.
> Setting the frequency of one channel changes every channel in the same
> group. Selecting servo mode sets the channel's shared group to 50 Hz.
## MicroPython Example

#### Servo control

This example initializes Unit 8Servos2-I2C for servo control. Button A selects
a channel or the all-channel option. Buttons B and C increase or decrease the
servo angle in 10-degree steps.

```python
import os, sys, io
import M5
from M5 import *
from hardware import Pin
from hardware import I2C
from unit import Servos8V2Unit

label_title = None
label_channel = None
label_angle = None
label_sel = None
label_increase = None
label_decrease = None
i2c0 = None
servos8v2_0 = None
channel = None
angle = None
i = None

def btna_was_clicked_event(state):
    global \
        label_title, \
        label_channel, \
        label_angle, \
        label_sel, \
        label_increase, \
        label_decrease, \
        i2c0, \
        servos8v2_0, \
        channel, \
        angle, \
        i
    channel = (channel if isinstance(channel, (int, float)) else 0) + 1
    if channel >= 9:
        channel = 0
    if channel == 8:
        label_channel.setText(str("Channel: all"))
        for i in range(7):
            servos8v2_0.set_servo_angle(i, angle)
    else:
        label_channel.setText(str((str("Channel: ") + str(channel))))
        servos8v2_0.set_servo_angle(channel, angle)

def btnb_was_clicked_event(state):
    global \
        label_title, \
        label_channel, \
        label_angle, \
        label_sel, \
        label_increase, \
        label_decrease, \
        i2c0, \
        servos8v2_0, \
        channel, \
        angle, \
        i
    angle = angle + 10
    if angle >= 180:
        angle = 0
    if channel == 8:
        for i in range(7):
            servos8v2_0.set_servo_angle(i, angle)
    else:
        servos8v2_0.set_servo_angle(channel, angle)
    label_angle.setText(str((str("Angle: ") + str(angle))))

def btnc_was_clicked_event(state):
    global \
        label_title, \
        label_channel, \
        label_angle, \
        label_sel, \
        label_increase, \
        label_decrease, \
        i2c0, \
        servos8v2_0, \
        channel, \
        angle, \
        i
    angle = angle - 10
    if angle <= 0:
        angle = 180
    if channel == 8:
        for i in range(7):
            servos8v2_0.set_servo_angle(i, angle)
    else:
        servos8v2_0.set_servo_angle(channel, angle)
    label_angle.setText(str((str("Angle: ") + str(angle))))

def setup():
    global \
        label_title, \
        label_channel, \
        label_angle, \
        label_sel, \
        label_increase, \
        label_decrease, \
        i2c0, \
        servos8v2_0, \
        channel, \
        angle, \
        i

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x000000)
    label_title = Widgets.Label(
        "Servo Control", 76, 2, 1.0, 0x1393E8, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_channel = Widgets.Label(
        "Channel: 1", 36, 77, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_angle = Widgets.Label(
        "Angle: 0", 40, 112, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat24
    )
    label_sel = Widgets.Label(
        "select", 43, 210, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat16
    )
    label_increase = Widgets.Label(
        "+10", 143, 210, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat16
    )
    label_decrease = Widgets.Label(
        "-10", 233, 210, 1.0, 0xFFFFFF, 0x000000, Widgets.FONTS.Montserrat16
    )

    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btna_was_clicked_event)
    BtnB.setCallback(type=BtnB.CB_TYPE.WAS_CLICKED, cb=btnb_was_clicked_event)
    BtnC.setCallback(type=BtnC.CB_TYPE.WAS_CLICKED, cb=btnc_was_clicked_event)

    i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
    servos8v2_0 = Servos8V2Unit(i2c0, 0x25)
    channel = 0
    angle = 0
    for i in range(7):
        servos8v2_0.set_channel_mode(i, Servos8V2Unit.MODE_SERVO)
        servos8v2_0.set_servo_angle(i, 0)

def loop():
    global \
        label_title, \
        label_channel, \
        label_angle, \
        label_sel, \
        label_increase, \
        label_decrease, \
        i2c0, \
        servos8v2_0, \
        channel, \
        angle, \
        i
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

Example output:

    The screen displays the selected channel and angle, and the selected servo
    output moves when the angle is changed.

## **API**

#### Servos8V2Unit

## `Servos8V2Unit`
Create a Unit 8Servos2 object.

- Parameter `| PAHUBUnit i2c` (`machine.I2C`): The I2C bus the Unit 8Servos2 is connected to.
- Parameter ` list  tuple address` (`int`): The I2C address of the device, range 0x25 to 0x34.
    Default is 0x25.

```python
from hardware import I2C, Pin
from unit import Servos8V2Unit

i2c0 = I2C(0, scl=Pin(22), sda=Pin(21), freq=100000)
servos8v2_0 = Servos8V2Unit(i2c0, 0x25)
```

### `get_channel_mode`
Get the current mode of a specific channel.

The channel mode values:

- `MODE_INPUT`: `0x00`
- `MODE_OUTPUT`: `0x01`
- `MODE_ADC`: `0x02`
- `MODE_SERVO`: `0x03`
- `MODE_RGB`: `0x04`
- `MODE_PWM`: `0x05`

- Parameter `channel` (`int`): The channel number (0 to 7).
- Returns: The mode of the specified channel.
- Return type: int

```python
mode = servos8v2_0.get_channel_mode(0)
```

### `set_channel_mode`
Set the mode of a specific channel.

The channel mode values:

- `MODE_INPUT`: `0x00`
- `MODE_OUTPUT`: `0x01`
- `MODE_ADC`: `0x02`
- `MODE_SERVO`: `0x03`
- `MODE_RGB`: `0x04`
- `MODE_PWM`: `0x05`

When a channel is set to `MODE_SERVO`, the driver automatically sets
its shared frequency group to 50 Hz. Channels 0-3 share one frequency,
and channels 4-7 share another frequency.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Parameter `mode` (`int`): The channel mode to set.

```python
servos8v2_0.set_channel_mode(0, Servos8V2Unit.MODE_SERVO)
```

### `set_input_pull`
Set the input pull configuration of a specific channel.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Parameter `pull` (`int`): Pull configuration. Use PULL_NONE, PULL_UP, or PULL_DOWN.

```python
servos8v2_0.set_input_pull(0, Servos8V2Unit.PULL_UP)
```

### `get_input_pull`
Get the input pull configuration of a specific channel.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Returns: Pull configuration of the specified channel.
- Return type: int

```python
pull = servos8v2_0.get_input_pull(0)
```

### `get_gpio_input_value`
Get the GPIO input value of a specific channel.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Returns: True for high level, False for low level.
- Return type: bool

```python
level = servos8v2_0.get_gpio_input_value(0)
```

### `set_gpio_output_value`
Set the GPIO output value of a specific channel.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Parameter `value` (`bool`): Output value, False for low level or True for high level.

```python
servos8v2_0.set_gpio_output_value(0, True)
```

### `get_gpio_output_value`
Get the GPIO output value of a specific channel.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Returns: True for high level, False for low level.
- Return type: bool

```python
level = servos8v2_0.get_gpio_output_value(0)
```

### `get_adc_input`
Get the 12-bit ADC input value of a specific channel.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Returns: ADC value, range 0 to 4095.
- Return type: int

```python
adc = servos8v2_0.get_adc_input(0)
```

### `set_servo_angle`
Set the servo angle of a specific channel.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Parameter `angle` (`int`): Servo angle, range 0 to 180.

```python
servos8v2_0.set_servo_angle(0, 90)
```

### `get_servo_angle`
Get the servo angle of a specific channel.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Returns: Servo angle, range 0 to 180.
- Return type: int

```python
angle = servos8v2_0.get_servo_angle(0)
```

### `set_rgb_config`
Set the WS2812 LED count and refresh flag of a specific channel.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Parameter `count` (`int`): WS2812 LED count, range 0 to 16.
- Parameter `refresh` (`bool`): Whether to trigger an RGB refresh. Default is False.

```python
servos8v2_0.set_rgb_config(0, 4, refresh=True)
```

### `get_rgb_config`
Get the raw WS2812 config value of a specific channel.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Returns: Raw RGB config byte.
- Return type: int

```python
config = servos8v2_0.get_rgb_config(0)
```

### `get_rgb_count`
Get the configured WS2812 LED count of a specific channel.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Returns: WS2812 LED count, range 0 to 16.
- Return type: int

```python
count = servos8v2_0.get_rgb_count(0)
```

### `refresh_rgb`
Trigger WS2812 refresh for a specific channel.

- Parameter `channel` (`int`): The channel number (0 to 7).

```python
servos8v2_0.refresh_rgb(0)
```

### `set_rgb_buffer`
Set one WS2812 color buffer entry.

- Parameter `index` (`int`): WS2812 color buffer index, range 0 to 15.
- Parameter `color` (`int`): RGB888 color value in `0xRRGGBB` format.

```python
servos8v2_0.set_rgb_buffer(0, 0xFF0000)
```

### `get_rgb_buffer`
Get one WS2812 color buffer entry.

- Parameter `index` (`int`): WS2812 color buffer index, range 0 to 15.
- Returns: RGB888 color value in `0xRRGGBB` format.
- Return type: int

```python
color = servos8v2_0.get_rgb_buffer(0)
```

### `set_pwm_duty`
Set the PWM duty of a specific channel.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Parameter `duty` (`int`): PWM duty, range 0 to 100.

```python
servos8v2_0.set_pwm_duty(0, 50)
```

### `get_pwm_duty`
Get the PWM duty of a specific channel.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Returns: PWM duty, range 0 to 100.
- Return type: int

```python
duty = servos8v2_0.get_pwm_duty(0)
```

### `set_pwm_freq`
Set the PWM frequency of a specific channel.

Channels 0-3 share one frequency, and channels 4-7 share another frequency.
Setting the frequency of any channel changes the frequency of every channel
in the same group.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Parameter `freq` (`int`): PWM frequency in Hz, range 1 to 65535.

```python
servos8v2_0.set_pwm_freq(0, 1000)
```

### `get_pwm_freq`
Get the PWM frequency of a specific channel.

Channels 0-3 share one frequency, and channels 4-7 share another frequency.
The returned value is the shared frequency of the channel's group.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Returns: PWM frequency in Hz.
- Return type: int

```python
freq = servos8v2_0.get_pwm_freq(0)
```

### `get_reference_voltage`
Get the reference voltage.

- Returns: Reference voltage in mV.
- Return type: int

```python
voltage = servos8v2_0.get_reference_voltage()
```

### `get_grove_voltage`
Get the Grove port voltage.

- Returns: Grove port voltage in mV.
- Return type: int

```python
voltage = servos8v2_0.get_grove_voltage()
```

### `get_dc_voltage`
Get the DC input voltage.

- Returns: DC input voltage in mV.
- Return type: int

```python
voltage = servos8v2_0.get_dc_voltage()
```

### `get_current`
Get the system current.

- Returns: System current in mA.
- Return type: int

```python
current = servos8v2_0.get_current()
```

### `get_firmware_version`
Get the firmware version.

- Returns: Firmware version.
- Return type: int

```python
version = servos8v2_0.get_firmware_version()
```

### `get_i2c_address`
Get the current I2C address.

- Returns: Current I2C address.
- Return type: int

```python
address = servos8v2_0.get_i2c_address()
```

### `get_uid`
Get the 12-byte device UID.

- Returns: Tuple containing the 12 UID bytes.
- Return type: tuple

```python
uid = servos8v2_0.get_uid()
```
