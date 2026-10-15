
# Chain 8Servos2

The `Servos8V2Chain` class controls the Unit 8Servos2-Chain through a
`ChainBus`. The device provides eight configurable channels for GPIO input,
GPIO output, ADC, servo, RGB, and PWM operation. It also provides power
monitoring, UID, firmware, bootloader, and device type APIs.

Support the following products:

    Unit 8Servos2-Chain

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

#### Basic control

This example reads device information and power values from Unit
8Servos2-Chain, then moves each servo channel between 0 and 180 degrees.

```python
import M5
from M5 import *
from chain import ChainBus
from chain import Servos8V2Chain
import time

title = None
label_angle = None
label_timer = None
label_power = None
label_state = None
bus2 = None
servos8v2_0 = None
last_move = 0
position = 0

ANGLES = (45, 135)

def require_ok(result, action):
    if not result:
        raise RuntimeError(action + " failed")

def setup():
    global title, label_angle, label_timer, label_power, label_state
    global bus2, servos8v2_0, last_move

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    title = Widgets.Title("Chain 8Servos2 Servo", 3, 0xFFFFFF, 0x0055AA, Widgets.FONTS.DejaVu18)
    label_angle = Widgets.Label(
        "All channels: 90 deg", 10, 58, 1.0, 0x17E6CF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_timer = Widgets.Label(
        "Servo PWM: 50 Hz", 10, 98, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_power = Widgets.Label(
        "Use external servo power", 10, 138, 1.0, 0xFFD166, 0x222222, Widgets.FONTS.DejaVu18
    )
    label_state = Widgets.Label(
        "Sweeps 45 <-> 135 deg", 10, 178, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )

    bus2 = ChainBus(2, tx=21, rx=22)
    servos8v2_0 = Servos8V2Chain(bus2, 1)
    for channel in range(8):
        require_ok(
            servos8v2_0.set_channel_mode(channel, Servos8V2Chain.MODE_SERVO),
            "set IO%d servo mode" % channel,
        )
    for channel in range(8):
        require_ok(servos8v2_0.set_servo_angle(channel, 90), "center servo %d" % channel)
    modes = tuple(servos8v2_0.get_channel_mode(channel) for channel in range(8))
    freqs = (
        servos8v2_0.get_pwm_freq(0),
        servos8v2_0.get_pwm_freq(4),
    )
    label_timer.setText("PWM groups: %d / %d Hz" % freqs)
    label_state.setText("Mode: %s" % ("OK" if modes == (3,) * 8 else str(modes)))
    last_move = time.ticks_ms()
    print("Chain 8Servos2: modes =", modes, "PWM groups =", freqs)
    print("Chain 8Servos2: all channels centered at 90 degrees")

def loop():
    global last_move, position

    M5.update()
    if time.ticks_diff(time.ticks_ms(), last_move) < 1500:
        return
    last_move = time.ticks_ms()
    angle = ANGLES[position]
    position = (position + 1) % len(ANGLES)
    for channel in range(8):
        require_ok(servos8v2_0.set_servo_angle(channel, angle), "set servo %d angle" % channel)
    label_angle.setText("All channels: %d deg" % angle)
    print("Servo angle:", angle)

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            if bus2 is not None:
                bus2.deinit()
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")
```

Example output:

    Device information and power values are printed to the serial console,
    and each connected servo moves through the test sequence.

## **API**

#### Servos8V2Chain

## `Servos8V2Chain`
Unit 8Servos2 Chain device.

- Parameter `bus` (`ChainBus`): The Chain bus instance.
- Parameter `device_id` (`int`): The device ID on the Chain bus.

```python
from chain import ChainBus
from chain import Servos8V2Chain

bus2 = ChainBus(2, tx=21, rx=22)
servos8v2_0 = Servos8V2Chain(bus2, 1)
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

- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
servos8v2_0.set_channel_mode(0, Servos8V2Chain.MODE_SERVO)
```

### `set_input_pull`
Set the input pull configuration of a specific channel.

- Parameter `channel` (`int`): The channel number (0 to 7).
- Parameter `pull` (`int`): Pull configuration. Use PULL_NONE, PULL_UP, or PULL_DOWN.

- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
servos8v2_0.set_input_pull(0, Servos8V2Chain.PULL_UP)
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

- Returns: True if the operation was successful, False otherwise.
- Return type: bool

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

- Returns: True if the operation was successful, False otherwise.
- Return type: bool

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

- Returns: True if the operation was successful, False otherwise.
- Return type: bool

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

- Returns: True if the operation was successful, False otherwise.
- Return type: bool

```python
servos8v2_0.refresh_rgb(0)
```

### `set_rgb_buffer`
Set one WS2812 color buffer entry.

- Parameter `index` (`int`): WS2812 color buffer index, range 0 to 15.
- Parameter `color` (`int`): RGB888 color value in `0xRRGGBB` format.

- Returns: True if the operation was successful, False otherwise.
- Return type: bool

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

- Returns: True if the operation was successful, False otherwise.
- Return type: bool

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

- Returns: True if the operation was successful, False otherwise.
- Return type: bool

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

### `get_uid`
Get the device UID.

- Parameter `uid_type` (`int`): UID type. Use 0 for 4-byte UID or 1 for 12-byte UID. Default is 0.
- Returns: Tuple of UID bytes. Returns an empty tuple if failed.
- Return type: tuple

```python
uid = servos8v2_0.get_uid(0)
```

### `get_bootloader_version`
Get the bootloader version.

- Returns: Bootloader version, or None if failed.
- Return type: int

```python
version = servos8v2_0.get_bootloader_version()
```

### `get_firmware_version`
Get the firmware version.

- Returns: Firmware version.
- Return type: int

```python
version = servos8v2_0.get_firmware_version()
```

### `get_device_type`
Get the Chain device type.

- Returns: Device type. Unit 8Servos2 Chain is 0x000C.
- Return type: int

```python
device_type = servos8v2_0.get_device_type()
```

    For general Chain device methods, refer to
    `KeyChain <chain.key.KeyChain>`.
