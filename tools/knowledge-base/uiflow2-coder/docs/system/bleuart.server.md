
# class BLEUARTServer

BLEUARTServer class is a BLE UART server, which can be connected to by a BLE UART client and communicate with it.

Micropython Example:

```python
import os, sys, io
import M5
from M5 import *
from bleuart import *
import time

label0 = None
ble_periph = None

data = None

def setup():
    global label0, ble_periph, data

    M5.begin()
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("Text", 20, 31, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    ble_periph = BLEUARTServer(name="ble-uart")

def loop():
    global label0, ble_periph, data
    M5.update()
    if (ble_periph.any()) > 0:
        data = ble_periph.read()
        label0.setText(str(data))
        ble_periph.write(data)
    else:
        time.sleep_ms(100)

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

### `class bleuart.BLEUARTServer(name="", rxbuf=100, verbose=False)`

    Create a BLE UART server.

    - Parameter `name` (`str`): The name of the ble device.
    - Parameter `rxbuf` (`int`): The size of the receive buffer.
    - Parameter `verbose` (`bool`): Enable verbose output.

## Methods

### `BLEUARTServer.irq()`

    The irq of the ble uart server.

### `BLEUARTServer.any() -> int`

    Check if there is any data in the receive buffer.

    - Returns: The number of bytes in the receive buffer.

### `BLEUARTServer.read(sz=None) -> bytes`

    Read data from the receive buffer.

    - Parameter `sz` (`int`): The number of bytes to read. If not specified, read all data.

    - Returns: The data read from the receive buffer.

### `BLEUARTServer.write(data: bytes)`

    Write data to the ble uart server.

    - Parameter `data` (`bytes`): The data to write.

### `BLEUARTServer.close()`

    Close the ble uart server.

### `BLEUARTServer.deinit()`

    Deinitialize the ble uart server.
