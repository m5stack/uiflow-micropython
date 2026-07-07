# Chain BUS

<!-- .. include:: ../refs/chain.bus.ref -->

Chain BUS is a communication bus module that allows multiple devices to connect and communicate with each other in the M5Chain series devices.

## **API**

#### ChainBUS

## ChainBus
Create a Chain bus instance.

:param int id: UART ID.
:param int tx: TX pin.
:param int rx: RX pin.
:param bool verbose: Enable verbose mode. Default is False.

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        from chain import ChainBus

        chainbus_0 = ChainBus(2, 32, 33, verbose=True)

### `register_device`
Register a Chain device.

:param ChainDevice device: Chain device instance.

### `register_event`

### `send`
Send custom command to device.

:param int device_id: Device ID.
:param int cmd: Command.
:param bytes payload: Data.
:param int timeout_ms: receive timeout in milliseconds.

:return: Response data.
:rtype: bytes

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        chainbus_0.send(1, 0x20, b"ÿ", 3000)

### `get_device_num`
Get connected device number.

:return: Number of connected devices.
:rtype: int

UiFlow2 Code Block:

MicroPython Code Block:

    .. code-block:: python

        num = chainbus_0.get_device_num()

### `set_device_connected_handler`
Set new device connection handler callback.

:param function handler: Callback function.

### `set_device_disconnected_handler`
Set device disconnection handler callback.

:param function handler: Callback function.

### `deinit`
Deinitialize the Chain bus.
