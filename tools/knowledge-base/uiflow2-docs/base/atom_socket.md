# Atom Socket Base

<!-- .. include:: ../refs/base.atom_socket.ref -->

The `ATOMSocketBase` class is a smart power socket integrated with the M5 ATOM controller. It features a built-in HLW8032 high-precision power measurement IC, enabling it to measure the voltage, current, power, and energy of the load. Additionally, it can function as a smart socket to control the power state of the load, making it suitable for applications in smart homes, industrial control, and energy management.

Supports the following products:

|ATOMSocketBase|

Micropython Example:

```python
# SPDX-FileCopyrightText: 2024 M5Stack Technology CO LTD
#
# SPDX-License-Identifier: MIT

import os, sys, io
import M5
from M5 import *
from base import ATOMSocketBase
from hardware import *

atomsocket = None

as_voltage = None
as_current = None
as_power = None
as_kwh = None
onoff = None

def atom_socket_receive_event(voltage, current, power, kwh):
    global atomsocket, as_voltage, as_current, as_power, as_kwh, onoff
    as_voltage = voltage
    as_current = current
    as_power = power
    as_kwh = kwh
    print("hello M5")
    print("hello M5")

def btnA_wasClicked_event(state):  # noqa: N802
    global atomsocket, as_voltage, as_current, as_power, as_kwh, onoff
    onoff = not onoff
    if onoff:
        atomsocket.set_relay(True)
    else:
        atomsocket.set_relay(False)

def setup():
    global atomsocket, as_voltage, as_current, as_power, as_kwh, onoff

    M5.begin()
    BtnA.setCallback(type=BtnA.CB_TYPE.WAS_CLICKED, cb=btnA_wasClicked_event)

    atomsocket = ATOMSocketBase(1, port=(22, 33), relay=23)
    onoff = False
    atomsocket.set_relay(False)
    atomsocket.receive_none_block(atom_socket_receive_event)

def loop():
    global atomsocket, as_voltage, as_current, as_power, as_kwh, onoff
    M5.update()

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

UIFLOW2 Example:

<!-- .. only:: builder_html -->

    |atomlite_socket_example.m5f2|

## class ATOMSocketBase

## Constructors

<!-- .. class:: ATOMSocketBase(_id: Literal[0, 1, 2], port: list | tuple, relay: int = 23) -->

    Initializes the ATOM Socket.

    - ``_id``: Serial ID, not actually used by this base.
    - ``port``: UART pin numbers.
    - ``relay``: The relay pin number.

    UIFLOW2:

## Methods

<!-- .. method:: ATOMSocketBase.set_relay(state: bool) -> None -->

    Sets the state of the ATOM Socket's relay.

    - ``state``: The desired state of the relay, True = ON, False = OFF.

    UIFLOW2:

<!-- .. method:: ATOMSocketBase.get_data(timeout=3000) -> tuple -->

    Retrieves data from the ATOM Socket.

    - ``timeout``: Function timeout period.

    Returns the ATOM Socket data: Tuple (Voltage (V), Current (A), Power (W), Total Energy (KWh)), or None if timeout occurs.

    UIFLOW2:

<!-- .. method:: ATOMSocketBase.get_voltage() -> float -->

    Retrieves the voltage measurement from the ATOM Socket.

    UIFLOW2:

<!-- .. method:: ATOMSocketBase.get_current() -> float -->

    Retrieves the current measurement from the ATOM Socket.

    UIFLOW2:

<!-- .. method:: ATOMSocketBase.get_power() -> float -->

    Retrieves the power measurement from the ATOM Socket.

    UIFLOW2:

<!-- .. method:: ATOMSocketBase.get_pf() -> int -->

    Retrieves the power factor from the ATOM Socket.

    UIFLOW2:

<!-- .. method:: ATOMSocketBase.get_inspecting_power() -> float -->

    Calculates the inspecting power of the ATOM Socket.

    UIFLOW2:

<!-- .. method:: ATOMSocketBase.get_power_factor() -> float -->

    Calculates the power factor of the ATOM Socket.

    UIFLOW2:

<!-- .. method:: ATOMSocketBase.get_kwh() -> float -->

    Retrieves the accumulated energy measurement in KWh from the ATOM Socket.

    UIFLOW2:

<!-- .. method:: ATOMSocketBase.stop_receive_data() -> None -->

    Stops receiving data from the ATOM Socket.

    UIFLOW2:

<!-- .. method:: ATOMSocketBase.receive_none_block(receive_callback) -> None -->

    Receives data from the ATOM Socket in non-blocking mode.

    - ``receive_callback``: Callback function to handle the received data.

    UIFLOW2:
