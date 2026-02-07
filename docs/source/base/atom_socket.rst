Atom Socket Base
=================

.. include:: ../refs/base.atom_socket.ref

The `ATOMSocketBase` class is a smart power socket integrated with the M5 ATOM controller. It features a built-in HLW8032 high-precision power measurement IC, enabling it to measure the voltage, current, power, and energy of the load. Additionally, it can function as a smart socket to control the power state of the load, making it suitable for applications in smart homes, industrial control, and energy management.

Supports the following products:

|ATOMSocketBase|


Micropython Example:

    .. literalinclude:: ../../../examples/base/atom_socket/atomlite_socket_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |atomlite_socket_example.m5f2|


class ATOMSocketBase
--------------------

Constructors
------------

.. class:: ATOMSocketBase(_id: Literal[0, 1, 2], port: list | tuple, relay: int = 23)

    Initializes the ATOM Socket.

    - ``_id``: Serial ID, not actually used by this base.
    - ``port``: UART pin numbers.
    - ``relay``: The relay pin number.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ATOMSocketBase.set_relay(state: bool) -> None

    Sets the state of the ATOM Socket's relay.

    - ``state``: The desired state of the relay, True = ON, False = OFF.

    UIFLOW2:

        |set_relay.png|


.. method:: ATOMSocketBase.get_data(timeout=3000) -> tuple

    Retrieves data from the ATOM Socket.

    - ``timeout``: Function timeout period.

    Returns the ATOM Socket data: Tuple (Voltage (V), Current (A), Power (W), Total Energy (KWh)), or None if timeout occurs.

    UIFLOW2:

        |get_data.png|


.. method:: ATOMSocketBase.get_voltage() -> float

    Retrieves the voltage measurement from the ATOM Socket.

    UIFLOW2:

        |get_voltage.png|


.. method:: ATOMSocketBase.get_current() -> float

    Retrieves the current measurement from the ATOM Socket.

    UIFLOW2:

        |get_current.png|


.. method:: ATOMSocketBase.get_power() -> float

    Retrieves the power measurement from the ATOM Socket.

    UIFLOW2:

        |get_power.png|


.. method:: ATOMSocketBase.get_pf() -> int

    Retrieves the power factor from the ATOM Socket.

    UIFLOW2:

        |get_pf.png|


.. method:: ATOMSocketBase.get_inspecting_power() -> float

    Calculates the inspecting power of the ATOM Socket.

    UIFLOW2:

        |get_inspecting_power.png|


.. method:: ATOMSocketBase.get_power_factor() -> float

    Calculates the power factor of the ATOM Socket.

    UIFLOW2:

        |get_power_factor.png|


.. method:: ATOMSocketBase.get_kwh() -> float

    Retrieves the accumulated energy measurement in KWh from the ATOM Socket.

    UIFLOW2:

        |get_kwh.png|


.. method:: ATOMSocketBase.stop_receive_data() -> None

    Stops receiving data from the ATOM Socket.

    UIFLOW2:

        |stop_receive_data.png|


.. method:: ATOMSocketBase.receive_none_block(receive_callback) -> None

    Receives data from the ATOM Socket in non-blocking mode.

    - ``receive_callback``: Callback function to handle the received data.

    UIFLOW2:

        |receive_none_block.png|
