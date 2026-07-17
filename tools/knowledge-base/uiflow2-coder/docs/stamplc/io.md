# StamPLC IO

`IOStamPLC` controls the StamPLC IO extension board over I2C.

## MicroPython Example

#### Voltage and current monitor

This example sets the two output channels to PWM mode, then displays the voltage and current of channel 0 and channel 1.

```python
import os, sys, io
import M5
from M5 import *
from stamplc import IOStamPLC
from stamplc import StamPLC

title0 = None
label0 = None
label1 = None
stamplc_0 = None
stamplc_io_0 = None

def setup():
    global title0, label0, label1, stamplc_0, stamplc_io_0

    M5.begin()
    Widgets.fillScreen(0x000000)
    title0 = Widgets.Title("StamPLC IO Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.Montserrat18)
    label0 = Widgets.Label("label0", 1, 42, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)
    label1 = Widgets.Label("label1", 2, 71, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.Montserrat18)

    stamplc_0 = StamPLC()
    stamplc_io_0 = IOStamPLC(address=0x20)
    stamplc_io_0.set_output_mode(IOStamPLC.PWM_MODE)
    stamplc_io_0.set_pwm_config(0, 1, 100)
    stamplc_io_0.set_pwm_config(1, 1, 100)

def loop():
    global title0, label0, label1, stamplc_0, stamplc_io_0
    M5.update()
    label0.setText(
        str(
            (
                str("ch0:")
                + str(
                    (
                        str((stamplc_io_0.get_voltage(0)))
                        + str(
                            (
                                str("mV")
                                + str(
                                    (
                                        str(", ")
                                        + str((str((stamplc_io_0.get_current(0))) + str("uA")))
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )
    label1.setText(
        str(
            (
                str("ch1:")
                + str(
                    (
                        str((stamplc_io_0.get_voltage(1)))
                        + str(
                            (
                                str("mV")
                                + str(
                                    (
                                        str(", ")
                                        + str((str((stamplc_io_0.get_current(1))) + str("uA")))
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
    )

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

#### IOStamPLC

### `class IOStamPLC(i2c=None, address=0x20)`

    Create a StamPLC IO extension object.

    - Parameter `i2c`: I2C interface. If omitted, the shared StamPLC I2C bus is used.
    - Parameter `address` (`int`): I2C address of the StamPLC IO extension.

```python
from stamplc import IOStamPLC

io = IOStamPLC(address=0x20)
```
### `get_voltage(channel)`

        Get the voltage of one channel.

        - Parameter `channel` (`int`): Channel index, `0` or `1`.
        - Returns: Voltage in mV.
        - Return type: int

```python
voltage = io.get_voltage(0)
```
### `get_current(channel)`

        Get the current of one channel.

        - Parameter `channel` (`int`): Channel index, `0` or `1`.
        - Returns: Current in uA.
        - Return type: int

```python
current = io.get_current(0)
```
### `get_io_control()`

        Get the IO control register value.

        - Returns: IO control register value.
        - Return type: int

### `set_io_control(value)`

        Set the IO control register value.

        - Parameter `value` (`int`): IO control register value.

### `set_solid_relay(channel, state)`

        Set the solid-state relay output of one channel.

        - Parameter `channel` (`int`): Channel index, `0` or `1`.
        - Parameter `state` (`bool`): `True` turns the output on, `False` turns it off.

```python
io.set_solid_relay(0, True)
```
### `get_solid_relay(channel)`

        Get the solid-state relay output state of one channel.

        - Parameter `channel` (`int`): Channel index, `0` or `1`.
        - Returns: Output state.
        - Return type: bool

### `set_ina226_pullup(channel, enable)`

        Enable or disable the INA226 pull-up of one channel.

        - Parameter `channel` (`int`): Channel index, `0` or `1`.
        - Parameter `enable` (`bool`): `True` enables the pull-up, `False` disables it.

### `get_ina226_pullup(channel)`

        Get the INA226 pull-up state of one channel.

        - Parameter `channel` (`int`): Channel index, `0` or `1`.
        - Returns: Pull-up state.
        - Return type: bool

### `set_relay(state)`

        Set the onboard relay output.

        - Parameter `state` (`bool`): `True` turns the relay on, `False` turns it off.

### `get_relay()`

        Get the onboard relay output state.

        - Returns: Relay state.
        - Return type: bool

### `set_output_mode(mode)`

        Set the output mode.

        - Parameter `mode` (`int`): `IOStamPLC.OUTPUT_IO_MODE` or `IOStamPLC.PWM_MODE`.

```python
io.set_output_mode(IOStamPLC.PWM_MODE)
```
### `get_output_mode()`

        Get the output mode.

        - Returns: `IOStamPLC.OUTPUT_IO_MODE` or `IOStamPLC.PWM_MODE`.
        - Return type: int

### `set_ina226_config(channel, value)`

        Set the INA226 configuration register of one channel.

        - Parameter `channel` (`int`): Channel index, `0` or `1`.
        - Parameter `value` (`int`): Register value.

### `get_ina226_config(channel)`

        Get the INA226 configuration register of one channel.

        - Parameter `channel` (`int`): Channel index, `0` or `1`.
        - Returns: Register value.
        - Return type: int

### `set_pwm_config(channel, freq, duty)`

        Set the PWM frequency and duty of one channel.

        - Parameter `channel` (`int`): Channel index, `0` or `1`.
        - Parameter `freq` (`int`): PWM frequency, `1` to `100`.
        - Parameter `duty` (`int`): PWM duty, `0` to `1000`.

```python
io.set_pwm_config(0, 1, 100)
```
### `get_pwm_config(channel)`

        Get the PWM frequency and duty of one channel.

        - Parameter `channel` (`int`): Channel index, `0` or `1`.
        - Returns: `(freq, duty)`.
        - Return type: tuple

### `get_firmware_version()`

        Get the firmware version.

        - Returns: Firmware version.
        - Return type: int

```python
version = io.get_firmware_version()
```
### `get_i2c_address()`

        Get the configured I2C address.

        - Returns: I2C address.
        - Return type: int

```python
address = io.get_i2c_address()
```
### `refresh_i2c_address()`

        Refresh the active I2C address from the device.
