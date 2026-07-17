# Chain BUS

Chain BUS is a communication bus module that allows multiple devices to connect and communicate with each other in the M5Chain series devices.

## **API**

#### ChainBUS

## `ChainBus`
Create a Chain bus instance.

- Parameter `id` (`int`): UART ID.
- Parameter `tx` (`int`): TX pin.
- Parameter `rx` (`int`): RX pin.
- Parameter `verbose` (`bool`): Enable verbose mode. Default is False.

```python
from chain import ChainBus

chainbus_0 = ChainBus(2, 32, 33, verbose=True)
```

### `register_device`
Register a Chain device.

- Parameter `device` (`ChainDevice`): Chain device instance.

### `register_event`

### `send`
Send custom command to device.

- Parameter `device_id` (`int`): Device ID.
- Parameter `cmd` (`int`): Command.
- Parameter `payload` (`bytes`): Data.
- Parameter `timeout_ms` (`int`): receive timeout in milliseconds.

- Returns: Response data.
- Return type: bytes

```python
chainbus_0.send(1, 0x20, b"ÿ", 3000)
```

### `get_device_num`
Get connected device number.

- Returns: Number of connected devices.
- Return type: int

```python
num = chainbus_0.get_device_num()
```

### `set_device_connected_handler`
Set new device connection handler callback.

- Parameter `handler` (`function`): Callback function.

### `set_device_disconnected_handler`
Set device disconnection handler callback.

- Parameter `handler` (`function`): Callback function.

### `deinit`
Deinitialize the Chain bus.
