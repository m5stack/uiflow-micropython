.. py:currentmodule:: modbus

ModbusTCPServer
===============

.. include:: ../refs/software.modbus.tcp.server.ref

ModbusTCPServer implements the Modbus TCP server. ModbusTCPServer support function codes 1 (Read Coils), 2 (Read Discrete Inputs), 3 (Read Holding Registers), 4 (Read Input Registers), 5 (Write Single Coil), 6 (Write Single Holding Register), 15 (Write Multiple Coils), and 16 (Write Multiple Holding Registers).

UiFlow2 Example
---------------

CoreS3 TCP Server
^^^^^^^^^^^^^^^^^

Open the |cores3_tcp_server_example.m5f2| project in UiFlow2.

This example demonstrates how to use `ModbusTCPServer` to implement a Modbus TCP server.

UiFlow2 Code Block:

    |cores3_tcp_server_example.png|

Example output:

    None

MicroPython Example
-------------------

CoreS3 TCP Server
^^^^^^^^^^^^^^^^^

This example demonstrates how to use `ModbusTCPServer` to implement a Modbus TCP server.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/software/modbus/cores3_tcp_server_example.py
        :language: python
        :linenos:

Example output:

    None

API
---

ModbusTCPServer
^^^^^^^^^^^^^^^

.. class:: ModbusTCPServer(host: str, port: int=502, verbose: bool=False)

    Create a ModbusTCPServer object.

    :param str host: Hostname or IP address.
    :param int port: Port number.
    :param bool verbose: Verbose mode.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from modbus import ModbusTCPServer
            server = ModbusTCPServer('0.0.0.0', 502)

    .. method:: ModbusTCPServer.start() -> None

        Start the Modbus RTU slave.

        UiFlow2 Code Block:

            |start.png|

        MicroPython Code Block:

            .. code-block:: python

                server.start()

    .. method:: ModbusTCPServer.stop() -> None

        Stop the Modbus RTU slave.

        UiFlow2 Code Block:

            |stop.png|

        MicroPython Code Block:

            .. code-block:: python

                server.stop()

    .. method:: ModbusTCPServer.add_coil(register: int, value: bool) -> None

        Add a coil to the modbus register dictionary.

        :param int register: address of the coils. The address is 0x0000 to 0xFFFF.
        :param int value: Value to add. The value is True or False.

        UiFlow2 Code Block:

            |add_coil.png|

        MicroPython Code Block:

            .. code-block:: python

                server.add_coil(0, False)

    .. method:: ModbusTCPServer.add_discrete_input(register: int, value: bool) -> None

        Add a discrete input to the modbus register dictionary.

        :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.
        :param int value: Value to add. The value is True or False.

        UiFlow2 Code Block:

            |add_discrete_input.png|

        MicroPython Code Block:

            .. code-block:: python

                server.add_discrete_input(0, False)

    .. method:: ModbusTCPServer.add_holding_register(register: int, value: int) -> None

        Add a holding register to the modbus register dictionary.

        :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param int value: Value to add. The value is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

            |add_holding_register.png|

        MicroPython Code Block:

            .. code-block:: python

                server.add_holding_register(0, 0)

    .. method:: ModbusTCPServer.add_input_register(register: int, value: int) -> None

        Add an input register to the modbus register dictionary.

        :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.
        :param int value: Value to add. The value is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

            |add_input_register.png|

        MicroPython Code Block:

            .. code-block:: python

                server.add_input_register(0, 0)

    .. method:: ModbusTCPServer.remove_coil(register: int) -> None

        Remove a coil from the modbus register dictionary.

        :param int register: address of the coils. The address is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

            |remove_coil.png|

        MicroPython Code Block:

            .. code-block:: python

                server.remove_coil(0)

    .. method:: ModbusTCPServer.remove_discrete_input(register: int) -> None

        Remove a discrete input from the modbus register dictionary.

        :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

            |remove_discrete_input.png|

        MicroPython Code Block:

            .. code-block:: python

                server.remove_discrete_input(0)

    .. method:: ModbusTCPServer.remove_holding_register(register: int) -> None

        Remove a holding register from the modbus register dictionary.

        :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

            |remove_holding_register.png|

        MicroPython Code Block:

            .. code-block:: python

                server.remove_holding_register(0)

    .. method:: ModbusTCPServer.remove_input_register(register: int) -> None

        Remove an input register from the modbus register dictionary.

        :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

            |remove_input_register.png|

        MicroPython Code Block:

            .. code-block:: python

                server.remove_input_register(0)

    .. method:: ModbusTCPServer.get_coil(register: int) -> bool

        Get the coil value.

        :param int register: address of the coils. The address is 0x0000 to 0xFFFF.

        :return: The value of the coil.

        UiFlow2 Code Block:

            |get_coil.png|

        MicroPython Code Block:

            .. code-block:: python

                server.get_coil(0)

    .. method:: ModbusTCPServer.get_discrete_input(register: int) -> bool

        Get the discrete input value.

        :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.

        :return: The value of the discrete input.

        UiFlow2 Code Block:

            |get_discrete_input.png|

        MicroPython Code Block:

            .. code-block:: python

                server.get_discrete_input(0)

    .. method:: ModbusTCPServer.get_holding_register(register: int) -> int

        Get the holding register value.

        :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.

        :return: The value of the holding register.

        UiFlow2 Code Block:

            |get_holding_register.png|

        MicroPython Code Block:

            .. code-block:: python

                server.get_holding_register(0)

    .. method:: ModbusTCPServer.get_input_register(register: int) -> int

        Get the input register value.

        :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.

        :return: The value of the input register.

        UiFlow2 Code Block:

            |get_input_register.png|

        MicroPython Code Block:

            .. code-block:: python

                server.get_input_register(0)

    .. method:: ModbusTCPServer.set_coil(register: int, value: bool) -> None

        Set the coil value.

        :param int register: address of the coils. The address is 0x0000 to 0xFFFF.
        :param int value: Value to set. The value is True or False.

        UiFlow2 Code Block:

            |set_coil.png|

        MicroPython Code Block:

            .. code-block:: python

                server.set_coil(0, False)

    .. method:: ModbusTCPServer.set_multi_coils(register: int, value: list) -> None

        Set the multi coils value.

        :param int register: address of the coils. The address is 0x0000 to 0xFFFF.
        :param list value: Values to set. The value is a list of True or False.

        UiFlow2 Code Block:

            |set_multi_coils.png|

        MicroPython Code Block:

            .. code-block:: python

                server.set_multi_coils(0, [False, True])

    .. method:: ModbusTCPServer.set_discrete_input(register: int, value: bool) -> None

        Set the discrete input value.

        :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.
        :param int value: Value to set. The value is True or False.

        UiFlow2 Code Block:

            |set_discrete_input.png|

        MicroPython Code Block:

            .. code-block:: python

                server.set_discrete_input(0, False)

    .. method:: ModbusTCPServer.set_multi_discrete_input(register: int, value: list) -> None

        Set the multi discrete inputs value.

        :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.
        :param list value: Values to set. The value is a list of True or False.

        UiFlow2 Code Block:

            |set_multi_discrete_input.png|

        MicroPython Code Block:

            .. code-block:: python

                server.set_multi_discrete_input(0, [False, True])

    .. method:: ModbusTCPServer.set_holding_register(register: int, value: int) -> None

        Set the holding register value.

        :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param int value: Value to set. The value is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

            |set_holding_register.png|

        MicroPython Code Block:

            .. code-block:: python

                server.set_holding_register(0, 0)

    .. method:: ModbusTCPServer.set_multi_holding_register(register: int, value: list) -> None

        Set the multi holding registers value.

        :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param list value: Values to set. The value is a list of 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

            |set_multi_holding_register.png|

        MicroPython Code Block:

            .. code-block:: python

                server.set_multi_holding_register(0, [0, 1])

    .. method:: ModbusTCPServer.set_input_register(register: int, value: int) -> None

        Set the input register value.

        :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.
        :param int value: Value to set. The value is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

            |set_input_register.png|

        MicroPython Code Block:

            .. code-block:: python

                server.set_input_register(0, 0)

    .. method:: ModbusTCPServer.set_multi_input_register(register: int, value: list) -> None

        Set the multi input registers value.

        :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.
        :param list value: Values to set. The value is a list of 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

            |set_multi_input_register.png|

        MicroPython Code Block:

            .. code-block:: python

                server.set_multi_input_register(0, [0, 1])

    .. method:: ModbusTCPServer.tick() -> None

        Modbus RTU slave tick function. This function should be called in the main loop.

        UiFlow2 Code Block:

            |tick.png|

        MicroPython Code Block:

            .. code-block:: python

                server.tick()

    .. method:: ModbusTCPServer.set_callback(func_code: int, handler) -> None

        Set the callback function for the function code.

        :param int func_code: Function code. The function code is 1 to 6, 15, 16. the symbol is defined in the modbus.ModbusTCPServer (\*_EVENT etc.).
        :param handler: Callback function.

        UiFlow2 Code Block:

            |read_coils_callback.png|

            |read_discrete_inputs_callback.png|

            |read_holding_registers_callback.png|

            |read_input_registers_callback.png|

            |write_multiple_coils_callback.png|

            |write_multiple_registers_callback.png|

            |write_single_coil_callback.png|

            |write_single_register_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def cb(arg):
                    pass
                server.set_callback(1, cb)


    .. data:: ModbusTCPServer.READ_COILS_EVENT

        Function code 1 (Read Coils).


    .. data:: ModbusTCPServer.READ_DISCRETE_INPUTS_EVENT

        Function code 2 (Read Discrete Inputs).


    .. data:: ModbusTCPServer.READ_HOLDING_REGISTERS_EVENT

        Function code 3 (Read Holding Registers).


    .. data:: ModbusTCPServer.READ_INPUT_REGISTERS_EVENT

        Function code 4 (Read Input Registers).


    .. data:: ModbusTCPServer.WRITE_SINGLE_COIL_EVENT

        Function code 5 (Write Single Coil).


    .. data:: ModbusTCPServer.WRITE_SINGLE_HOLDING_REGISTER_EVENT

        Function code 6 (Write Single Holding Register).


    .. data:: ModbusTCPServer.WRITE_MULTIPLE_COILS_EVENT

        Function code 15 (Write Multiple Coils).


    .. data:: ModbusTCPServer.WRITE_MULTIPLE_HOLDING_REGISTERS_EVENT

        Function code 16 (Write Multiple Holding Registers).
