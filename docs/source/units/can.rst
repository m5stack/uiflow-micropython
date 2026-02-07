.. _unit.CANUnit:

.. py:currentmodule:: unit

CANUnit
=======

.. include:: ../refs/unit.can.ref

The CAN Unit is used to communicate via the CAN bus.
The following products are supported:

    ================== ==================
    |CAN Unit|         |MiniCAN Unit|
    ================== ==================

UiFlow2 Example
---------------

TX Example
^^^^^^^^^^

Open the |stickc_plus2_can_tx_example.m5f2| project in UiFlow2.

This example demonstrates how to transmit data using CAN Unit.

Click the BtnA to change the data to be sent.

UiFlow2 Code Block:

    |tx_example.png|

Example output:

    None


RX Example
^^^^^^^^^^

Open the |dial_can_rx_example.m5f2| project in UiFlow2.

This example demonstrates how to receive data using CAN Unit.

UiFlow2 Code Block:

    |rx_example.png|


Example output:

    Screen will display the received CAN data.

MicroPython Example
-------------------

TX Example
^^^^^^^^^^

This example demonstrates how to transmit data using CAN Unit.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/can/stickc_plus2_can_tx_example.py
        :language: python
        :linenos:

Example output:

    None

RX Example
^^^^^^^^^^

This example demonstrates how to receive data using CAN Unit.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/can/dial_can_rx_example.py
        :language: python
        :linenos:

Example output:

    Screen will display the received CAN data.

API
---

CANUnit
^^^^^^^

.. class:: CANUnit(port, mode, baudrate=125000)

    Create a CANUnit object.

    :param int id: The CAN ID.
    :param tuple port: The port pins (tx, rx).
    :param int mode: One of CAN.NORMAL, CAN.NO_ACKNOWLEDGE, CAN.LISTEN_ONLY.
    :param int baudrate: The baudrate of CANUnit.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import CANUnit

            can = CANUnit(id=0, port=(13, 14), mode=CANUnit.NORMAL, baudrate=125000)

    .. note::

        CANUnit class inherits CAN class. See :class:`hardware.CAN <hardware.CAN>` for more details.


.. class:: CANUnit(tx, rx, mode, prescaler=32, sjw=3, bs1=15, bs2=4, triple_sampling=False)
    :no-index:

    Initialise the CAN bus with the given parameters.

    :param int id: The CAN ID.
    :param tuple port: The port pins (tx, rx).
    :param int mode: One of CAN.NORMAL, CAN.NO_ACKNOWLEDGE, CAN.LISTEN_ONLY.
    :param int prescaler: The value by which the CAN input clock is divided to generate the nominal bit time quanta. The prescaler can be a value between 1 and 1024 inclusive for classic CAN.
    :param int sjw: The resynchronisation jump width in units of time quanta for nominal bits; it can be a value between 1 and 4 inclusive for classic CAN.
    :param int bs1: Defines the location of the sample point in units of the time quanta for nominal bits; it can be a value between 1 and 16 inclusive for classic CAN.
    :param int bs2: Defines the location of the transmit point in units of the time quanta for nominal bits; it can be a value between 1 and 8 inclusive for classic CAN.
    :param bool triple_sampling: is Enables triple sampling when the TWAI controller samples a bit.

    UiFlow2 Code Block:

        |init1.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import CANUnit

            can = CANUnit(id=0, port=(13, 14), mode=CANUnit.NORMAL, prescaler=128, sjw=3, bs1=16, bs2=8, triple_sampling=False)

    .. note::

        CANUnit class inherits CAN class. See :class:`hardware.CAN <hardware.CAN>` for more details.
