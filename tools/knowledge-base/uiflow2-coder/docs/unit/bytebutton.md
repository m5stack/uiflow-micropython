
# ByteButton Unit

Unit ByteButton is an 8-button touch switch input unit equipped with 8 button inputs and 9 WS2812C RGB LEDs. It uses the STM32 microcontroller and supports I2C communication. The board includes two Port A interfaces and supports cascading multiple Unit ByteButton modules, making it suitable for complex systems. It can achieve button input detection and dynamic lighting feedback, ideal for smart home control, gaming devices, educational platforms, industrial status displays, and interactive exhibitions.

Support the following products:

ByteButtonUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import ByteButtonUnit
import time

title0 = None
label0 = None
label1 = None
i2c0 = None
bytebutton_0 = None

state_byte = None
i = None

def setup():
    global title0, label0, label1, i2c0, bytebutton_0, state_byte, i

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "ByteButton CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 4, 87, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 5, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    bytebutton_0 = ByteButtonUnit(i2c0, 0x47)
    bytebutton_0.set_led_show_mode(ByteButtonUnit.BYTEBUTTON_LED_USER_MODE)
    bytebutton_0.set_indicator_color(0x33FF33)
    for i in range(8):
        bytebutton_0.set_led_color(i, 0xFF0000, ByteButtonUnit.BYTEBUTTON_LED_USER_MODE)
        bytebutton_0.set_indicator_brightness(255)
        time.sleep(0.2)
        bytebutton_0.set_led_color(i + 1, 0x333300, ByteButtonUnit.BYTEBUTTON_LED_USER_MODE)
    time.sleep(1)
    for i in range(7, -1, -1):
        bytebutton_0.set_led_color(i, 0x66FF99, ByteButtonUnit.BYTEBUTTON_LED_USER_MODE)
        time.sleep(0.2)
    time.sleep(1)
    bytebutton_0.set_led_show_mode(ByteButtonUnit.BYTEBUTTON_LED_SYS_MODE)
    for i in range(8):
        bytebutton_0.set_led_color(i, 0xFFFFFF, ByteButtonUnit.BYTEBUTTON_LED_SYS_MODE, False)
        bytebutton_0.set_led_color(i, 0xFF0000, ByteButtonUnit.BYTEBUTTON_LED_SYS_MODE, True)

def loop():
    global title0, label0, label1, i2c0, bytebutton_0, state_byte, i
    M5.update()
    state_byte = bytebutton_0.get_byte_button_status()
    label0.setText(
        str(
            [
                (str("B0:") + str(((state_byte >> 0) & 0x01))),
                (str("B1:") + str(((state_byte >> 1) & 0x01))),
                (str("B2:") + str(((state_byte >> 2) & 0x01))),
                (str("B3:") + str(((state_byte >> 3) & 0x01))),
            ]
        )
    )
    label1.setText(
        str(
            [
                (str("B4:") + str(((state_byte >> 4) & 0x01))),
                (str("B5:") + str(((state_byte >> 5) & 0x01))),
                (str("B6:") + str(((state_byte >> 6) & 0x01))),
                (str("B7:") + str(((state_byte >> 7) & 0x01))),
            ]
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

## class ByteButtonUnit

## Constructors

### `class ByteButtonUnit(i2c, address)`

    Initialize the ByteButtonUnit with a specified I2C address.

    - Parameter `i2c` (`I2C`): The I2C interface instance for communication.
    - Parameter `address` (`int`): The I2C address of the ByteButtonUnit, default is 0x47.

## Methods

### `ByteButtonUnit.get_byte_button_status() -> int`

    Get the status of all buttons as an integer, where each bit represents the state of each button.

### `ByteButtonUnit.get_button_state(num) -> bool`

    Get the state of a specific button.

    - Parameter `num` (`int`): The index of the button (0-7).

### `ByteButtonUnit.get_led_show_mode() -> int`

    Get the current LED show mode.

### `ByteButtonUnit.set_led_show_mode(mode)`

    Set the LED show mode.

    - Parameter `mode` (`int`): The LED show mode to set.

        Options:
            - `BYTEBUTTON_LED_USER_MODE`: 0
            - `BYTEBUTTON_LED_SYS_MODE`: 1

### `ByteButtonUnit.set_led_brightness(num, brightness)`

    Set the brightness of a specific LED.

    - Parameter `num` (`int`): The index of the LED (0-7).
    - Parameter `brightness` (`int`): The brightness level (0-255).

### `ByteButtonUnit.get_led_brightness(num) -> int`

    Get the brightness of a specific LED.

    - Parameter `num` (`int`): The index of the LED (0-7).

### `ByteButtonUnit.set_led_color(num, color, led_show_mode, btn_is_pressed)`

    Set the color of a specific LED.

    - Parameter `num` (`int`): The index of the LED (0-7).
    - Parameter `color` (`int`): The RGB888 color value to set.
    - Parameter `led_show_mode` (`int`): The LED show mode, default is BYTEBUTTON_LED_SYS_MODE.
    - Parameter `btn_is_pressed` (`bool`): Whether the button is pressed (affects color in SYS mode).

### `ByteButtonUnit.get_led_color(num, led_show_mode, btn_is_pressed) -> int`

    Get the color of a specific LED.

    - Parameter `num` (`int`): The index of the LED (0-7).
    - Parameter `led_show_mode` (`int`): The LED show mode, default is BYTEBUTTON_LED_SYS_MODE.
    - Parameter `btn_is_pressed` (`bool`): Whether the button is pressed (affects color in SYS mode).

### `ByteButtonUnit.set_indicator_brightness(brightness)`

    Set the brightness of the indicator LED.

    - Parameter `brightness` (`int`): The brightness level (0-255).

### `ByteButtonUnit.get_indicator_brightness() -> int`

    Get the brightness of the indicator LED.

### `ByteButtonUnit.set_indicator_color(color)`

    Set the color of the indicator LED in RGB888 format.

    - Parameter `color` (`int`): The RGB888 color value to set.

### `ByteButtonUnit.get_indicator_color() -> int`

    Get the color of the indicator LED in RGB888 format.

### `ByteButtonUnit.rgb888_to_rgb233(color)`

    Convert an RGB888 color value to RGB233 format.

    - Parameter `color` (`int`): The RGB888 color value as a 32-bit integer.

### `ByteButtonUnit.set_rgb233(num, color)`

    Set the color of a specific LED in RGB233 format.

    - Parameter `num` (`int`): The index of the LED (0-7).
    - Parameter `color` (`int`): The RGB233 color value to set.

### `ByteButtonUnit.get_rgb233(num)`

    Get the color of a specific LED in RGB233 format.

    - Parameter `num` (`int`): The index of the LED (0-7).

### `ByteButtonUnit.set_irq_enable(enable)`

    Enable or disable IRQ functionality.

    - Parameter `enable` (`bool`): Whether to enable (True) or disable (False) IRQ.

### `ByteButtonUnit.get_irq_enable()`

    Get the current IRQ enable status.

### `ByteButtonUnit.save_to_flash()`

    Save the current user settings to flash.

### `ByteButtonUnit.get_firmware_version() -> int`

    Get the firmware version of the ByteButtonUnit.

### `ByteButtonUnit.set_i2c_address(new_addr)`

    Set a new I2C address for the ByteButtonUnit.

    - Parameter `new_addr` (`int`): The new I2C address to set. Must be in the range 0x08 to 0x77.

### `ByteButtonUnit.get_i2c_address() -> int`

    Get the current I2C address of the ByteButtonUnit.
