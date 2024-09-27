.. py:currentmodule:: modbus

class ModbusTCPClient -- Modbus TCP client
==========================================

.. include:: ../refs/software.modbus.tcp.client.ref


ModbusTCPClient implements the Modbus TCP client. ModbusTCPClient support function codes 1 (Read Coils), 2 (Read Discrete Inputs), 3 (Read Holding Registers), 4 (Read Input Registers), 5 (Write Single Coil), 6 (Write Single Holding Register), 15 (Write Multiple Coils), and 16 (Write Multiple Holding Registers).


Micropython Example:

    .. literalinclude:: ../../../examples/softwave/modbus/cores3_tcp_client_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_tcp_client_example.m5f2|


Constructors
------------

.. py:class:: modbus.ModbusTCPClient(host: str, port: int=502, verbose: bool=False)

    Create a ModbusTCPClient object.

    :param str host: Hostname or IP address.
    :param int port: Port number.
    :param bool verbose: Verbose mode.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ModbusTCPClient.connect() -> None

    Connect to the Modbus server.

    UIFLOW2:

        |connect.png|


.. method:: ModbusTCPClient.disconnect() -> None

    Disconnect from the Modbus server.

    UIFLOW2:

        |disconnect.png|


.. method:: ModbusTCPClient.read_coils(address, register, quantity, timeout: int=2000) -> list

    Read coils.

    :param int address: Slave address. The address is 0 to 247.
    :param int register: Start address of the coils. The address is 0x0000 to 0xFFFF.
    :param int quantity: Quantity of registers to read.
    :param int timeout: Timeout in milliseconds.

    :return: A list of coils. The item of the list is True or False.

    UIFLOW2:

        |read_coils.png|


.. method:: ModbusTCPClient.read_discrete_inputs(address, register, quantity, timeout: int=2000) -> list

    Read discrete inputs.

    :param int address: Slave address. The address is 0 to 247.
    :param int register: Start address of the discrete inputs. The address is 0x0000 to 0xFFFF.
    :param int quantity: Quantity of registers to read.
    :param int timeout: Timeout in milliseconds.

    :return: A list of discrete inputs. The item of the list is True or False.

    UIFLOW2:

        |read_discrete_inputs.png|


.. method:: ModbusTCPClient.read_holding_registers(address, register, quantity, timeout: int=2000) -> list

    Read holding registers.

    :param int address: Slave address. The address is 0 to 247.
    :param int register: Start address of the holding registers. The address is 0x0000 to 0xFFFF.
    :param int quantity: Quantity of registers to read.
    :param int timeout: Timeout in milliseconds.

    :return: A list of holding registers. The item of the list is 0x0000 to 0xFFFF.

    UIFLOW2:

        |read_holding_registers.png|


.. method:: ModbusTCPClient.read_input_registers(address, register, quantity, timeout: int=2000) -> list

    Read input registers.

    :param int address: Slave address. The address is 0 to 247.
    :param int register: Start address of the input registers. The address is 0x0000 to 0xFFFF.
    :param int quantity: Quantity of registers to read.
    :param int timeout: Timeout in milliseconds.

    :return: A list of input registers. The item of the list is 0x0000 to 0xFFFF.

    UIFLOW2:

        |read_input_registers.png|


.. method:: ModbusTCPClient.write_single_coil(address, register, value, timeout: int=2000) -> bool

    Write a single coil.

    :param int address: Slave address. The address is 0 to 247.
    :param int register: Start address of the coils. The address is 0x0000 to 0xFFFF.
    :param int value: Value to write. The value is True or False.
    :param int timeout: Timeout in milliseconds.

    :return: The value of the coil.

    UIFLOW2:

        |write_single_coil.png|


.. method:: ModbusTCPClient.write_single_register(address, register, value, timeout: int=2000) -> int

    Write a single register.

    :param int address: Slave address. The address is 0 to 247.
    :param int register: Start address of the holding registers. The address is 0x0000 to 0xFFFF.
    :param int value: Value to write. The value is 0x0000 to 0xFFFF.
    :param int timeout: Timeout in milliseconds.

    :return: the written value

    UIFLOW2:

        |write_single_register.png|


.. method:: ModbusTCPClient.write_multiple_coils(address, register, values, timeout: int=2000) -> int

    Write multiple coils.

    :param int address: Slave address. The address is 0 to 247.
    :param int register: Start address of the coils. The address is 0x0000 to 0xFFFF.
    :param list values: Values to write. The item of the list is True or False.
    :param int timeout: Timeout in milliseconds.

    :return: the written count.

    UIFLOW2:

        |write_multiple_coils.png|


.. method:: ModbusTCPClient.write_multiple_registers(address: int, register: int, values: list, timeout: int=2000) -> int

    Write multiple registers.

    :param int address: Slave address. The address is 0 to 247.
    :param int register: Start address of the holding registers. The address is 0x0000 to 0xFFFF.
    :param list values: Values to write. The item of the list is 0x0000 to 0xFFFF.
    :param int timeout: Timeout in milliseconds.

    :return: the written count.

    UIFLOW2:

        |write_multiple_registers.png|
