EXTIOUnit
=========
.. sku:U011
.. include:: ../refs/unit.extio.ref

Support the following products:

|EXTIOUnit|

.. Micropython Example:
    
..     .. literalinclude:: ../../../examples/unit/extio/extio_core2_example.py
..         :language: python
..         :linenos:

.. UIFLOW2 Example:

..     |example.png|

.. .. only:: builder_html

..     |extio_core2_example.m5f2|

class EXTIOUnit
---------------

Constructors
------------

.. class:: EXTIOUnit(i2c, address)

    Initialize the PCA9554 device.

    :param I2C i2c: An instance of the I2C bus to communicate with the device.
    :param int address: The I2C address of the PCA9554 device (default is _PCA9554_DEFAULT_ADDRESS).

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: EXTIOUnit.set_port_mode(mode) -> None

    Set the mode of the entire port.

    :param Literal[0x00,0x01] mode: The mode to set, either PCA9554.IN (input, 0x00) or PCA9554.OUT (output, 0x01).

    UIFLOW2:

        |set_port_mode.png|

.. method:: EXTIOUnit.set_pin_mode(id, mode) -> None

    Set the mode of a specific pin.

    :param int id: The pin number (0-7).
    :param Literal[0x00,0x01] mode: The mode to set, either PCA9554.IN (input, 0x00) or PCA9554.OUT (output, 0x01).

    UIFLOW2:

        |set_pin_mode.png|

.. method:: EXTIOUnit.digit_write_port(value) -> None

    Set a value to the entire port.

    :param int value: An 8-bit value to set to the port.

    UIFLOW2:

        |digit_write_port.png|

.. method:: EXTIOUnit.digit_write(id, value) -> None

    Set a value to a specific pin.

    :param int id: The pin number (0-7).
    :param int value: The value to set, either 0 (low) or 1 (high).

    UIFLOW2:

        |digit_write.png|

.. method:: EXTIOUnit.digit_read_port() -> int

    Read the value from the entire port.

    :return: An 8-bit value representing the state of the port.

    UIFLOW2:

        |digit_read_port.png|

.. method:: EXTIOUnit.digit_read(id) -> int

    Read the value from a specific pin.

    :param int id: The pin number (0-7).
    :return: The value of the pin, either 0 (low) or 1 (high).

    UIFLOW2:

        |digit_read.png|

.. method:: EXTIOUnit.pin(id, mode, value) -> Pin
    
    Provide a MicroPython-style interface for handling GPIO pins.

    :param int id: The GPIO pin number to configure and control.
    :param int mode: The pin mode, either `Pin.IN` (default) or `Pin.OUT`.
    :param value: The initial value to set for the pin if in `OUT` mode. Use `None` for no initial value.
    :return: A `Pin` object for further pin operations such as reading or writing values.

class Pin
---------

Constructors
------------

.. class:: Pin(port, id, mode, value)
    :no-index:

    Initialize the Pin object with specified parameters.

    :param port: The port object controlling the pin.
    :param id: The pin identifier (e.g., GPIO number).
    :param int mode: The mode of the pin, either `Pin.IN` (default) or `Pin.OUT`.
    :param value: Optional initial value for the pin, 0 or 1.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: Pin.init(mode, value)

    Reinitialize the pin with a new mode or value.

    :param int mode: New mode for the pin, `Pin.IN` (default) or `Pin.OUT`.
    :param value: New value for the pin, 0 or 1.

.. method:: Pin.value(args)
    :no-index:

    Get or set the digital value of the pin.

    If no arguments are passed, the method returns the current value of the pin.  
    If one argument is passed, it sets the pin to the specified value.

    :param args: Optional argument to set the pin value.

.. method:: Pin.on()
    :no-index:

    Set the pin to a high state (1).

.. method:: Pin.off()
    :no-index:

    Set the pin to a low state (0).
