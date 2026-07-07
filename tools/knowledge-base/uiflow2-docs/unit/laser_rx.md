
# LaserRX Unit

<!-- .. sku:U065 -->
<!-- .. include:: ../refs/unit.laser_rx.ref -->

LASER.RX is one of the communication devices among M5Units, a Laser receiver. It is mainly built with a laser transistor. Laser communications devices are wireless connections through the atmosphere. They work similarly to fiber-optic links, except the beam is transmitted through free space. While the transmitter and receiver must require line-of-sight conditions, they have the benefit of eliminating the need for broadcast rights and buried cables. Laser communications systems can be easily deployed since they are inexpensive, small, low power and do not require any radio interference studies. Two parallel beams are needed, one for transmission and one for reception. Therefore we have a LASER.TX in parallel.

Support the following products:

|LaserRXUnit|

LaserTX Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import LaserTXUnit
import time

title1 = None
label0 = None
laser_tx_0 = None

def setup():
    global title1, label0, laser_tx_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title1 = Widgets.Title(
        "LaserTXUnit CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label0 = Widgets.Label("label0", 2, 116, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    laser_tx_0 = LaserTXUnit((1, 2), mode=2, id=1)
    laser_tx_0.init_uart(9600, 8, None, 1)

def loop():
    global title1, label0, laser_tx_0
    M5.update()
    if M5.Touch.getCount():
        laser_tx_0.write("Hello")
        label0.setText(str("Write Message"))
        time.sleep(1)
    else:
        label0.setText(str("Wait to write Message"))

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

LaserRX Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from unit import LaserRXUnit

title0 = None
laser_rx_0 = None

def setup():
    global title0, laser_rx_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "LaserRXUnit Core2 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )

    laser_rx_0 = LaserRXUnit((33, 32), mode=2, id=1)
    laser_rx_0.init_uart(9600, 8, None, 1)

def loop():
    global title0, laser_rx_0
    M5.update()
    if laser_rx_0.any():
        print(laser_rx_0.read())

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

LaserTX UIFLOW2 Example:

LaserRX UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |laserrx_core2_example.m5f2|

    |lasertx_cores3_example.m5f2|

## class LaserRXUnit

## Constructors

<!-- .. class:: LaserRXUnit(port, mode, id) -->

    Initialize the LaserRXUnit with the specified port, communication mode, and UART ID.

    :param tuple port: A tuple containing pin numbers for TX and RX.
    :param int mode: Communication mode; use PIN_MODE or UART_MODE.
    :param int id: UART ID, either 1 or 2.

    UIFLOW2:

## Methods

<!-- .. method:: LaserRXUnit.init_uart(baudrate, bits, parity, stop) -->

    Initialize UART communication with specified parameters.

    :param int baudrate: The baud rate for UART communication. Default is 115200.
    :param int bits: The number of data bits; 7, 8, or 9. Default is 8.
    :param int parity: Parity setting; None, 0, or 1. Default is 8.
    :param int stop: The number of stop bits; 1 or 2. Default is 1.

    UIFLOW2:

<!-- .. method:: LaserRXUnit.read(byte) -->

    Read data from UART. Optionally specify the number of bytes to read.

    :param  byte: The number of bytes to read. If None, reads all available data.

    :returns: The data read from UART or None if no data is available.

    UIFLOW2:

<!-- .. method:: LaserRXUnit.readline() -->

    Read a single line of data from UART.

    :returns: The line read from UART or None if no data is available.

<!-- .. method:: LaserRXUnit.any() -->

    Check if there is any data available in UART buffer.

    :returns: True if data is available; otherwise, False.

    UIFLOW2:

<!-- .. method:: LaserRXUnit.value() -->

    Get the current value of the input pin when using PIN_MODE.

    :returns: The value of the pin (0 or 1).
