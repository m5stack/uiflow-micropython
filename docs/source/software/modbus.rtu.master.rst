.. py:currentmodule:: modbus

ModbusRTUMaster
===============

.. include:: ../refs/software.modbus.rtu.master.ref

ModbusRTUMaster implements the Modbus RTU master. ModbusRTUMaster support function codes 1 (Read Coils), 2 (Read Discrete Inputs), 3 (Read Holding Registers), 4 (Read Input Registers), 5 (Write Single Coil), 6 (Write Single Holding Register), 15 (Write Multiple Coils), and 16 (Write Multiple Holding Registers).

UiFlow2 Example
---------------

CoreS3 RTU Master
^^^^^^^^^^^^^^^^^

Open the |cores3_rtu_master_example.m5f2| project in UiFlow2.

This example demonstrates how to use the ``ModbusRTUMaster`` class.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

CoreS3 RTU Master
^^^^^^^^^^^^^^^^^

This example demonstrates how to use the ``ModbusRTUMaster`` class.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/software/modbus/cores3_rtu_master_example.py
        :language: python
        :linenos:

Example output:

    None

API
---

ModbusRTUMaster
^^^^^^^^^^^^^^^

.. class:: ModbusRTUMaster(uart: UART, verbose: bool = False)

    Create a ModbusRTUMaster object.

    :param UART uart: UART object or RS485 object.
    :param bool verbose: Verbose mode.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from modbus import ModbusRTUMaster
            # For CoreS3
            # master = ModbusRTUMaster(uart)


    .. py:method:: ModbusRTUMaster.read_coils(address: int, register: int, quantity: int, timeout: int = 2000)

        Read coils.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the coils. The address is 0x0000 to 0xFFFF.
        :param int quantity: Quantity of registers to read.
        :param int timeout: Timeout in milliseconds.
        :returns: list - A list of coils. The item of the list is True or False.

        UiFlow2 Code Block:

            |read_coils.png|

        MicroPython Code Block:

            .. code-block:: python

                master.read_coils(1, 0, 10)


    .. py:method:: ModbusRTUMaster.read_discrete_inputs(address: int, register: int, quantity: int, timeout: int = 2000)

        Read discrete inputs.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the discrete inputs. The address is 0x0000 to 0xFFFF.
        :param int quantity: Quantity of registers to read.
        :param int timeout: Timeout in milliseconds.
        :returns: list - A list of discrete inputs. The item of the list is True or False.

        UiFlow2 Code Block:

            |read_discrete_inputs.png|

        MicroPython Code Block:

            .. code-block:: python

                master.read_discrete_inputs(1, 0, 10)


    .. py:method:: ModbusRTUMaster.read_holding_registers(address: int, register: int, quantity: int, timeout: int = 2000)

        Read holding registers.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param int quantity: Quantity of registers to read.
        :param int timeout: Timeout in milliseconds.
        :returns: list - A list of holding registers. The item of the list is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

            |read_holding_registers.png|

        MicroPython Code Block:

            .. code-block:: python

                master.read_holding_registers(1, 0, 10)


    .. py:method:: ModbusRTUMaster.read_input_registers(address: int, register: int, quantity: int, timeout: int = 2000)

        Read input registers.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the input registers. The address is 0x0000 to 0xFFFF.
        :param int quantity: Quantity of registers to read.
        :param int timeout: Timeout in milliseconds.
        :returns: list - A list of input registers. The item of the list is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

            |read_input_registers.png|

        MicroPython Code Block:

            .. code-block:: python

                master.read_input_registers(1, 0, 10)


    .. py:method:: ModbusRTUMaster.write_single_coil(address: int, register: int, value: int, timeout: int = 2000)

        Write a single coil.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the coils. The address is 0x0000 to 0xFFFF.
        :param int value: Value to write. The value is True or False.
        :param int timeout: Timeout in milliseconds.
        :returns: bool - The value of the coil.

        UiFlow2 Code Block:

            |write_single_coil.png|

        MicroPython Code Block:

            .. code-block:: python

                master.write_single_coil(1, 0, True)


    .. py:method:: ModbusRTUMaster.write_single_register(address: int, register: int, value: int, timeout: int = 2000)

        Write a single register.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param int value: Value to write. The value is 0x0000 to 0xFFFF.
        :param int timeout: Timeout in milliseconds.
        :returns: int - the written value

        UiFlow2 Code Block:

            |write_single_register.png|

        MicroPython Code Block:

            .. code-block:: python

                master.write_single_register(1, 0, 100)


    .. py:method:: ModbusRTUMaster.write_multiple_coils(address: int, register: int, values: list, timeout: int = 2000)

        Write multiple coils.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the coils. The address is 0x0000 to 0xFFFF.
        :param list values: Values to write. The item of the list is True or False.
        :param int timeout: Timeout in milliseconds.
        :returns: int - the written count.

        UiFlow2 Code Block:

            |write_multiple_coils.png|

        MicroPython Code Block:

            .. code-block:: python

                master.write_multiple_coils(1, 0, [True, False, True])


    .. py:method:: ModbusRTUMaster.write_multiple_registers(address: int, register: int, values: list, timeout: int = 2000)

        Write multiple registers.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param list values: Values to write. The item of the list is 0x0000 to 0xFFFF.
        :param int timeout: Timeout in milliseconds.
        :returns: int - the written count.

        UiFlow2 Code Block:

            |write_multiple_registers.png|

        MicroPython Code Block:

            .. code-block:: python

                master.write_multiple_registers(1, 0, [100, 200, 300])
