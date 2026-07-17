# EXTIO Unit

Support the following products:

EXTIOUnit

## class EXTIOUnit

## Constructors

### `class EXTIOUnit(i2c, address)`

    Initialize the PCA9554 device.

    - Parameter `i2c` (`I2C`): An instance of the I2C bus to communicate with the device.
    - Parameter `address` (`int`): The I2C address of the PCA9554 device (default is _PCA9554_DEFAULT_ADDRESS).

## Methods

### `EXTIOUnit.set_port_mode(mode) -> None`

    Set the mode of the entire port.

    - Parameter `mode` (`Literal[0x00,0x01]`): The mode to set, either PCA9554.IN (input, 0x00) or PCA9554.OUT (output, 0x01).

### `EXTIOUnit.set_pin_mode(id, mode) -> None`

    Set the mode of a specific pin.

    - Parameter `id` (`int`): The pin number (0-7).
    - Parameter `mode` (`Literal[0x00,0x01]`): The mode to set, either PCA9554.IN (input, 0x00) or PCA9554.OUT (output, 0x01).

### `EXTIOUnit.digit_write_port(value) -> None`

    Set a value to the entire port.

    - Parameter `value` (`int`): An 8-bit value to set to the port.

### `EXTIOUnit.digit_write(id, value) -> None`

    Set a value to a specific pin.

    - Parameter `id` (`int`): The pin number (0-7).
    - Parameter `value` (`int`): The value to set, either 0 (low) or 1 (high).

### `EXTIOUnit.digit_read_port() -> int`

    Read the value from the entire port.

    - Returns: An 8-bit value representing the state of the port.

### `EXTIOUnit.digit_read(id) -> int`

    Read the value from a specific pin.

    - Parameter `id` (`int`): The pin number (0-7).
    - Returns: The value of the pin, either 0 (low) or 1 (high).

### `EXTIOUnit.pin(id, mode, value) -> Pin`

    Provide a MicroPython-style interface for handling GPIO pins.

    - Parameter `id` (`int`): The GPIO pin number to configure and control.
    - Parameter `mode` (`int`): The pin mode, either `Pin.IN` (default) or `Pin.OUT`.
    - Parameter `value`: The initial value to set for the pin if in `OUT` mode. Use `None` for no initial value.
    - Returns: A `Pin` object for further pin operations such as reading or writing values.

## class Pin

## Constructors

### `class Pin(port, id, mode, value)`

    Initialize the Pin object with specified parameters.

    - Parameter `port`: The port object controlling the pin.
    - Parameter `id`: The pin identifier (e.g., GPIO number).
    - Parameter `mode` (`int`): The mode of the pin, either `Pin.IN` (default) or `Pin.OUT`.
    - Parameter `value`: Optional initial value for the pin, 0 or 1.

## Methods

### `Pin.init(mode, value)`

    Reinitialize the pin with a new mode or value.

    - Parameter `mode` (`int`): New mode for the pin, `Pin.IN` (default) or `Pin.OUT`.
    - Parameter `value`: New value for the pin, 0 or 1.

### `Pin.value(args)`

    Get or set the digital value of the pin.

    If no arguments are passed, the method returns the current value of the pin.
    If one argument is passed, it sets the pin to the specified value.

    - Parameter `args`: Optional argument to set the pin value.

### `Pin.on()`

    Set the pin to a high state (1).

### `Pin.off()`

    Set the pin to a low state (0).
