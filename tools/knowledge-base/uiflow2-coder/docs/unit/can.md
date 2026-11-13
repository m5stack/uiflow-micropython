

# CANUnit

The CAN Unit is used to communicate via the CAN bus.
The following products are supported:

    CAN Unit         MiniCAN Unit

## MicroPython Example

#### TX Example

This example demonstrates how to transmit data using CAN Unit.

```python
import os, sys, io
import M5
from M5 import *
from unit import CANUnit
from hardware import *

label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
can_0 = None

import random

id2 = None
payload = None

def setup():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        can_0, \
        id2, \
        payload

    M5.begin()
    label0 = Widgets.Label("Master", 35, 4, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("ID:", 4, 39, 1.0, 0xF5A41D, 0x080808, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("RTR:", 4, 90, 1.0, 0xF5A41D, 0x000000, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("Ext:", 4, 141, 1.0, 0xF5A41D, 0x000000, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Msg:", 3, 192, 1.0, 0xF5A41D, 0x000000, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("label5", 3, 64, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("label6", 4, 115, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("label7", 4, 166, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label8 = Widgets.Label("label8", 4, 217, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    can_0 = CANUnit((33, 32), CANUnit.NORMAL, baudrate=25000)
    id2 = 123
    payload = "uiflow2"
    label5.setText(str(id2))
    label6.setText(str(False))
    label7.setText(str(False))
    label0.setText(str(payload))

def loop():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        can_0, \
        id2, \
        payload
    M5.update()
    can_0.send(payload, id2, timeout=0, rtr=False, extframe=False)
    if BtnA.wasClicked():
        id2 = random.randint(1, 100)
        label5.setText(str(id2))
        payload = str((random.randint(32, 126)))
        label8.setText(str(payload))

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

#### RX Example

This example demonstrates how to receive data using CAN Unit.

```python
import os, sys, io
import M5
from M5 import *
from unit import MiniCANUnit

label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
minican_0 = None

frame = None

def setup():
    global label0, label1, label2, label3, label4, label5, label6, label7, label8, minican_0, frame

    M5.begin()
    label0 = Widgets.Label("Slaver", 90, 13, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("ID:", 35, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("Ext:", 25, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("RTR:", 20, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("Msg:", 18, 90, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("label5", 72, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("label6", 72, 89, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("label7", 72, 120, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label8 = Widgets.Label("label8", 72, 150, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    minican_0 = MiniCANUnit((1, 2), MiniCANUnit.NORMAL, baudrate=25000)

def loop():
    global label0, label1, label2, label3, label4, label5, label6, label7, label8, minican_0, frame
    M5.update()
    if minican_0.any(0):
        frame = minican_0.recv(0, timeout=5000)
        label5.setText(str(frame[0]))
        label6.setText(str(frame[4]))
        label7.setText(str(frame[2]))
        label8.setText(str(frame[1]))

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

    Screen will display the received CAN data.

## API

#### CANUnit

### `class CANUnit(id=0, port=None, mode=CANUnit.NORMAL, prescaler=0, sjw=0, bs1=0, bs2=0, triple_sampling=False, quantum_resolution_hz=0, baudrate=0, verbose=False)`

    Create a CANUnit object. Supply `port=(rx_pin, tx_pin)` for the connected
    controller; the default `None` does not select pins automatically.

    - Parameter `id` (`int`): The hardware CAN controller ID; the current binding accepts only `0`.
    - Parameter `port` (`tuple`): The port pins in **(rx, tx)** order.
    - Parameter `mode` (`int`): CANUnit.NORMAL, CANUnit.NO_ACKNOWLEDGE, or CANUnit.LISTEN_ONLY.
    - Parameter `prescaler` (`int`): Nominal bit-time prescaler for manual timing.
    - Parameter `sjw` (`int`): Resynchronisation jump width in time quanta.
    - Parameter `bs1` (`int`): Time segment before the sample point, in time quanta.
    - Parameter `bs2` (`int`): Time segment after the sample point, in time quanta.
    - Parameter `triple_sampling` (`bool`): Enable triple sampling.
    - Parameter `quantum_resolution_hz` (`int`): Time-quanta clock frequency in Hz.
    - Parameter `baudrate` (`int`): Bus bitrate in bits per second. Use a nonzero value for automatic timing.
    - Parameter `verbose` (`bool`): Print the selected configuration.

```python
from unit import CANUnit

# Automatic timing, 125 kbit/s. Choose pins for your controller.
can = CANUnit(id=0, port=(13, 14), mode=CANUnit.NORMAL, baudrate=125000)
```
    Alternatively, configure manual timing instead of setting `baudrate`:

```python
can = CANUnit(
    id=0, port=(13, 14), mode=CANUnit.NORMAL,
    prescaler=128, sjw=3, bs1=16, bs2=8,
    triple_sampling=False,
)
```
> Note: CANUnit inherits CAN. See `hardware.CAN <hardware.CAN>`
> for timing constraints and supported controller IDs on each target.
#### Methods

CANUnit and MiniCANUnit inherit the following methods from `m5can.CAN`.
`MiniCANUnit` is an alias of `CANUnit`.

### `CANUnit.init(mode, tx, rx, quanta_resolution_hz=2500000, brp=0, tseg_1=15, tseg_2=4, sjw=3, triple_sampling=False, baudrate=0)`

    Start a deinitialized controller. Call `deinit()` first when it is active.
    This method uses separate `tx`/`rx` pins and `baudrate` in **kbit/s**.
    The constructor uses `port=(rx, tx)` and baudrate in **bits per second**.
    See `hardware.CAN.init` for native timing parameters.

    - Returns: `None`.

    Raises `ValueError`: Unsupported automatic bitrate.

    Raises `OSError`: Controller initialization fails.

### `CANUnit.deinit()`

    Stop the controller and release its driver.

    - Returns: `None`.

    Raises `OSError`: Driver removal fails.

### `CANUnit.restart()`

    Stop and start an enabled controller with its existing configuration.
    A deinitialized controller stays disabled.

    - Returns: `None`.

    Raises `OSError`: The controller cannot be started.

### `CANUnit.state()`

    - Returns: `STOPPED` (0), `BUS_OFF` (4), `RECOVERING` (5), or `RUNNING` (6).
    - Return type: int

    Raises `OSError`: Reading controller status fails.

### `CANUnit.info([list])`

    - Parameter `list` (`list`): Optional list of at least eight entries, updated in place.
        Omit this argument to allocate a list.
    - Returns: `[TEC, REC, 0, 0, 0, pending_tx, pending_rx, 0]` while enabled.
        See `hardware.CAN.info` for behavior after deinitialization.

    Raises `TypeError`: The supplied argument is not a list.

    Raises `ValueError`: The supplied list has fewer than eight entries.

    Raises `OSError`: Reading controller status fails.

### `CANUnit.any(fifo)`

    - Parameter `fifo` (`int`): Compatibility argument; use `0`.
    - Returns: `True` if a frame is waiting, otherwise `False`.

    Raises `OSError`: Reading controller status fails.

### `CANUnit.send(data, id, *, timeout=0, rtr=False, extframe=False)`

    - Parameter `data`: Readable buffer of at most eight bytes, such as `bytes` or `bytearray`.
    - Parameter `id` (`int`): Standard 11-bit identifier, or 29-bit identifier with `extframe=True`.
    - Parameter `timeout` (`int`): TX queue wait in FreeRTOS ticks; standard UiFlow2 builds use 1 ms ticks.
    - Parameter `rtr` (`bool`): Send a remote request, using the buffer length as DLC.
    - Parameter `extframe` (`bool`): Use an extended identifier.
    - Returns: `None` after queueing; receipt by another node is not confirmed.

    Raises `TypeError`: `data` does not support the buffer protocol.

    Raises `ValueError`: The buffer exceeds eight bytes.

    Raises `OSError`: The driver rejects an argument, or queueing fails or times out.

### `CANUnit.recv(fifo, list=None, *, timeout=5000)`

    - Parameter `fifo` (`int`): Compatibility argument; use `0`.
    - Parameter `list` (`list`): Optional reusable list with at least five entries; its
        fifth entry must be a writable byte-oriented memoryview backed by at least eight bytes.
    - Parameter `timeout` (`int`): RX wait in FreeRTOS ticks; standard UiFlow2 builds use 1 ms ticks.
    - Returns: `(id, extframe, rtr, 255, data)` or the updated supplied list.
        Returns `None` on timeout or receive failure.

    Raises `TypeError`: On receipt of a frame, the supplied list or memoryview has the wrong type.

    Raises `ValueError`: On receipt of a frame, the list is too short or the memoryview has an invalid format.

```python
can.send(b"\x01\x02", 0x123, timeout=0)
frame = can.recv(0, timeout=0)
if frame is not None:
    identifier, extended, remote, fmi, payload = frame
    print(identifier, payload)
```
### `CANUnit.setfilter(bank, mode, fifo, params, *, rtr=None, extframe=False)`

    Compatibility placeholder: arguments are parsed but filters are not applied.
    The controller accepts all identifiers.

    - Returns: `None`.

### `CANUnit.clearfilter(bank, extframe=False)`

    Compatibility placeholder; it does not change the receive filter.
    `bank` is positional.

    - Returns: `None`.
