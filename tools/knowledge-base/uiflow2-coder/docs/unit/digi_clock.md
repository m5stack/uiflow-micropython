# DigiClock Unit

UNIT-Digi-Clock is a 2.1 inch 4-digit 7-segment display module. There are
decimal points on each digit and an extra wire for colon-dots in the center,
which can display Decimals and Clock. This module adopts TM1637 as the driver
IC, and STM32F030 as I2C communication. I2C address can be modified per 4-bit
dip switch. The red LED supports 8 brightness. And we have reserved 4 fixing
holes there.

Support the following products:

    DigiClockUnit

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from hardware import *
from unit import DigiClockUnit
import time

label0 = None
i2c0 = None
digiclock_0 = None

now = None

def setup():
    global label0, i2c0, digiclock_0, now

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 99, 97, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu40)

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    digiclock_0 = DigiClockUnit(i2c0, 0x30)
    now = str((str(((time.localtime())[3])) + str(":"))) + str(((time.localtime())[4]))
    digiclock_0.set_string(now)
    label0.setText(str(now))

def loop():
    global label0, i2c0, digiclock_0, now
    M5.update()
    if now != (str((str(((time.localtime())[3])) + str(":"))) + str(((time.localtime())[4]))):
        now = str((str(((time.localtime())[3])) + str(":"))) + str(((time.localtime())[4]))
        label0.setText(str(now))
        digiclock_0.set_string(now)
    digiclock_0.set_raw(1, 2)
    time.sleep(1)
    digiclock_0.set_raw(0, 2)
    time.sleep(1)

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

## class DigiClockUnit

## Constructors

### `class DigiClockUnit(i2c: I2C, address: int  list  tuple = 0x30)`

    Initialize the DigiClockUnit.

    - Parameter `i2c` (`I2C`): I2C port to use.
    - Parameter ` list  tuple address` (`int`): I2C address of the DigiClockUnit.

## Methods

### `DigiClockUnit.clear() -> None`

    Clear the display.

### `DigiClockUnit.set_brightness(brightness: int) -> None`

    Set the brightness of the display.

    - Parameter `brightness` (`int`): The brightness of the display, range from 0 to 8.

### `DigiClockUnit.set_raw(data: int, index: int) -> None`

    Write raw data to the display.

    - Parameter `data` (`int`): The data to write.
    - Parameter `index` (`int`): The index of the data, range from 0 to 4.

### `DigiClockUnit.set_char(char: str, index: int) -> None`

    Write a character to the display.

    - Parameter `char` (`str`): The character to write.
    - Parameter `index` (`int`): The index of the character, range from 0 to 4.

### `DigiClockUnit.set_string(string: str) -> None`

    Write a string to the display.

    - Parameter `string` (`str`): The string to write.

### `DigiClockUnit.get_fw_version() -> int`

    Get the firmware version of the DigiClockUnit.

    - Returns: The firmware version.
