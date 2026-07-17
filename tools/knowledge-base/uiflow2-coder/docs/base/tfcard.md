# Atomic TFCard Base

This is the driver library for the Atomic TFCard Base, which is used to mount TFCard.

Support the following products:

    Atom TFCard      Atomic TFCard Base

## MicroPython Example

#### TFCard mount

This example demonstrates how to read/create a directory using Atomic TFCard Base.

```python
import os, sys, io
import M5
from M5 import *
from base import AtomicTFCardBase
import time

title0 = None
base_tfcard = None

def setup():
    global title0, base_tfcard

    M5.begin()
    title0 = Widgets.Title("TFCard e.g.", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18)

    base_tfcard = AtomicTFCardBase(slot=3, width=1, sck=7, miso=8, mosi=6, freq=1000000)
    os.chdir("/sd")
    print((str("Current dir:") + str((os.getcwd()))))
    print((str("list /sd/dir: ") + str((os.listdir("/sd/")))))
    if not ("sdcard_test" in os.listdir("/sd/")):  # noqa: E713
        print("Try create 'sdcard_test' directory in /sd/")
        os.mkdir("/sd/sdcard_test")
    print((str("'sdcard_test' is directory?:") + str((os.stat("/sd/sdcard_test")[0] == 0x4000))))
    print((str("'sdcard_test' is file?:") + str((os.stat("/sd/sdcard_test")[0] == 0x8000))))
    print("Delay 1s to delete 'sdcard_test' directory")
    time.sleep(1)
    os.rmdir("/sd/sdcard_test")
    if not ("sdcard_test" in os.listdir("/sd/")):  # noqa: E713
        print("Directory 'sdcard_test' deleted successfully")

def loop():
    global title0, base_tfcard
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

    Files in the /sd directory.

## **API**

#### function AtomicTFCardBase

### `AtomicTFCardBase(slot=1, width=1, cd=None, wp=None, sck=None, miso=None, mosi=None, cs=None, freq=20000000)`

    This function is only used to initialize and mount the SD card to
    the /sd directory, and to try to unmount the existing SD card before
    mounting it. Other file operations (such as reading/writing files,
    creating directories, etc.) need to be performed by the os module.

    - Parameter `slot` (`int`): Which of the available interfaces to use. The default value is 1.
    - Parameter `width` (`int`): The bus width for the SD/MMC interface. The default value is 1.
    - Parameter `cd` (`int`): The card-detect pin to use. The default value is None.
    - Parameter `wp` (`int`): The write-protect pin to use. The default value is None.
    - Parameter `sck` (`int`): The SPI clock pin to use. The default value is None.
    - Parameter `miso` (`int`): The SPI miso pin to use. The default value is None.
    - Parameter `mosi` (`int`): The SPI mosi pin to use. The default value is None.
    - Parameter `cs` (`int`): The SPI chip select pin to use. The default value is None.
    - Parameter `freq` (`int`): The SD/MMC interface frequency in Hz. The default value is 20000000.

    - Returns: None

```python
from base import AtomicTFCardBase
base_tfcard = AtomicTFCardBase(slot=3, width=1, sck=7, miso=8, mosi=6, freq=20000000)
```
    See `micropython:os` -- basic "operating system" for more details.
