# Commu Module

This is the driver library for the module Commu for receiving and sending CAN / RS485 / I2C data.

Support the following products:

    commu

## MicroPython Example

#### CAN, RS485, I2C communication

This example shows how to receive and send data using the Commu Module.

```python
import os, sys, io
import M5
from M5 import *
from module import CommuModuleCAN
from module import CommuModuleRS485
from module import CommuModuleI2C
from hardware import Pin

title0 = None
label0 = None
label1 = None
label2 = None
commu_0 = None
commu_1 = None
commu_2 = None

def setup():
    global title0, label0, label1, label2, commu_0, commu_1, commu_2

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "COMMUModule Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("CAN Rec:", 1, 77, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("RS485 Rec:", 1, 121, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("I2C List:", 1, 166, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    commu_0 = CommuModuleCAN(0x00, baudrate=16)
    commu_1 = CommuModuleRS485(2, baudrate=115200, bits=8, parity=None, stop=1, tx=14, rx=13)
    commu_2 = CommuModuleI2C(0, scl=Pin(22), sda=Pin(21), freq=100000)

def loop():
    global title0, label0, label1, label2, commu_0, commu_1, commu_2
    M5.update()
    if commu_0.any():
        label0.setText(str((str("CAN Rec:") + str((commu_0.recv())))))
    if BtnA.isPressed():
        commu_0.send("uiflow2", 0, extframe=False)
    elif BtnB.isPressed():
        label2.setText(str((str("I2C List:") + str((commu_2.scan())))))
    if commu_1.any():
        label1.setText(str((str("RS485 Rec:") + str((commu_1.read())))))

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

#### CommuModule

## `CommuModuleCAN`
Create an CommuModuleCAN object

- Parameter `mode` (`int`): The CAN mode to use(NORMAL, LISTEN_ONLY), Default is NORMAL.

    Options:
        - `NORMAL`: Normal mode
        - `LISTEN_ONLY`: Listen only mode

- Parameter `baudrate` (`int`): The baudrate to use, Default is CAN_1000KBPS.

    Options:
        - `CAN_5KBPS`: 5Kbps
        - `CAN_10KBPS`: 10Kbps
        - `CAN_20KBPS`: 20Kbps
        - `CAN_31K25BPS`: 31.25Kbps
        - `CAN_33KBPS`: 33Kbps
        - `CAN_40KBPS`: 40Kbps
        - `CAN_50KBPS`: 50Kbps
        - `CAN_80KBPS`: 80Kbps
        - `CAN_83K3BPS`: 83.33Kbps
        - `CAN_95KBPS`: 95Kbps
        - `CAN_100KBPS`: 100Kbps
        - `CAN_125KBPS`: 125Kbps
        - `CAN_200KBPS`: 200Kbps
        - `CAN_250KBPS`: 250Kbps
        - `CAN_500KBPS`: 500Kbps
        - `CAN_1000KBPS`: 1Mbps

- Parameter `spi_baud` (`int`): The SPI baudrate to use, Default is 8000000.
- Parameter `canIDMode` (`int`): The CAN ID mode to use(MCP_STDEXT, MCP_EXTDONLY), Default is MCP_STDEXT.

    Options:
        - `MCP_STDEXT`: Standard and Extended
        - `MCP_EXTDONLY`: Extended only

- Parameter `debug` (`bool`): Whether to enable debug mode, Default is False.

```python
from module import CommuModuleCAN

commu = CommuModuleCAN(CommuModule.NORMAL, baudrate=16)
```

### `info`
Get the state of error information.

- Returns: The current error information.
- Return type: str

```python
commu.info()
```

### `reset`

### `get_irq_state`

### `any`
Check if any message is available.

- Returns: The current message availability.
- Return type: bool

```python
commu.any()
```

### `clear_interrupts`

### `recv`
Read a message from the CAN bus.

- Parameter `fifo` (`int`): The fifo is an integer, it can be any number and compatible with Pyb.CAN
- Parameter `list` (`list`): list is an optional list object to be used as the return value.
- Parameter `timeout` (`int`): timeout is the timeout in milliseconds to wait for the receive.
- Returns: Tuple containing (can_id, is_extended, is_rtr, fmi, data)
- Return type: tuple

    - The id of the message.
    - A boolean that indicates if the message ID is standard or extended.
    - A boolean that indicates if the message is an RTR message.
    - The FMI (Filter Match Index) value.
    - An array containing the data.

```python
commu.recv(0)

buf = bytearray(8)
lst = [0, 0, 0, 0, memoryview(buf)]
# No heap memory is allocated in the following call
commu.recv(0, lst)
```

### `send`
Send a message to the CAN bus.

- Parameter `data` (`str`): The message data.
- Parameter `can_id` (`int`): The CAN ID.
- Parameter `extframe` (`bool`): Whether to use extended frame format.
- Returns: The message data.
- Return type: str

```python
commu.send('uiflow2', 0, extframe=False)
```

### `commu_can_debug`

### `deinit`

### `commu_can_config_rate`

## `CommuModuleRS485`

    The `CommuModuleRS485` class wraps an instance of the `UART` class.

    For more details, see `hardware.UART <hardware.UART>`.

## `CommuModuleI2C`

    The `CommuModuleI2C` class wraps an instance of the `I2C` class.

    For more details, see `machine.I2C <machine.I2C>`. -- a two-wire serial protocol.
