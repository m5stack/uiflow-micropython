
# Encoder8 Unit

UNIT 8Encoder is a set of 8 rotary encoders as one of the input unit, the internal use of STM32 single-chip microcomputer as the acquisition and communication processor, and the host computer using I2C communication interface, each rotary encoder corresponds to 1 RGB LED light, encoder in addition to left and right rotation, but also radially pressed, in addition to a physical toggle switch and its corresponding RGB LED light, including 5V->3V3 DCDC circuit.

Support the following products:

Encoder8Unit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import Encoder8Unit

label0 = None
title0 = None
label1 = None
label2 = None
i2c0 = None
encoder8_0 = None

def setup():
    global label0, title0, label1, label2, i2c0, encoder8_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 2, 72, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    title0 = Widgets.Title(
        "8EncoderUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label("label1", 2, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 2, 161, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    encoder8_0 = Encoder8Unit(i2c0, 0x41)
    encoder8_0.set_led_rgb_from(1, 8, 0x33FF33)
    encoder8_0.set_counter_value(1, 0)

def loop():
    global label0, title0, label1, label2, i2c0, encoder8_0
    M5.update()
    label0.setText(str((str("CH1 Counter Value:") + str((encoder8_0.get_counter_value(1))))))
    label1.setText(str((str("CH1 Button State:") + str((encoder8_0.get_button_status(1))))))
    label2.setText(str((str("Switch State:") + str((encoder8_0.get_switch_status())))))

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

## class Encoder8Unit

## Constructors

### `class Encoder8Unit(i2c, slave_addr, address)`

    Initialize the Encoder8 Unit with the specified I2C interface and address.

    - Parameter `i2c`: The I2C interface or PAHUBUnit instance for communication.
    - Parameter `slave_addr` (`int`): Deprecated parameter, kept for backward compatibility.
    - Parameter `address` (`int`): The I2C address of the Encoder8 Unit. Default is 0x41.

## Methods

### `Encoder8Unit.init_i2c_address(slave_addr)`

    Set or change the I2C address of the Encoder8 Unit.

    - Parameter `slave_addr` (`int`): The new I2C address to set.

### `Encoder8Unit.available()`

    Check if the Encoder8 Unit is connected on the I2C bus.

### `Encoder8Unit.get_counter_value(channel)`

    Get the current counter value of the specified channel.

    - Parameter `channel` (`int`): The encoder channel (1-8). Default is 1.

    - Returns: The current counter value as an integer.

### `Encoder8Unit.set_counter_value(channel, value)`

    Set the counter value for the specified channel.

    - Parameter `channel` (`int`): The encoder channel (1-8). Default is 1.
    - Parameter `value` (`int`): The counter value to set.

### `Encoder8Unit.get_increment_value(channel)`

    Get the incremental value of the specified channel.

    - Parameter `channel` (`int`): The encoder channel (1-8). Default is 1.

    - Returns: The incremental value as an integer.

### `Encoder8Unit.reset_counter_value(channel)`

    Reset the counter value for the specified channel.

    - Parameter `channel` (`int`): The encoder channel (1-8). Default is 1.

### `Encoder8Unit.get_button_status(channel)`

    Get the button status for the specified channel.

    - Parameter `channel` (`int`): The encoder channel (1-8). Default is 1.

    - Returns: True if the button is pressed, False otherwise.

### `Encoder8Unit.get_switch_status()`

    Get the status of the global switch.

    - Returns: True if the switch is on, False otherwise.

### `Encoder8Unit.set_led_rgb(channel, rgb)`

    Set the RGB color of the specified channel&#x27;s LED.

    - Parameter `channel` (`int`): The encoder channel (1-8). Default is 1.
    - Parameter `rgb` (`int`): The RGB color value (0-0xFFFFFF). Default is 0.

### `Encoder8Unit.set_led_rgb_from(begin, end, rgb)`

    Set the RGB color for a range of channels&#x27; LEDs.

    - Parameter `begin` (`int`): The starting channel index. Default is 0.
    - Parameter `end` (`int`): The ending channel index. Default is 0.
    - Parameter `rgb` (`int`): The RGB color value (0-0xFFFFFF). Default is 0.

### `Encoder8Unit.get_device_status(mode)`

    Get the device firmware version or I2C address.

    - Parameter `mode` (`int`): The mode to read. 0xFE for firmware version, 0xFF for I2C address. Default is 0xFE.

    - Returns: The value read from the specified mode register.

### `Encoder8Unit.set_i2c_address(addr)`

    Set a new I2C address for the device.

    - Parameter `addr` (`int`): The new I2C address. Default is 0x41.

### `Encoder8Unit.read_reg_data(reg, num)`

    Read data from a specified register.

    - Parameter `reg` (`int`): The register address to read from.
    - Parameter `num` (`int`): The number of bytes to read.

### `Encoder8Unit.write_reg_data(reg, byte_lst)`

    Write data to a specified register.

    - Parameter `reg`: The register address to write to.
    - Parameter `byte_lst`: A list of bytes to write to the register.

### `Encoder8Unit.deinit()`

    Deinitialize the Encoder8 Unit instance.
