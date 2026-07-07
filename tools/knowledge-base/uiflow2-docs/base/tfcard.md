# Atomic TFCard Base

<!-- .. sku: A135/K044 -->

<!-- .. include:: ../refs/base.tfcard.ref -->

This is the driver library for the Atomic TFCard Base, which is used to mount TFCard.

Support the following products:

    ================== =====================
    |Atom TFCard|      |Atomic TFCard Base|
    ================== =====================

## UiFlow2 Example

#### TFCard mount

Open the |atoms3r_tfcard_example.m5f2| project in UiFlow2.

This example demonstrates how to read/create a directory using Atomic TFCard Base.

UiFlow2 Code Block:

Example output:

    Files in the /sd directory.

## MicroPython Example

#### TFCard mount

This example demonstrates how to read/create a directory using Atomic TFCard Base.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2025 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

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

<!-- .. function:: AtomicTFCardBase(slot=1, width=1, cd=None, wp=None, sck=None, miso=None, mosi=None, cs=None, freq=20000000) -->

    This function is only used to initialize and mount the SD card to
    the /sd directory, and to try to unmount the existing SD card before
    mounting it. Other file operations (such as reading/writing files,
    creating directories, etc.) need to be performed by the os module.

    :param int slot: Which of the available interfaces to use. The default value is 1.
    :param int width: The bus width for the SD/MMC interface. The default value is 1.
    :param int cd: The card-detect pin to use. The default value is None.
    :param int wp: The write-protect pin to use. The default value is None.
    :param int sck: The SPI clock pin to use. The default value is None.
    :param int miso: The SPI miso pin to use. The default value is None.
    :param int mosi: The SPI mosi pin to use. The default value is None.
    :param int cs: The SPI chip select pin to use. The default value is None.
    :param int freq: The SD/MMC interface frequency in Hz. The default value is 20000000.

    :return: None

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from base import AtomicTFCardBase
            base_tfcard = AtomicTFCardBase(slot=3, width=1, sck=7, miso=8, mosi=6, freq=20000000)

    See :mod:`micropython:os` -- basic "operating system" for more details.
