<!-- .. currentmodule:: bleuart -->

# class BLEUARTClient

<!-- .. include:: ../refs/system.bleuart.client.ref -->

BLEUARTClient class is a BLE UART client, which can connect to a BLE UART server and communicate with it.

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from bleuart import *
import time

ble_central = None

nums = None
i = None

def setup():
    global ble_central, nums, i

    M5.begin()
    ble_central = BLEUARTClient()
    ble_central.connect("ble-uart", timeout=2000)
    while not (ble_central.is_connected()):
        time.sleep_ms(100)
    print("Connected")
    nums = [4, 8, 15, 16, 23, 46]
    i = 1
    while True:
        ble_central.write((str((nums[int(i - 1)]))))
        i = (i + 1) % len(nums)
        time.sleep(1)
        print((str("rx:") + str(((ble_central.read()).decode()))))
    ble_central.close()
    ble_central.deinit()

def loop():
    global ble_central, nums, i
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

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |atoms3_bleuart_client_example.m5f2|

## Constructors

<!-- .. class:: bleuart.BLEUARTClient(name="", rxbuf=100, verbose=False) -->

    Create a BLE UART client.

    :param str name: The name of the ble device.
    :param int rxbuf: The size of the receive buffer.
    :param bool verbose: Enable verbose output.

    UIFLOW2:

## Methods

<!-- .. method:: BLEUARTClient.irq() -->

    The irq of the ble uart client.

<!-- .. method:: BLEUARTClient.is_connected() -->

    Check if the ble uart server is connected.

    UIFLOW2:

<!-- .. method:: BLEUARTClient.connect(name, timeout=2000) -->

    Connect to the ble uart server.

    :param str name: The name of the ble device.
    :param int timeout: The timeout of the connection.

    UIFLOW2:

<!-- .. method:: BLEUARTClient.any() -> int -->

    Check if there is any data in the receive buffer.

    :return: The number of bytes in the receive buffer.

    UIFLOW2:

<!-- .. method:: BLEUARTClient.read(sz=None) -> bytes -->

    Read data from the receive buffer.

    :param int sz: The number of bytes to read. If not specified, read all data.

    :return: The data read from the receive buffer.

    UIFLOW2:

<!-- .. method:: BLEUARTClient.write(data: bytes) -->

    Write data to the ble uart server.

    :param bytes data: The data to write.

    UIFLOW2:

<!-- .. method:: BLEUARTClient.close() -->

    Close the ble uart server.

    UIFLOW2:

<!-- .. method:: BLEUARTClient.deinit() -->

    Deinitialize the ble uart server.

    UIFLOW2:
