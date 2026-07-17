
# class BLEUARTClient

BLEUARTClient class is a BLE UART client, which can connect to a BLE UART server and communicate with it.

Micropython Example:

```python
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

## Constructors

### `class bleuart.BLEUARTClient(name="", rxbuf=100, verbose=False)`

    Create a BLE UART client.

    - Parameter `name` (`str`): The name of the ble device.
    - Parameter `rxbuf` (`int`): The size of the receive buffer.
    - Parameter `verbose` (`bool`): Enable verbose output.

## Methods

### `BLEUARTClient.irq()`

    The irq of the ble uart client.

### `BLEUARTClient.is_connected()`

    Check if the ble uart server is connected.

### `BLEUARTClient.connect(name, timeout=2000)`

    Connect to the ble uart server.

    - Parameter `name` (`str`): The name of the ble device.
    - Parameter `timeout` (`int`): The timeout of the connection.

### `BLEUARTClient.any() -> int`

    Check if there is any data in the receive buffer.

    - Returns: The number of bytes in the receive buffer.

### `BLEUARTClient.read(sz=None) -> bytes`

    Read data from the receive buffer.

    - Parameter `sz` (`int`): The number of bytes to read. If not specified, read all data.

    - Returns: The data read from the receive buffer.

### `BLEUARTClient.write(data: bytes)`

    Write data to the ble uart server.

    - Parameter `data` (`bytes`): The data to write.

### `BLEUARTClient.close()`

    Close the ble uart server.

### `BLEUARTClient.deinit()`

    Deinitialize the ble uart server.
