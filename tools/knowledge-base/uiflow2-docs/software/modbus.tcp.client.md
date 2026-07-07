<!-- .. py:currentmodule:: modbus -->

# ModbusTCPClient

<!-- .. include:: ../refs/software.modbus.tcp.client.ref -->

ModbusTCPClient implements the Modbus TCP client. ModbusTCPClient support function codes 1 (Read Coils), 2 (Read Discrete Inputs), 3 (Read Holding Registers), 4 (Read Input Registers), 5 (Write Single Coil), 6 (Write Single Holding Register), 15 (Write Multiple Coils), and 16 (Write Multiple Holding Registers).

## UiFlow2 Example

#### CoreS3 TCP Client

Open the |cores3_tcp_client_example.m5f2| project in UiFlow2.

This example demonstrates how to use `ModbusTCPClient` to implement a Modbus TCP client.

UiFlow2 Code Block:

Example output:

    None

## MicroPython Example

#### CoreS3 TCP Client

This example demonstrates how to use `ModbusTCPClient` to implement a Modbus TCP client.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
import modbus
import time

label0 = None
label1 = None
label2 = None
label3 = None
label4 = None
label5 = None
label6 = None
label7 = None
label8 = None
label9 = None
label14 = None
label19 = None
label24 = None
label10 = None
label15 = None
label20 = None
label25 = None
label11 = None
label16 = None
label21 = None
label26 = None
label12 = None
label17 = None
label22 = None
label27 = None
label13 = None
label18 = None
label23 = None
label28 = None
modbustcpclient_0 = None

hr = None
coil = None
res = None

def setup():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        label9, \
        label14, \
        label19, \
        label24, \
        label10, \
        label15, \
        label20, \
        label25, \
        label11, \
        label16, \
        label21, \
        label26, \
        label12, \
        label17, \
        label22, \
        label27, \
        label13, \
        label18, \
        label23, \
        label28, \
        modbustcpclient_0, \
        hr, \
        coil, \
        res

    M5.begin()
    Widgets.setRotation(1)
    Widgets.fillScreen(0x222222)
    label0 = Widgets.Label("co", 65, 8, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label1 = Widgets.Label("di", 135, 8, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label2 = Widgets.Label("hr", 205, 8, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label3 = Widgets.Label("ir", 275, 8, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label4 = Widgets.Label("1000", 4, 45, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label5 = Widgets.Label("1001", 4, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label6 = Widgets.Label("1002", 4, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label7 = Widgets.Label("1003", 4, 165, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label8 = Widgets.Label("1004", 4, 205, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label9 = Widgets.Label("a00", 65, 45, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label14 = Widgets.Label("a01", 135, 45, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label19 = Widgets.Label("a02", 205, 45, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label24 = Widgets.Label("a03", 275, 45, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label10 = Widgets.Label("a10", 65, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label15 = Widgets.Label("a11", 135, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label20 = Widgets.Label("a12", 205, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label25 = Widgets.Label("a13", 275, 85, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label11 = Widgets.Label("a20", 65, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label16 = Widgets.Label("a21", 135, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label21 = Widgets.Label("a22", 205, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label26 = Widgets.Label("a23", 275, 125, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label12 = Widgets.Label("a30", 65, 165, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label17 = Widgets.Label("a31", 135, 165, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label22 = Widgets.Label("a32", 205, 165, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label27 = Widgets.Label("a33", 275, 165, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label13 = Widgets.Label("a40", 65, 205, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label18 = Widgets.Label("a41", 135, 205, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label23 = Widgets.Label("a42", 205, 205, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label28 = Widgets.Label("a43", 275, 205, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    modbustcpclient_0 = modbus.ModbusTCPClient("192.168.52.60", 5000, verbose=True)
    modbustcpclient_0.connect()
    hr = 0
    res = modbustcpclient_0.read_coils(1, 1000, 5, timeout=2000)
    label9.setText(str(res[0]))
    label10.setText(str(res[1]))
    label11.setText(str(res[2]))
    label12.setText(str(res[3]))
    label13.setText(str(res[4]))
    res = modbustcpclient_0.read_discrete_inputs(1, 1000, 5, timeout=2000)
    label14.setText(str(res[0]))
    label15.setText(str(res[1]))
    label16.setText(str(res[2]))
    label17.setText(str(res[3]))
    label18.setText(str(res[4]))
    res = modbustcpclient_0.read_holding_registers(1, 1000, 5, timeout=2000)
    label19.setText(str(res[0]))
    label20.setText(str(res[1]))
    label21.setText(str(res[2]))
    label22.setText(str(res[3]))
    label23.setText(str(res[4]))
    res = modbustcpclient_0.read_input_registers(1, 1000, 5, timeout=2000)
    label24.setText(str(res[0]))
    label25.setText(str(res[1]))
    label26.setText(str(res[2]))
    label27.setText(str(res[3]))
    label28.setText(str(res[4]))

def loop():
    global \
        label0, \
        label1, \
        label2, \
        label3, \
        label4, \
        label5, \
        label6, \
        label7, \
        label8, \
        label9, \
        label14, \
        label19, \
        label24, \
        label10, \
        label15, \
        label20, \
        label25, \
        label11, \
        label16, \
        label21, \
        label26, \
        label12, \
        label17, \
        label22, \
        label27, \
        label13, \
        label18, \
        label23, \
        label28, \
        modbustcpclient_0, \
        hr, \
        coil, \
        res
    M5.update()
    hr = (hr + 1) % 65535
    coil = not coil
    modbustcpclient_0.write_single_coil(1, 1000, coil, timeout=2000)
    modbustcpclient_0.write_single_register(1, 1000, hr, timeout=2000)
    modbustcpclient_0.write_multiple_coils(1, 1000, [coil, coil, coil, coil, coil], timeout=2000)
    label9.setText(str(coil))
    label10.setText(str(coil))
    label11.setText(str(coil))
    modbustcpclient_0.write_multiple_registers(1, 1000, [hr, hr, hr, hr, hr], timeout=2000)
    label19.setText(str(hr))
    label20.setText(str(hr))
    label21.setText(str(hr))
    time.sleep(1)

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

#### ModbusTCPClient

<!-- .. class:: ModbusTCPClient(host: str, port: int=502, verbose: bool=False) -->

    Create a ModbusTCPClient object.

    :param str host: Hostname or IP address.
    :param int port: Port number.
    :param bool verbose: Verbose mode.

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from modbus import ModbusTCPClient
            client = ModbusTCPClient('192.168.1.100', 502)

<!-- .. py:method:: ModbusTCPClient.connect() -> None -->

        Connect to the Modbus server.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                client.connect()

<!-- .. py:method:: ModbusTCPClient.disconnect() -> None -->

        Disconnect from the Modbus server.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                client.disconnect()

<!-- .. py:method:: ModbusTCPClient.read_coils(address, register, quantity, timeout: int=2000) -> list -->

        Read coils.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the coils. The address is 0x0000 to 0xFFFF.
        :param int quantity: Quantity of registers to read.
        :param int timeout: Timeout in milliseconds.

        :return: A list of coils. The item of the list is True or False.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                client.read_coils(1, 0, 10)

<!-- .. py:method:: ModbusTCPClient.read_discrete_inputs(address, register, quantity, timeout: int=2000) -> list -->

        Read discrete inputs.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the discrete inputs. The address is 0x0000 to 0xFFFF.
        :param int quantity: Quantity of registers to read.
        :param int timeout: Timeout in milliseconds.

        :return: A list of discrete inputs. The item of the list is True or False.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                client.read_discrete_inputs(1, 0, 10)

<!-- .. py:method:: ModbusTCPClient.read_holding_registers(address, register, quantity, timeout: int=2000) -> list -->

        Read holding registers.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param int quantity: Quantity of registers to read.
        :param int timeout: Timeout in milliseconds.

        :return: A list of holding registers. The item of the list is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                client.read_holding_registers(1, 0, 10)

<!-- .. py:method:: ModbusTCPClient.read_input_registers(address, register, quantity, timeout: int=2000) -> list -->

        Read input registers.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the input registers. The address is 0x0000 to 0xFFFF.
        :param int quantity: Quantity of registers to read.
        :param int timeout: Timeout in milliseconds.

        :return: A list of input registers. The item of the list is 0x0000 to 0xFFFF.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                client.read_input_registers(1, 0, 10)

<!-- .. py:method:: ModbusTCPClient.write_single_coil(address, register, value, timeout: int=2000) -> bool -->

        Write a single coil.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the coils. The address is 0x0000 to 0xFFFF.
        :param int value: Value to write. The value is True or False.
        :param int timeout: Timeout in milliseconds.

        :return: The value of the coil.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                client.write_single_coil(1, 0, True)

<!-- .. py:method:: ModbusTCPClient.write_single_register(address, register, value, timeout: int=2000) -> int -->

        Write a single register.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param int value: Value to write. The value is 0x0000 to 0xFFFF.
        :param int timeout: Timeout in milliseconds.

        :return: the written value

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                client.write_single_register(1, 0, 100)

<!-- .. py:method:: ModbusTCPClient.write_multiple_coils(address, register, values, timeout: int=2000) -> int -->

        Write multiple coils.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the coils. The address is 0x0000 to 0xFFFF.
        :param list values: Values to write. The item of the list is True or False.
        :param int timeout: Timeout in milliseconds.

        :return: the written count.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                client.write_multiple_coils(1, 0, [True, False, True])

<!-- .. py:method:: ModbusTCPClient.write_multiple_registers(address: int, register: int, values: list, timeout: int=2000) -> int -->

        Write multiple registers.

        :param int address: Slave address. The address is 0 to 247.
        :param int register: Start address of the holding registers. The address is 0x0000 to 0xFFFF.
        :param list values: Values to write. The item of the list is 0x0000 to 0xFFFF.
        :param int timeout: Timeout in milliseconds.

        :return: the written count.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                client.write_multiple_registers(1, 0, [100, 200, 300])
