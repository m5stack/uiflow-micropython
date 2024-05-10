ATOM Socket Base
================

.. include:: ../refs/base.atom_socket.ref

The `ATOMSocketBase` class is a smart power socket integrated with the M5 ATOM controller. It features a built-in HLW8032 high-precision power measurement IC, enabling it to measure the voltage, current, power, and energy of the load. Additionally, it can function as a smart socket to control the power state of the load, making it suitable for applications in smart homes, industrial control, and energy management.

Supports the following products:

|ATOMSocketBase|

Micropython Example::

    from machine import I2C
    from base import ATOMSocketBase

    atomsocket = ATOMSocketBase(1, (22, 33), 23)  # For ATOM Lite
    atomsocket = ATOMSocketBase(1, (5, 8), 7)  # For ATOM S3
    # Retrieve data
    print(atomsocket.get_data())  # Outputs (230.4192, 0.02074951, 0.8106091, 0.0)
    atomsocket.set_relay(True)    # Turns on the relay
    atomsocket.set_relay(False)   # Turns off the relay
    # Read metrics
    print("Voltage:", atomsocket.get_voltage(), "V")
    print("Current:", atomsocket.get_current(), "A")
    print("Power:", atomsocket.get_power(), "W")
    print("Power Factor:", atomsocket.get_power_factor())
    print("Accumulated Energy:", atomsocket.get_kwh(), "kWh")
    # Receive data in non-blocking mode
    def callback(voltage, current, power, kwh):
        print(voltage, current, power, kwh)
    atomsocket.receive_none_block(callback)
    # Stop receiving data
    atomsocket.stop_receive_data()

UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

ATOMSocketBase Class
--------------------

Constructors
------------

.. class:: ATOMSocketBase(_id: Literal[0, 1, 2], port: list | tuple, relay: int = 23)

    Initializes the ATOM Socket.

    - ``_id``: Serial ID, not actually used by this base.
    - ``port``: UART pin numbers.
    - ``relay``: The relay pin number.
    
Methods
-------

.. method:: set_relay(state: bool) -> None

    Sets the state of the ATOM Socket's relay.

    - ``state``: The desired state of the relay, True = ON, False = OFF.

.. method:: get_data(timeout=3000) -> tuple

    Retrieves data from the ATOM Socket.

    - ``timeout``: Function timeout period.

    Returns the ATOM Socket data: Tuple (Voltage (V), Current (A), Power (W), Total Energy (KWh)), or None if timeout occurs.

.. method:: get_voltage() -> float

    Retrieves the voltage measurement from the ATOM Socket.

.. method:: get_current() -> float

    Retrieves the current measurement from the ATOM Socket.

.. method:: get_power() -> float

    Retrieves the power measurement from the ATOM Socket.

.. method:: get_pf() -> int

    Retrieves the power factor from the ATOM Socket.

.. method:: get_inspecting_power() -> float

    Calculates the inspecting power of the ATOM Socket.

.. method:: get_power_factor() -> float

    Calculates the power factor of the ATOM Socket.

.. method:: get_kwh() -> float

    Retrieves the accumulated energy measurement in KWh from the ATOM Socket.

.. method:: stop_receive_data() -> None

    Stops receiving data from the ATOM Socket.

.. method:: receive_none_block(receive_callback) -> None

    Receives data from the ATOM Socket in non-blocking mode.

    - ``receive_callback``: Callback function to handle the received data.
