.. py:currentmodule:: modbus

class ModbusRTUSlave -- Modbus RTU slave
==========================================

.. include:: ../refs/software.modbus.rtu.slave.ref

ModbusRTUSlave implements the Modbus RTU slave. ModbusRTUSlave support function codes 1 (Read Coils), 2 (Read Discrete Inputs), 3 (Read Holding Registers), 4 (Read Input Registers), 5 (Write Single Coil), 6 (Write Single Holding Register), 15 (Write Multiple Coils), and 16 (Write Multiple Holding Registers).


Micropython Example:

    .. literalinclude:: ../../../examples/softwave/modbus/cores3_rtu_slave_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_rtu_slave_example.m5f2|

Constructors
------------

.. py:class:: modbus.ModbusRTUSlave(uart, device_address: int=1, context=None, ignore_unit_id: bool=False, verbose: bool=False)

    Create a ModbusRTUSlave object.

    :param UART uart: UART object or RS485 object.
    :param int device_address: Device address. The address is 0 to 247.
    :param dict context: Modbus server context.
    :param bool ignore_unit_id: Ignore unit ID(or Device address).
    :param bool verbose: Verbose mode.

    ``context`` is a dictionary that contains the Modbus server context. the format is as follows::

        {
            "discrete_inputs": [
                {
                    "register": 0,  # Start address of the discrete inputs.
                    "value": [False, True, False, True]  # Values of the discrete inputs. quantity is the length of the list.
                }
            ],
            "coils": [
                {
                    "register": 0,  # Start address of the coils.
                    "value": [False, True, False, True]  # Values of the coils. quantity is the length of the list. quantity is the length of the list.
                }
            ],
            "input_registers": [
                {
                    "register": 0,  # Start address of the input registers.
                    "value": [0x0000, 0x0001, 0x0002, 0x0003]  # Values of the input registers. quantity is the length of the list. quantity is the length of the list.
                }
            ],
            "holding_registers": [
                {
                    "register": 0,  # Start address of the holding registers.
                    "value": [0x0000, 0x0001, 0x0002, 0x0003]  # Values of the holding registers. quantity is the length of the list. quantity is the length of the list.
                }
            ],
        }

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ModbusRTUSlave.start() -> None

    Start the Modbus RTU slave.

    UIFLOW2:

        |start.png|


.. method:: ModbusRTUSlave.stop() -> None

    Stop the Modbus RTU slave.

    UIFLOW2:

        |stop.png|


.. method:: ModbusRTUSlave.add_coil(register: int, value: bool) -> None

    Add a coil to the modbus register dictionary.

    :param int register: address of the coils. The address is 0x0000 to 0xFFFF.
    :param int value: Value to add. The value is True or False.

    UIFLOW2:

        |add_coil.png|


.. method:: ModbusRTUSlave.add_discrete_input(register: int, value: bool) -> None

    Add a discrete input to the modbus register dictionary.

    :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.
    :param int value: Value to add. The value is True or False.

    UIFLOW2:

        |add_discrete_input.png|


.. method:: ModbusRTUSlave.add_holding_register(register: int, value: int) -> None

    Add a holding register to the modbus register dictionary.

    :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.
    :param int value: Value to add. The value is 0x0000 to 0xFFFF.

    UIFLOW2:

        |add_holding_register.png|


.. method:: ModbusRTUSlave.add_input_register(register: int, value: int) -> None

    Add an input register to the modbus register dictionary.

    :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.
    :param int value: Value to add. The value is 0x0000 to 0xFFFF.

    UIFLOW2:

        |add_input_register.png|


.. method:: ModbusRTUSlave.remove_coil(register: int) -> None

    Remove a coil from the modbus register dictionary.

    :param int register: address of the coils. The address is 0x0000 to 0xFFFF.

    UIFLOW2:

        |remove_coil.png|


.. method:: ModbusRTUSlave.remove_discrete_input(register: int) -> None

    Remove a discrete input from the modbus register dictionary.

    :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.

    UIFLOW2:

        |remove_discrete_input.png|


.. method:: ModbusRTUSlave.remove_holding_register(register: int) -> None

    Remove a holding register from the modbus register dictionary.

    :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.

    UIFLOW2:

        |remove_holding_register.png|


.. method:: ModbusRTUSlave.remove_input_register(register: int) -> None

    Remove an input register from the modbus register dictionary.

    :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.

    UIFLOW2:

        |remove_input_register.png|


.. method:: ModbusRTUSlave.get_coil(register: int) -> bool

    Get the coil value.

    :param int register: address of the coils. The address is 0x0000 to 0xFFFF.

    :return: The value of the coil.

    UIFLOW2:

        |get_coil.png|


.. method:: ModbusRTUSlave.get_discrete_input(register: int) -> bool

    Get the discrete input value.

    :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.

    :return: The value of the discrete input.

    UIFLOW2:

        |get_discrete_input.png|


.. method:: ModbusRTUSlave.get_holding_register(register: int) -> int

    Get the holding register value.

    :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.

    :return: The value of the holding register.

    UIFLOW2:

        |get_holding_register.png|


.. method:: ModbusRTUSlave.get_input_register(register: int) -> int

    Get the input register value.

    :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.

    :return: The value of the input register.

    UIFLOW2:

        |get_input_register.png|


.. method:: ModbusRTUSlave.set_coil(register: int, value: bool) -> None

    Set the coil value.

    :param int register: address of the coils. The address is 0x0000 to 0xFFFF.
    :param int value: Value to set. The value is True or False.

    UIFLOW2:

        |set_coil.png|


.. method:: ModbusRTUSlave.set_multi_coils(register: int, value: list) -> None

    Set the multi coils value.

    :param int register: address of the coils. The address is 0x0000 to 0xFFFF.
    :param list value: Values to set. The value is a list of True or False.

    UIFLOW2:

        |set_multi_coils.png|


.. method:: ModbusRTUSlave.set_discrete_input(register: int, value: bool) -> None

    Set the discrete input value.

    :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.
    :param int value: Value to set. The value is True or False.

    UIFLOW2:

        |set_discrete_input.png|


.. method:: ModbusRTUSlave.set_multi_discrete_input(register: int, value: list) -> None

    Set the multi discrete inputs value.

    :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.
    :param list value: Values to set. The value is a list of True or False.

    UIFLOW2:

        |set_multi_discrete_input.png|


.. method:: ModbusRTUSlave.set_holding_register(register: int, value: int) -> None

    Set the holding register value.

    :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.
    :param int value: Value to set. The value is 0x0000 to 0xFFFF.

    UIFLOW2:

        |set_holding_register.png|


.. method:: ModbusRTUSlave.set_multi_holding_register(register: int, value: list) -> None

    Set the multi holding registers value.

    :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.
    :param list value: Values to set. The value is a list of 0x0000 to 0xFFFF.

    UIFLOW2:

        |set_multi_holding_register.png|


.. method:: ModbusRTUSlave.set_input_register(register: int, value: int) -> None

    Set the input register value.

    :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.
    :param int value: Value to set. The value is 0x0000 to 0xFFFF.

    UIFLOW2:

        |set_input_register.png|


.. method:: ModbusRTUSlave.set_multi_input_register(register: int, value: list) -> None

    Set the multi input registers value.

    :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.
    :param list value: Values to set. The value is a list of 0x0000 to 0xFFFF.

    UIFLOW2:

        |set_multi_input_register.png|


.. method:: ModbusRTUSlave.tick() -> None

    Modbus RTU slave tick function. This function should be called in the main loop.

    UIFLOW2:

        |tick.png|


.. method:: ModbusRTUSlave.set_callback(func_code: int, handler) -> None

    Set the callback function for the function code.

    :param int func_code: Function code. The function code is 1 to 6, 15, 16. the symbol is defined in the modbus.ModbusRTUSlave (\*_EVENT etc.).
    :param handler: Callback function.

    UIFLOW2:

        |read_coils_callback.png|

        |read_discrete_inputs_callback.png|

        |read_holding_registers_callback.png|

        |read_input_registers_callback.png|

        |write_multiple_coils_callback.png|

        |write_multiple_registers_callback.png|

        |write_single_coil_callback.png|

        |write_single_register_callback.png|


Constants
---------

.. data:: ModbusRTUSlave.READ_COILS_EVENT

    Function code 1 (Read Coils).


.. data:: ModbusRTUSlave.READ_DISCRETE_INPUTS_EVENT

    Function code 2 (Read Discrete Inputs).


.. data:: ModbusRTUSlave.READ_HOLDING_REGISTERS_EVENT

    Function code 3 (Read Holding Registers).


.. data:: ModbusRTUSlave.READ_INPUT_REGISTERS_EVENT

    Function code 4 (Read Input Registers).


.. data:: ModbusRTUSlave.WRITE_SINGLE_COIL_EVENT

    Function code 5 (Write Single Coil).


.. data:: ModbusRTUSlave.WRITE_SINGLE_HOLDING_REGISTER_EVENT

    Function code 6 (Write Single Holding Register).


.. data:: ModbusRTUSlave.WRITE_MULTIPLE_COILS_EVENT

    Function code 15 (Write Multiple Coils).


.. data:: ModbusRTUSlave.WRITE_MULTIPLE_HOLDING_REGISTERS_EVENT

    Function code 16 (Write Multiple Holding Registers).
