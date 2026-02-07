.. py:currentmodule:: modbus

ModbusTCPClient
===============

.. include:: ../refs/software.modbus.tcp.client.ref

ModbusTCPClient implements the Modbus TCP client. ModbusTCPClient support function codes 1 (Read Coils), 2 (Read Discrete Inputs), 3 (Read Holding Registers), 4 (Read Input Registers), 5 (Write Single Coil), 6 (Write Single Holding Register), 15 (Write Multiple Coils), and 16 (Write Multiple Holding Registers).

UiFlow2 Example
---------------

CoreS3 TCP Client
^^^^^^^^^^^^^^^^^

Open the |cores3_tcp_client_example.m5f2| project in UiFlow2.

This example demonstrates how to use `ModbusTCPClient` to implement a Modbus TCP client.

UiFlow2 Code Block:

    |cores3_tcp_client_example.png|

Example output:

    None

MicroPython Example
-------------------

CoreS3 TCP Client
^^^^^^^^^^^^^^^^^

This example demonstrates how to use `ModbusTCPClient` to implement a Modbus TCP client.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/software/modbus/cores3_tcp_client_example.py
        :language: python
        :linenos:

Example output:

    None

API
---

ModbusTCPClient
^^^^^^^^^^^^^^^

.. class:: ModbusTCPClient(host: str, port: int=502, verbose: bool=False)

    Create a ModbusTCPClient object.

    :param str host: Hostname or IP address.
    :param int port: Port number.
    :param bool verbose: Verbose mode.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from modbus import ModbusTCPClient
            client = ModbusTCPClient('192.168.1.100', 502)

    .. py:method:: ModbusTCPClient.connect() -> None

        Connect to the Modbus server.

        UiFlow2 Code Block:

            |connect.png|

        MicroPython Code Block:

            .. code-block:: python

                client.connect()

    .. py:method:: ModbusTCPClient.disconnect() -> None

        Disconnect from the Modbus server.

        UiFlow2 Code Block:

            |disconnect.png|

        MicroPython Code Block:

            .. code-block:: python

                client.disconnect()

    .. py:method:: ModbusTCPClient.read_coils(address, register, quantity, timeout: int=2000) -> list

        Read coils.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the coils. The address is 0x0000 to 0xFFFF.
        :param int quantity: Quantity of registers to read.
        :param int timeout: Timeout in milliseconds.

        :return: A list of coils. The item of the list is True or False.

        UiFlow2 Code Block:

            |read_coils.png|

        MicroPython Code Block:

            .. code-block:: python

                client.read_coils(1, 0, 10)

    .. py:method:: ModbusTCPClient.read_discrete_inputs(address, register, quantity, timeout: int=2000) -> list

        Read discrete inputs.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the discrete inputs. The address is 0x0000 to 0xFFFF.
        :param int quantity: Quantity of registers to read.
        :param int timeout: Timeout in milliseconds.

        :return: A list of discrete inputs. The item of the list is True or False.

        UiFlow2 Code Block:

            |read_discrete_inputs.png|

        MicroPython Code Block:

            .. code-block:: python

                client.read_discrete_inputs(1, 0, 10)

    .. py:method:: ModbusTCPClient.read_holding_registers(address, register, quantity, timeout: int=2000) -> list

        Read holding registers.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param int quantity: Quantity of registers to read.
        :param int timeout: Timeout in milliseconds.

        :return: A list of holding registers. The item of the list is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

            |read_holding_registers.png|

        MicroPython Code Block:

            .. code-block:: python

                client.read_holding_registers(1, 0, 10)

    .. py:method:: ModbusTCPClient.read_input_registers(address, register, quantity, timeout: int=2000) -> list

        Read input registers.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the input registers. The address is 0x0000 to 0xFFFF.
        :param int quantity: Quantity of registers to read.
        :param int timeout: Timeout in milliseconds.

        :return: A list of input registers. The item of the list is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

            |read_input_registers.png|

        MicroPython Code Block:

            .. code-block:: python

                client.read_input_registers(1, 0, 10)

    .. py:method:: ModbusTCPClient.write_single_coil(address, register, value, timeout: int=2000) -> bool

        Write a single coil.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the coils. The address is 0x0000 to 0xFFFF.
        :param int value: Value to write. The value is True or False.
        :param int timeout: Timeout in milliseconds.

        :return: The value of the coil.

        UiFlow2 Code Block:

            |write_single_coil.png|

        MicroPython Code Block:

            .. code-block:: python

                client.write_single_coil(1, 0, True)

    .. py:method:: ModbusTCPClient.write_single_register(address, register, value, timeout: int=2000) -> int

        Write a single register.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param int value: Value to write. The value is 0x0000 to 0xFFFF.
        :param int timeout: Timeout in milliseconds.

        :return: the written value

        UiFlow2 Code Block:

            |write_single_register.png|

        MicroPython Code Block:

            .. code-block:: python

                client.write_single_register(1, 0, 100)

    .. py:method:: ModbusTCPClient.write_multiple_coils(address, register, values, timeout: int=2000) -> int

        Write multiple coils.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the coils. The address is 0x0000 to 0xFFFF.
        :param list values: Values to write. The item of the list is True or False.
        :param int timeout: Timeout in milliseconds.

        :return: the written count.

        UiFlow2 Code Block:

            |write_multiple_coils.png|

        MicroPython Code Block:

            .. code-block:: python

                client.write_multiple_coils(1, 0, [True, False, True])

    .. py:method:: ModbusTCPClient.write_multiple_registers(address: int, register: int, values: list, timeout: int=2000) -> int

        Write multiple registers.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param list values: Values to write. The item of the list is 0x0000 to 0xFFFF.
        :param int timeout: Timeout in milliseconds.

        :return: the written count.

        UiFlow2 Code Block:

            |write_multiple_registers.png|

        MicroPython Code Block:

            .. code-block:: python

                client.write_multiple_registers(1, 0, [100, 200, 300])
