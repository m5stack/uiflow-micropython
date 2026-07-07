<!-- .. py:currentmodule:: modbus -->

# ModbusRTUSlave

<!-- .. include:: ../refs/software.modbus.rtu.slave.ref -->

ModbusRTUSlave implements the Modbus RTU slave. ModbusRTUSlave support function codes 1 (Read Coils), 2 (Read Discrete Inputs), 3 (Read Holding Registers), 4 (Read Input Registers), 5 (Write Single Coil), 6 (Write Single Holding Register), 15 (Write Multiple Coils), and 16 (Write Multiple Holding Registers).

## UiFlow2 Example

#### CoreS3 RTU Slave

Open the |cores3_rtu_slave_example.m5f2| project in UiFlow2.

This example demonstrates how to use the ``ModbusRTUSlave`` class.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### CoreS3 RTU Slave

This example demonstrates how to use the ``ModbusRTUSlave`` class.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import modbus
from unit import ISO485Unit

label0 = None
label1 = None
label2 = None
modbusrtuslave_0 = None
iso485_0 = None

starting_register1 = None
slave_list1 = None
register1 = None
slave_value1 = None
starting_register4 = None
slave_list4 = None
register2 = None
slave_value2 = None
starting_register2 = None
slave_list2 = None
starting_register6 = None
slave_list6 = None
starting_register5 = None
slave_list5 = None
starting_register3 = None
slave_list3 = None

def modbus_read_coils_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, starting_register1, slave_list1 = args
    label0.setText(str("read coils"))
    label1.setText(str(starting_register1))
    label2.setText(str(slave_list1))

def modbus_write_single_coil_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, register1, slave_value1 = args
    label0.setText(str("write single coil"))
    label1.setText(str(register1))
    label2.setText(str(slave_value1))

def modbus_read_input_registers_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, starting_register4, slave_list4 = args
    label0.setText(str("read input register"))
    label1.setText(str(starting_register4))
    label2.setText(str(slave_list4))

def modbus_write_single_registers_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, register2, slave_value2 = args
    label0.setText(str("write single registers"))
    label1.setText(str(register2))
    label2.setText(str(slave_value2))

def modbus_read_discrete_inputs_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, starting_register2, slave_list2 = args
    label0.setText(str("read  discrete input"))
    label1.setText(str(starting_register2))
    label2.setText(str(slave_list2))

def modbus_write_multiple_registers_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, starting_register6, slave_list6 = args
    label0.setText(str("write multiple registers"))
    label1.setText(str(slave_list6))
    label2.setText(str(slave_list6))

def modbus_write_multiple_coils_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, starting_register5, slave_list5 = args
    label0.setText(str("write multiple coils"))
    label1.setText(str(slave_list5))
    label2.setText(str(slave_list5))

def modbus_read_holding_registers_cb(args):
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    _, starting_register3, slave_list3 = args
    label0.setText(str("read holding register"))
    label1.setText(str(starting_register3))
    label2.setText(str(slave_list3))

def setup():
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 79, 60, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 73, 100, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 67, 135, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    iso485_0 = ISO485Unit(2, port=(1, 2))
    iso485_0.init(
        tx_pin=None,
        rx_pin=None,
        baudrate=115200,
        data_bits=None,
        stop_bits=None,
        parity=None,
        ctrl_pin=None,
    )
    modbusrtuslave_0 = modbus.ModbusRTUSlave(iso485_0, device_address=1, verbose=True)
    modbusrtuslave_0.set_callback(modbusrtuslave_0.READ_COILS_EVENT, modbus_read_coils_cb)
    modbusrtuslave_0.set_callback(
        modbusrtuslave_0.WRITE_SINGLE_COIL_EVENT, modbus_write_single_coil_cb
    )
    modbusrtuslave_0.set_callback(
        modbusrtuslave_0.READ_INPUT_REGISTERS_EVENT, modbus_read_input_registers_cb
    )
    modbusrtuslave_0.set_callback(
        modbusrtuslave_0.WRITE_SINGLE_REGISTER_EVENT, modbus_write_single_registers_cb
    )
    modbusrtuslave_0.set_callback(
        modbusrtuslave_0.READ_DISCRETE_INPUTS_EVENT, modbus_read_discrete_inputs_cb
    )
    modbusrtuslave_0.set_callback(
        modbusrtuslave_0.WRITE_MULTIPLE_REGISTERS_EVENT, modbus_write_multiple_registers_cb
    )
    modbusrtuslave_0.set_callback(
        modbusrtuslave_0.WRITE_MULTIPLE_COILS_EVENT, modbus_write_multiple_coils_cb
    )
    modbusrtuslave_0.set_callback(
        modbusrtuslave_0.READ_HOLDING_REGISTERS_EVENT, modbus_read_holding_registers_cb
    )
    modbusrtuslave_0.add_coil(1000, True)
    modbusrtuslave_0.add_coil(1001, False)
    modbusrtuslave_0.add_coil(1002, True)
    modbusrtuslave_0.add_coil(1003, False)
    modbusrtuslave_0.add_coil(1004, True)
    modbusrtuslave_0.add_discrete_input(1000, True)
    modbusrtuslave_0.add_discrete_input(1001, False)
    modbusrtuslave_0.add_discrete_input(1002, True)
    modbusrtuslave_0.add_discrete_input(1003, False)
    modbusrtuslave_0.add_discrete_input(1004, True)
    modbusrtuslave_0.add_holding_register(1000, 0x0102)
    modbusrtuslave_0.add_holding_register(1001, 0x0304)
    modbusrtuslave_0.add_holding_register(1002, 0x0304)
    modbusrtuslave_0.add_holding_register(1003, 0x0304)
    modbusrtuslave_0.add_holding_register(1004, 0x0304)
    modbusrtuslave_0.add_input_register(1000, 0x0102)
    modbusrtuslave_0.add_input_register(1001, 0x0304)
    modbusrtuslave_0.add_input_register(1002, 0x0304)
    modbusrtuslave_0.add_input_register(1003, 0x0304)
    modbusrtuslave_0.add_input_register(1004, 0x0304)

def loop():
    global \
        label0, \
        label1, \
        label2, \
        modbusrtuslave_0, \
        iso485_0, \
        starting_register1, \
        slave_list1, \
        register1, \
        slave_value1, \
        starting_register4, \
        slave_list4, \
        register2, \
        slave_value2, \
        starting_register2, \
        slave_list2, \
        starting_register6, \
        slave_list6, \
        starting_register5, \
        slave_list5, \
        starting_register3, \
        slave_list3
    M5.update()
    modbusrtuslave_0.tick()

if __name__ == "__main__":
    try:
        setup()
        while True:
            loop()
    except (Exception, KeyboardInterrupt) as e:
        try:
            from utility import print_error_msg

            print_error_msg(e)
        except ImportError:
            print("please update to latest firmware")

```

Example output:

    None

## API

#### ModbusRTUSlave

<!-- .. class:: ModbusRTUSlave(uart, device_address: int = 1, context=None, ignore_unit_id: bool = False, verbose: bool = False) -->

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

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from modbus import ModbusRTUSlave
            # slave = ModbusRTUSlave(uart, device_address=1, context=context)

<!-- .. py:method:: ModbusRTUSlave.start() -->

        Start the Modbus RTU slave.

        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.start()

<!-- .. py:method:: ModbusRTUSlave.stop() -->

        Stop the Modbus RTU slave.

        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.stop()

<!-- .. py:method:: ModbusRTUSlave.add_coil(register: int, value: bool) -->

        Add a coil to the modbus register dictionary.

        :param int register: address of the coils. The address is 0x0000 to 0xFFFF.
        :param bool value: Value to add. The value is True or False.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.add_coil(0, True)

<!-- .. py:method:: ModbusRTUSlave.add_discrete_input(register: int, value: bool) -->

        Add a discrete input to the modbus register dictionary.

        :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.
        :param bool value: Value to add. The value is True or False.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.add_discrete_input(0, True)

<!-- .. py:method:: ModbusRTUSlave.add_holding_register(register: int, value: int) -->

        Add a holding register to the modbus register dictionary.

        :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param int value: Value to add. The value is 0x0000 to 0xFFFF.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.add_holding_register(0, 100)

<!-- .. py:method:: ModbusRTUSlave.add_input_register(register: int, value: int) -->

        Add an input register to the modbus register dictionary.

        :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.
        :param int value: Value to add. The value is 0x0000 to 0xFFFF.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.add_input_register(0, 100)

<!-- .. py:method:: ModbusRTUSlave.remove_coil(register: int) -->

        Remove a coil from the modbus register dictionary.

        :param int register: address of the coils. The address is 0x0000 to 0xFFFF.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.remove_coil(0)

<!-- .. py:method:: ModbusRTUSlave.remove_discrete_input(register: int) -->

        Remove a discrete input from the modbus register dictionary.

        :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.remove_discrete_input(0)

<!-- .. py:method:: ModbusRTUSlave.remove_holding_register(register: int) -->

        Remove a holding register from the modbus register dictionary.

        :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.remove_holding_register(0)

<!-- .. py:method:: ModbusRTUSlave.remove_input_register(register: int) -->

        Remove an input register from the modbus register dictionary.

        :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.remove_input_register(0)

<!-- .. py:method:: ModbusRTUSlave.get_coil(register: int) -->

        Get the coil value.

        :param int register: address of the coils. The address is 0x0000 to 0xFFFF.
        :returns: bool - The value of the coil.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                value = slave.get_coil(0)

<!-- .. py:method:: ModbusRTUSlave.get_discrete_input(register: int) -->

        Get the discrete input value.

        :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.
        :returns: bool - The value of the discrete input.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                value = slave.get_discrete_input(0)

<!-- .. py:method:: ModbusRTUSlave.get_holding_register(register: int) -->

        Get the holding register value.

        :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.
        :returns: int - The value of the holding register.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                value = slave.get_holding_register(0)

<!-- .. py:method:: ModbusRTUSlave.get_input_register(register: int) -->

        Get the input register value.

        :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.
        :returns: int - The value of the input register.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                value = slave.get_input_register(0)

<!-- .. py:method:: ModbusRTUSlave.set_coil(register: int, value: bool) -->

        Set the coil value.

        :param int register: address of the coils. The address is 0x0000 to 0xFFFF.
        :param bool value: Value to set. The value is True or False.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.set_coil(0, True)

<!-- .. py:method:: ModbusRTUSlave.set_multi_coils(register: int, value: list) -->

        Set the multi coils value.

        :param int register: address of the coils. The address is 0x0000 to 0xFFFF.
        :param list value: Values to set. The value is a list of True or False.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.set_multi_coils(0, [True, False])

<!-- .. py:method:: ModbusRTUSlave.set_discrete_input(register: int, value: bool) -->

        Set the discrete input value.

        :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.
        :param bool value: Value to set. The value is True or False.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.set_discrete_input(0, True)

<!-- .. py:method:: ModbusRTUSlave.set_multi_discrete_input(register: int, value: list) -->

        Set the multi discrete inputs value.

        :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.
        :param list value: Values to set. The value is a list of True or False.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.set_multi_discrete_input(0, [True, False])

<!-- .. py:method:: ModbusRTUSlave.set_holding_register(register: int, value: int) -->

        Set the holding register value.

        :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param int value: Value to set. The value is 0x0000 to 0xFFFF.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.set_holding_register(0, 100)

<!-- .. py:method:: ModbusRTUSlave.set_multi_holding_register(register: int, value: list) -->

        Set the multi holding registers value.

        :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param list value: Values to set. The value is a list of 0x0000 to 0xFFFF.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.set_multi_holding_register(0, [100, 200])

<!-- .. py:method:: ModbusRTUSlave.set_input_register(register: int, value: int) -->

        Set the input register value.

        :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.
        :param int value: Value to set. The value is 0x0000 to 0xFFFF.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.set_input_register(0, 100)

<!-- .. py:method:: ModbusRTUSlave.set_multi_input_register(register: int, value: list) -->

        Set the multi input registers value.

        :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.
        :param list value: Values to set. The value is a list of 0x0000 to 0xFFFF.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.set_multi_input_register(0, [100, 200])

<!-- .. py:method:: ModbusRTUSlave.tick() -->

        Modbus RTU slave tick function. This function should be called in the main loop.

        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                slave.tick()

<!-- .. py:method:: ModbusRTUSlave.set_callback(func_code: int, handler) -->

        Set the callback function for the function code.

        :param int func_code: Function code. The function code is 1 to 6, 15, 16. the symbol is defined in the modbus.ModbusRTUSlave (\*_EVENT etc.).
        :param handler: Callback function.
        :returns: None

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                def callback(arg):
                    pass
                slave.set_callback(1, callback)

<!-- .. py:data:: ModbusRTUSlave.READ_COILS_EVENT -->

        Function code 1 (Read Coils).

<!-- .. py:data:: ModbusRTUSlave.READ_DISCRETE_INPUTS_EVENT -->

        Function code 2 (Read Discrete Inputs).

<!-- .. py:data:: ModbusRTUSlave.READ_HOLDING_REGISTERS_EVENT -->

        Function code 3 (Read Holding Registers).

<!-- .. py:data:: ModbusRTUSlave.READ_INPUT_REGISTERS_EVENT -->

        Function code 4 (Read Input Registers).

<!-- .. py:data:: ModbusRTUSlave.WRITE_SINGLE_COIL_EVENT -->

        Function code 5 (Write Single Coil).

<!-- .. py:data:: ModbusRTUSlave.WRITE_SINGLE_HOLDING_REGISTER_EVENT -->

        Function code 6 (Write Single Holding Register).

<!-- .. py:data:: ModbusRTUSlave.WRITE_MULTIPLE_COILS_EVENT -->

        Function code 15 (Write Multiple Coils).

<!-- .. py:data:: ModbusRTUSlave.WRITE_MULTIPLE_HOLDING_REGISTERS_EVENT -->

        Function code 16 (Write Multiple Holding Registers).
