
# CAN

CAN provides the ESP32 classic CAN controller interface. Connect the MCU's
RX/TX pins to a CAN transceiver, then connect its CAN_H/CAN_L lines to the bus.
For CAN Unit examples, see `unit.CANUnit <unit.CANUnit>`.

## API

#### CAN

### `class CAN(id=0, port=None, mode=CAN.NORMAL, prescaler=0, sjw=0, bs1=0, bs2=0, triple_sampling=False, quantum_resolution_hz=0, baudrate=0, verbose=False)`

    Construct and start the CAN controller.

    - Parameter `id` (`int`): Controller ID. The current binding accepts only `0`.
    - Parameter `port` (`tuple`): Required pin selection in `(rx_pin, tx_pin)` order.
        The default `None` does not select pins automatically.
    - Parameter `mode` (`int`): `CAN.NORMAL`, `CAN.NO_ACKNOWLEDGE`, or `CAN.LISTEN_ONLY`.
    - Parameter `prescaler` (`int`): Clock divider for manual timing.
    - Parameter `sjw` (`int`): Resynchronisation jump width in time quanta.
    - Parameter `bs1` (`int`): Time segment before the sample point, in time quanta.
    - Parameter `bs2` (`int`): Time segment after the sample point, in time quanta.
    - Parameter `triple_sampling` (`bool`): Enable triple sampling.
    - Parameter `quantum_resolution_hz` (`int`): Time-quanta clock frequency in Hz.
    - Parameter `baudrate` (`int`): Bitrate in **bits per second**. A nonzero value selects
        automatic timing; otherwise supply valid manual timing parameters.
    - Parameter `verbose` (`bool`): Print the selected configuration.

    Raises `ValueError`: Unsupported controller ID or automatic bitrate.

    Raises `OSError`: Controller initialization fails.

```python
from hardware import CAN

# Choose RX/TX pins for the connected controller and transceiver.
can = CAN(id=0, port=(13, 14), mode=CAN.NORMAL, baudrate=125000)
```
#### Methods

### `CAN.init(mode, tx, rx, quanta_resolution_hz=2500000, brp=0, tseg_1=15, tseg_2=4, sjw=3, triple_sampling=False, baudrate=0)`

    Start a deinitialized controller. Call `deinit()` before using this method
    on an active controller.

    This inherited native method takes separate `tx` and `rx` pins. Its
    `baudrate` is in **kbit/s**; the constructor takes bits per second.
    `quanta_resolution_hz`, `brp`, `tseg_1` and `tseg_2` correspond to
    the constructor's `quantum_resolution_hz`, `prescaler`, `bs1` and `bs2`.

    - Parameter `mode` (`int`): Controller mode.
    - Parameter `tx` (`int`): Transmit GPIO.
    - Parameter `rx` (`int`): Receive GPIO.
    - Parameter `quanta_resolution_hz` (`int`): Time-quanta clock frequency in Hz.
    - Parameter `brp` (`int`): Clock divider; used when `quanta_resolution_hz=0`.
    - Parameter `tseg_1` (`int`): Time quanta before the sample point.
    - Parameter `tseg_2` (`int`): Time quanta after the sample point.
    - Parameter `sjw` (`int`): Resynchronisation jump width in time quanta.
    - Parameter `triple_sampling` (`bool`): Enable triple sampling.
    - Parameter `baudrate` (`int`): Automatic bitrate in kbit/s. Use `0` for manual timing.
    - Returns: `None`.

    Raises `ValueError`: Unsupported automatic bitrate.

    Raises `OSError`: Controller initialization fails.

```python
can.deinit()
can.init(CAN.NORMAL, tx=14, rx=13, baudrate=125)
```
### `CAN.deinit()`

    Stop the controller and release its driver.

    - Returns: `None`.

    Raises `OSError`: Driver removal fails.

### `CAN.restart()`

    Stop and start an enabled controller with its existing configuration.
    A deinitialized controller is left disabled.

    - Returns: `None`.

    Raises `OSError`: The controller cannot be started.

### `CAN.state()`

    - Returns: `CAN.STOPPED` (0), `CAN.BUS_OFF` (4), `CAN.RECOVERING` (5),
        or `CAN.RUNNING` (6). A deinitialized controller returns `CAN.STOPPED`.
    - Return type: int

    Raises `OSError`: Reading the controller status fails.

### `CAN.info([list])`

    Read `[TEC, REC, 0, 0, 0, pending_tx, pending_rx, 0]` while enabled.
    The zero fields are compatibility placeholders. Call this while the controller
    is initialized; status entries are not populated after `deinit()`.

    - Parameter `list` (`list`): Optional list with at least eight entries, updated in place.
    - Returns: The supplied list, or a new eight-element list.

    Raises `TypeError`: The supplied argument is not a list. Omit it to allocate a list.

    Raises `ValueError`: The supplied list has fewer than eight entries.

    Raises `OSError`: Reading the controller status fails.

### `CAN.any(fifo)`

    - Parameter `fifo` (`int`): Compatibility argument; use `0`. The controller has one RX queue.
    - Returns: `True` if a frame is waiting, otherwise `False`.
        A deinitialized controller returns `False`.

    Raises `OSError`: Reading the controller status fails.

### `CAN.send(data, id, *, timeout=0, rtr=False, extframe=False)`

    Queue a CAN frame. Success means the frame was queued for transmission;
    it does not confirm receipt by another node.

    - Parameter `data`: A readable buffer such as `bytes` or `bytearray`, up to eight bytes.
        To send a single byte, use `bytes([value])`.
    - Parameter `id` (`int`): Standard 11-bit identifier, or extended 29-bit identifier
        when `extframe=True`.
    - Parameter `timeout` (`int`): Maximum wait for space in the TX queue. The binding passes
        FreeRTOS ticks; standard UiFlow2 builds use a 1 ms tick. `0` does not wait.
    - Parameter `rtr` (`bool`): Send a remote request; only the buffer length supplies the DLC.
    - Parameter `extframe` (`bool`): Use an extended identifier.
    - Returns: `None`.

    Raises `TypeError`: `data` does not support the buffer protocol.

    Raises `ValueError`: The buffer is longer than eight bytes.

    Raises `OSError`: The driver rejects an argument, or queueing fails or times out.

```python
can.send(b"\x01\x02", 0x123, timeout=0)
```
### `CAN.recv(fifo, list=None, *, timeout=5000)`

    - Parameter `fifo` (`int`): Compatibility argument; use `0`.
    - Parameter `list` (`list`): Optional list with at least five entries. Its fifth entry
        must be a writable byte-oriented `memoryview` backed by at least eight bytes.
    - Parameter `timeout` (`int`): Maximum wait for a frame, in FreeRTOS ticks
        (1 ms per tick in standard UiFlow2 builds). `0` does not wait.
    - Returns: `(id, extframe, rtr, 255, data)` with `data` as `bytes`,
        or the supplied list updated in place. Returns `None` on timeout or
        receive failure. The fourth field is a fixed compatibility value.

    Raises `TypeError`: On receipt of a frame, `list` is not a list or its
        fifth entry is not a memoryview.

    Raises `ValueError`: On receipt of a frame, the list is too short or its
        memoryview is not writable and byte-oriented.

```python
frame = can.recv(0, timeout=0)
if frame is not None:
    identifier, extended, remote, fmi, payload = frame
    print(identifier, payload)

buffer = bytearray(8)
frame_buffer = [0, False, False, 0, memoryview(buffer)]
frame = can.recv(0, frame_buffer, timeout=0)
```
### `CAN.setfilter(bank, mode, fifo, params, *, rtr=None, extframe=False)`

    Compatibility placeholder. The arguments are parsed, but reception filters
    are not applied. The controller accepts all identifiers.

    - Returns: `None`.

### `CAN.clearfilter(bank, extframe=False)`

    Compatibility placeholder. `bank` is positional. This method does not
    change the receive filter.

    - Returns: `None`.

#### Constants

### `CAN.NORMAL`
          CAN.NO_ACKNOWLEDGE
          CAN.LISTEN_ONLY

    Controller modes accepted by the constructor and `init()`.

### `CAN.STOPPED`
          CAN.BUS_OFF
          CAN.RECOVERING
          CAN.RUNNING

    Controller states returned by `state()`.

### `CAN.MASK16`
          CAN.LIST16
          CAN.MASK32
          CAN.LIST32

    Compatibility filter constants. Filter programming is not implemented.
