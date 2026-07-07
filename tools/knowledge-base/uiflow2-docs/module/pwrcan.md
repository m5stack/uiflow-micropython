<!-- .. py:currentmodule:: module -->

# PwrCAN

<!-- .. include:: ../refs/module.pwrcan.ref -->

PwrCAN Module 13.2 is a multifunctional module designed for the PwrCAN bus, integrating isolated CAN communication and DC 9-24V power bus. The module also includes Pwr485 (with isolation) bus functionality and can provide isolated 5V power supply to the M5 host. The CAN communication part uses the CA-IS3050G isolated transceiver, and the RS485 part uses the CA-IS3082W isolated transceiver. The GPIOs related to CAN and RS485 communication can be selected through dip switches, and the 120-ohm terminal resistance at the CAN and RS485 outputs can also be selected through dip switches. The module's power bus supports DC 9-24V wide voltage input, with the DC socket directly connected to the HT3.96 and XT30 power parts. The built-in isolated power module F0505S-2WR3 provides power to the M5 host. This module is suitable for fields such as robot control, protocol conversion, industrial automation, automotive communication systems, intelligent transportation, and building automation.

Supported Products:

|PwrCANModule|

## UiFlow2 Example

#### Simple CAN and RS485 Communication

Open the |pwrcan_cores3_example.m5f2| project in UiFlow2.

This example demonstrates how to use the PwrCAN module.

Touch the screen to send CAN messages and RS485 data. Received RS485 data will be printed in the label.

UiFlow2 Code Block:

Example output:

    Screen will display the received RS485 data.

## MicroPython Example

#### Simple CAN and RS485 Communication

This example demonstrates how to use the PwrCAN module in MicroPython.

Touch the screen to send CAN messages and RS485 data. Received RS485 data will be printed in the label.

MicroPython Code Block:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from module import PwrCANModule
from module import PwrCANModuleRS485
from unit import RS485Unit
import time

title0 = None
label3 = None
label0 = None
label1 = None
label2 = None
pwrcan_0 = None
pwrcan_1 = None
rs485_0 = None

def setup():
    global title0, label3, label0, label1, label2, pwrcan_0, pwrcan_1, rs485_0

    M5.begin()
    Widgets.fillScreen(0x222222)
    title0 = Widgets.Title(
        "PwrCANModule CoreS3 Example", 3, 0xFFFFFF, 0x0000FF, Widgets.FONTS.DejaVu18
    )
    label3 = Widgets.Label("CAN Rec:", 0, 95, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)
    label0 = Widgets.Label(
        "CAN Message State: ", 0, 49, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label1 = Widgets.Label(
        "RS485 Message State: ", 0, 138, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18
    )
    label2 = Widgets.Label("RS485 Rec:", 0, 179, 1.0, 0xFFFFFF, 0x222222, Widgets.FONTS.DejaVu18)

    pwrcan_0 = PwrCANModule(0, 17, 18, PwrCANModule.NORMAL, baudrate=1000000)
    pwrcan_1 = PwrCANModuleRS485(1, baudrate=115200, bits=8, parity=None, stop=1, tx=13, rx=7)
    rs485_0 = RS485Unit(
        2,
        port=(1, 2),
        baudrate=115200,
        bits=8,
        parity=None,
        stop=1,
        txbuf=256,
        rxbuf=256,
        timeout=0,
        timeout_char=0,
        invert=0,
        flow=0,
    )

def loop():
    global title0, label3, label0, label1, label2, pwrcan_0, pwrcan_1, rs485_0
    M5.update()
    if M5.Touch.getCount():
        pwrcan_0.send("uiflow2", 0, timeout=0, rtr=False, extframe=False)
        label0.setText(str("CAN Message State: Send"))
        pwrcan_1.write("RS485_uiflow2" + "\r\n")
        label1.setText(str("RS485 Message State: Send"))
        time.sleep(1)
    else:
        label0.setText(str("CAN Message State: Not Send"))
        label1.setText(str("RS485 Message State: Not Send"))
    if pwrcan_0.any(0):
        label3.setText(str((str("CAN Rec:") + str((pwrcan_0.recv(0, timeout=5000))))))
    if rs485_0.any():
        label2.setText(str((str("RS485 Rec:") + str((rs485_0.read())))))

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

    Screen will display the received RS485 data.

## API

#### PwrCANModule

<!-- .. class:: PwrCANModule(id, mode, tx, rx, prescaler=32, sjw=3, bs1=15, bs2=4, triple_sampling=False) -->

    Initialise the CAN bus with the given parameters.

    :param int id: The CAN bus ID.
    :param int mode: One of NORMAL, NO_ACKNOWLEDGE, LISTEN_ONLY.
    :param int tx: The pin to use for transmitting data.
    :param int rx: The pin to use for receiving data.
    :param int prescaler: The value by which the CAN input clock is divided to generate the nominal bit time quanta. Value between 1 and 1024 inclusive for classic CAN.
    :param int sjw: The resynchronisation jump width in units of time quanta for nominal bits; value between 1 and 4 inclusive for classic CAN.
    :param int bs1: Defines the location of the sample point in units of the time quanta for nominal bits; value between 1 and 16 inclusive for classic CAN.
    :param int bs2: Defines the location of the transmit point in units of the time quanta for nominal bits; value between 1 and 8 inclusive for classic CAN.
    :param bool triple_sampling: Enables triple sampling when the TWAI controller samples a bit.

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from module import PwrCANModule

            can = PwrCANModule(0, PwrCANModule.NORMAL, 13, 14)

    PwrCANModule class inherits CAN class. See :class:`hardware.CAN <hardware.CAN>` for more details.

#### PwrCANModuleRS485

<!-- .. class:: PwrCANModuleRS485(id, baudrate=9600, bits=8, parity=None, stop=1) -->

    Construct a UART object of the given id.

    :param int id: UART ID.
    :param int baudrate: Clock rate.
    :param int bits: Number of bits per character, 7, 8, or 9.
    :param int parity: The parity, None, 0 (even), or 1 (odd).
    :param int stop: Number of stop bits, 1 or 2.

    UiFlow2 Code Block:

    MicroPython Code Block:

<!-- .. code-block:: python -->

            from module import PwrCANModuleRS485
            rs485 = PwrCANModuleRS485(1, baudrate=115200)

<!-- .. py:method:: PwrCANModuleRS485.init(baudrate=9600, bits=8, parity=None, stop=1, *, tx=None, rx=None, rts=None, cts=None, txbuf=None, rxbuf=None, timeout=None, timeout_char=None, invert=None, flow=None) -->

        Initialise the UART bus with the given parameters.

        :param int baudrate: The clock rate.
        :param int bits: The number of bits per character, 7, 8 or 9.
        :param int parity: The parity, ``None``, 0 (even) or 1 (odd).
        :param int stop: The number of stop bits, 1 or 2.
        :param int tx: The TX pin to use.
        :param int rx: The RX pin to use.
        :param int rts: The RTS (output) pin to use for hardware receive flow control.
        :param int cts: The CTS (input) pin to use for hardware transmit flow control.
        :param int txbuf: The length in characters of the TX buffer.
        :param int rxbuf: The length in characters of the RX buffer.
        :param int timeout: The time to wait for the first character (in ms).
        :param int timeout_char: The time to wait between characters (in ms).
        :param int invert: Specifies which lines to invert.
        :param int flow: Specifies which hardware flow control signals to use.

<!-- .. note:: -->
            It is possible to call ``init()`` multiple times on the same object in
            order to reconfigure UART on the fly. That allows using single UART
            peripheral to serve different devices attached to different GPIO pins.
            Only one device can be served at a time in that case.
            Also do not call ``deinit()`` as it will prevent calling ``init()``
            again.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                rs485.init(baudrate=9600, bits=8, parity=None, stop=1)

<!-- .. py:method:: PwrCANModuleRS485.deinit() -->

        Turn off the UART bus.

<!-- .. note:: -->
            You will not be able to call ``init()`` on the object after ``deinit()``.
            A new instance needs to be created in that case.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                rs485.deinit()

<!-- .. py:method:: PwrCANModuleRS485.any() -->

        Returns an integer counting the number of characters that can be read without
        blocking.

        :returns: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                rs485.any()

<!-- .. py:method:: PwrCANModuleRS485.read([nbytes]) -->

        Read characters.

        :param int nbytes: If specified then read at most that many bytes, otherwise read as much data as possible.
        :returns: bytes

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                data = rs485.read()

<!-- .. py:method:: PwrCANModuleRS485.readinto(buf[, nbytes]) -->

        Read bytes into the ``buf``.

        :param bytearray buf: The buffer to read into.
        :param int nbytes: If specified then read at most that many bytes. Otherwise, read at most ``len(buf)`` bytes.
        :returns: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                buf = bytearray(10)
                rs485.readinto(buf)

<!-- .. py:method:: PwrCANModuleRS485.readline() -->

        Read a line, ending in a newline character.

        :returns: bytes

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                line = rs485.readline()

<!-- .. py:method:: PwrCANModuleRS485.write(buf) -->

        Write the buffer of bytes to the bus.

        :param bytes buf: The buffer/bytes to write.
        :returns: int

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                rs485.write(b'data')

<!-- .. py:method:: PwrCANModuleRS485.sendbreak() -->

        Send a break condition on the bus.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                rs485.sendbreak()

<!-- .. py:method:: PwrCANModuleRS485.flush() -->

        Waits until all data has been sent.

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                rs485.flush()

<!-- .. py:method:: PwrCANModuleRS485.txdone() -->

        Tells whether all data has been sent.

        :returns: bool

        UiFlow2 Code Block:

        MicroPython Code Block:

<!-- .. code-block:: python -->

                rs485.txdone()
