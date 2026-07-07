<!-- .. py:currentmodule:: modbus -->

# ModbusTCPServer

<!-- .. include:: ../refs/software.modbus.tcp.server.ref -->

ModbusTCPServer implements the Modbus TCP server. ModbusTCPServer support function codes 1 (Read Coils), 2 (Read Discrete Inputs), 3 (Read Holding Registers), 4 (Read Input Registers), 5 (Write Single Coil), 6 (Write Single Holding Register), 15 (Write Multiple Coils), and 16 (Write Multiple Holding Registers).

## UiFlow2 Example

#### CoreS3 TCP Server

Open the |cores3_tcp_server_example.m5f2| project in UiFlow2.

This example demonstrates how to use `ModbusTCPServer` to implement a Modbus TCP server.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### CoreS3 TCP Server

This example demonstrates how to use `ModbusTCPServer` to implement a Modbus TCP server.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT
import os, sys, io
import M5
from M5 import *
import modbus
import network

label0 = None
label1 = None
label3 = None
label2 = None
wlan_sta = None
modbustcpserver_0 = None

starting_register4 = None
slave_list4 = None
starting_register1 = None
slave_list1 = None
starting_register2 = None
slave_list2 = None
register2 = None
slave_value2 = None
starting_register3 = None
slave_list3 = None
starting_register6 = None
slave_list6 = None
register1 = None
slave_value1 = None
starting_register5 = None
slave_list5 = None

def modbus_read_input_registers_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, starting_register4, slave_list4 = args
    label0.setText(str("read input register"))
    label1.setText(str(starting_register4))
    label2.setText(str(slave_list4))

def modbus_read_coils_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, starting_register1, slave_list1 = args
    label0.setText(str("read coils"))
    label1.setText(str(starting_register1))
    label2.setText(str(slave_list1))

def modbus_read_discrete_inputs_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, starting_register2, slave_list2 = args
    label0.setText(str("read  discrete input"))
    label1.setText(str(starting_register2))
    label2.setText(str(slave_list2))

def modbus_write_single_registers_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, register2, slave_value2 = args
    label0.setText(str("write single registers"))
    label1.setText(str(register2))
    label2.setText(str(slave_value2))

def modbus_read_holding_registers_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, starting_register3, slave_list3 = args
    label0.setText(str("read holding register"))
    label1.setText(str(starting_register3))
    label2.setText(str(slave_list3))

def modbus_write_multiple_registers_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, starting_register6, slave_list6 = args
    label0.setText(str("write multiple registers"))
    label1.setText(str(slave_list6))
    label2.setText(str(slave_list6))

def modbus_write_single_coil_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, register1, slave_value1 = args
    label0.setText(str("write single coil"))
    label1.setText(str(register1))
    label2.setText(str(slave_value1))

def modbus_write_multiple_coils_cb(args):
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    _, starting_register5, slave_list5 = args
    label0.setText(str("write multiple coils"))
    label0.setText(str(slave_list5))
    label0.setText(str(slave_list5))

def setup():
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("label0", 61, 54, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("label1", 58, 94, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("label3", 53, 11, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("label2", 58, 133, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    wlan_sta = network.WLAN(network.STA_IF)
    while not (wlan_sta.isconnected()):
        pass
    label3.setText(str(wlan_sta.ifconfig()[0]))
    modbustcpserver_0 = modbus.ModbusTCPServer("0.0.0.0", 5000, device_address=1, verbose=False)
    modbustcpserver_0.set_callback(
        modbustcpserver_0.READ_INPUT_REGISTERS_EVENT, modbus_read_input_registers_cb
    )
    modbustcpserver_0.set_callback(modbustcpserver_0.READ_COILS_EVENT, modbus_read_coils_cb)
    modbustcpserver_0.set_callback(
        modbustcpserver_0.READ_DISCRETE_INPUTS_EVENT, modbus_read_discrete_inputs_cb
    )
    modbustcpserver_0.set_callback(
        modbustcpserver_0.WRITE_SINGLE_REGISTER_EVENT, modbus_write_single_registers_cb
    )
    modbustcpserver_0.set_callback(
        modbustcpserver_0.READ_HOLDING_REGISTERS_EVENT, modbus_read_holding_registers_cb
    )
    modbustcpserver_0.set_callback(
        modbustcpserver_0.WRITE_MULTIPLE_REGISTERS_EVENT, modbus_write_multiple_registers_cb
    )
    modbustcpserver_0.set_callback(
        modbustcpserver_0.WRITE_SINGLE_COIL_EVENT, modbus_write_single_coil_cb
    )
    modbustcpserver_0.set_callback(
        modbustcpserver_0.WRITE_MULTIPLE_COILS_EVENT, modbus_write_multiple_coils_cb
    )
    modbustcpserver_0.add_coil(1000, True)
    modbustcpserver_0.add_coil(1001, False)
    modbustcpserver_0.add_coil(1002, True)
    modbustcpserver_0.add_coil(1003, False)
    modbustcpserver_0.add_coil(1004, True)
    modbustcpserver_0.add_discrete_input(1000, True)
    modbustcpserver_0.add_discrete_input(1001, False)
    modbustcpserver_0.add_discrete_input(1002, True)
    modbustcpserver_0.add_discrete_input(1003, False)
    modbustcpserver_0.add_discrete_input(1004, True)
    modbustcpserver_0.add_holding_register(1000, 0x0102)
    modbustcpserver_0.add_holding_register(1001, 0x0304)
    modbustcpserver_0.add_holding_register(1002, 0x0506)
    modbustcpserver_0.add_holding_register(1003, 0x0708)
    modbustcpserver_0.add_holding_register(1004, 0x090A)
    modbustcpserver_0.add_input_register(1000, 0x0102)
    modbustcpserver_0.add_input_register(1001, 0x0304)
    modbustcpserver_0.add_input_register(1002, 0x0506)
    modbustcpserver_0.add_input_register(1003, 0x0708)
    modbustcpserver_0.add_input_register(1004, 0x090A)
    modbustcpserver_0.start()

def loop():
    global \
        label0, \
        label1, \
        label3, \
        label2, \
        wlan_sta, \
        modbustcpserver_0, \
        starting_register4, \
        slave_list4, \
        starting_register1, \
        slave_list1, \
        starting_register2, \
        slave_list2, \
        register2, \
        slave_value2, \
        starting_register3, \
        slave_list3, \
        starting_register6, \
        slave_list6, \
        register1, \
        slave_value1, \
        starting_register5, \
        slave_list5
    M5.update()
    modbustcpserver_0.tick()

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

#### ModbusTCPServer

<!-- .. class:: ModbusTCPServer(host: str, port: int=502, verbose: bool=False) -->

    Create a ModbusTCPServer object.

    :param str host: Hostname or IP address.
    :param int port: Port number.
    :param bool verbose: Verbose mode.

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from modbus import ModbusTCPServer
            server = ModbusTCPServer('0.0.0.0', 502)

<!-- .. method:: ModbusTCPServer.start() -> None -->

        Start the Modbus RTU slave.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.start()

<!-- .. method:: ModbusTCPServer.stop() -> None -->

        Stop the Modbus RTU slave.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.stop()

<!-- .. method:: ModbusTCPServer.add_coil(register: int, value: bool) -> None -->

        Add a coil to the modbus register dictionary.

        :param int register: address of the coils. The address is 0x0000 to 0xFFFF.
        :param int value: Value to add. The value is True or False.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.add_coil(0, False)

<!-- .. method:: ModbusTCPServer.add_discrete_input(register: int, value: bool) -> None -->

        Add a discrete input to the modbus register dictionary.

        :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.
        :param int value: Value to add. The value is True or False.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.add_discrete_input(0, False)

<!-- .. method:: ModbusTCPServer.add_holding_register(register: int, value: int) -> None -->

        Add a holding register to the modbus register dictionary.

        :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param int value: Value to add. The value is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.add_holding_register(0, 0)

<!-- .. method:: ModbusTCPServer.add_input_register(register: int, value: int) -> None -->

        Add an input register to the modbus register dictionary.

        :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.
        :param int value: Value to add. The value is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.add_input_register(0, 0)

<!-- .. method:: ModbusTCPServer.remove_coil(register: int) -> None -->

        Remove a coil from the modbus register dictionary.

        :param int register: address of the coils. The address is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.remove_coil(0)

<!-- .. method:: ModbusTCPServer.remove_discrete_input(register: int) -> None -->

        Remove a discrete input from the modbus register dictionary.

        :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.remove_discrete_input(0)

<!-- .. method:: ModbusTCPServer.remove_holding_register(register: int) -> None -->

        Remove a holding register from the modbus register dictionary.

        :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.remove_holding_register(0)

<!-- .. method:: ModbusTCPServer.remove_input_register(register: int) -> None -->

        Remove an input register from the modbus register dictionary.

        :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.remove_input_register(0)

<!-- .. method:: ModbusTCPServer.get_coil(register: int) -> bool -->

        Get the coil value.

        :param int register: address of the coils. The address is 0x0000 to 0xFFFF.

        :return: The value of the coil.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.get_coil(0)

<!-- .. method:: ModbusTCPServer.get_discrete_input(register: int) -> bool -->

        Get the discrete input value.

        :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.

        :return: The value of the discrete input.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.get_discrete_input(0)

<!-- .. method:: ModbusTCPServer.get_holding_register(register: int) -> int -->

        Get the holding register value.

        :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.

        :return: The value of the holding register.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.get_holding_register(0)

<!-- .. method:: ModbusTCPServer.get_input_register(register: int) -> int -->

        Get the input register value.

        :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.

        :return: The value of the input register.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.get_input_register(0)

<!-- .. method:: ModbusTCPServer.set_coil(register: int, value: bool) -> None -->

        Set the coil value.

        :param int register: address of the coils. The address is 0x0000 to 0xFFFF.
        :param int value: Value to set. The value is True or False.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.set_coil(0, False)

<!-- .. method:: ModbusTCPServer.set_multi_coils(register: int, value: list) -> None -->

        Set the multi coils value.

        :param int register: address of the coils. The address is 0x0000 to 0xFFFF.
        :param list value: Values to set. The value is a list of True or False.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.set_multi_coils(0, [False, True])

<!-- .. method:: ModbusTCPServer.set_discrete_input(register: int, value: bool) -> None -->

        Set the discrete input value.

        :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.
        :param int value: Value to set. The value is True or False.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.set_discrete_input(0, False)

<!-- .. method:: ModbusTCPServer.set_multi_discrete_input(register: int, value: list) -> None -->

        Set the multi discrete inputs value.

        :param int register: address of the discrete inputs. The address is 0x0000 to 0xFFFF.
        :param list value: Values to set. The value is a list of True or False.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.set_multi_discrete_input(0, [False, True])

<!-- .. method:: ModbusTCPServer.set_holding_register(register: int, value: int) -> None -->

        Set the holding register value.

        :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param int value: Value to set. The value is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.set_holding_register(0, 0)

<!-- .. method:: ModbusTCPServer.set_multi_holding_register(register: int, value: list) -> None -->

        Set the multi holding registers value.

        :param int register: address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param list value: Values to set. The value is a list of 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.set_multi_holding_register(0, [0, 1])

<!-- .. method:: ModbusTCPServer.set_input_register(register: int, value: int) -> None -->

        Set the input register value.

        :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.
        :param int value: Value to set. The value is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.set_input_register(0, 0)

<!-- .. method:: ModbusTCPServer.set_multi_input_register(register: int, value: list) -> None -->

        Set the multi input registers value.

        :param int register: address of the input registers. The address is 0x0000 to 0xFFFF.
        :param list value: Values to set. The value is a list of 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.set_multi_input_register(0, [0, 1])

<!-- .. method:: ModbusTCPServer.tick() -> None -->

        Modbus RTU slave tick function. This function should be called in the main loop.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                server.tick()

<!-- .. method:: ModbusTCPServer.set_callback(func_code: int, handler) -> None -->

        Set the callback function for the function code.

        :param int func_code: Function code. The function code is 1 to 6, 15, 16. the symbol is defined in the modbus.ModbusTCPServer (\*_EVENT etc.).
        :param handler: Callback function.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                def cb(arg):
                    pass
                server.set_callback(1, cb)

<!-- .. data:: ModbusTCPServer.READ_COILS_EVENT -->

        Function code 1 (Read Coils).

<!-- .. data:: ModbusTCPServer.READ_DISCRETE_INPUTS_EVENT -->

        Function code 2 (Read Discrete Inputs).

<!-- .. data:: ModbusTCPServer.READ_HOLDING_REGISTERS_EVENT -->

        Function code 3 (Read Holding Registers).

<!-- .. data:: ModbusTCPServer.READ_INPUT_REGISTERS_EVENT -->

        Function code 4 (Read Input Registers).

<!-- .. data:: ModbusTCPServer.WRITE_SINGLE_COIL_EVENT -->

        Function code 5 (Write Single Coil).

<!-- .. data:: ModbusTCPServer.WRITE_SINGLE_HOLDING_REGISTER_EVENT -->

        Function code 6 (Write Single Holding Register).

<!-- .. data:: ModbusTCPServer.WRITE_MULTIPLE_COILS_EVENT -->

        Function code 15 (Write Multiple Coils).

<!-- .. data:: ModbusTCPServer.WRITE_MULTIPLE_HOLDING_REGISTERS_EVENT -->

        Function code 16 (Write Multiple Holding Registers).
