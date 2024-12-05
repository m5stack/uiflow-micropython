.. _unit.CANUnit:

CAN Unit
========

.. include:: ../refs/unit.can.ref

The following products are supported:

    ================== ==================
    |CAN Unit|         |MiniCAN Unit|
    ================== ==================


Micropython TX Example:

    .. literalinclude:: ../../../examples/unit/can/stickc_plus2_can_tx_example.py
        :language: python
        :linenos:


Micropython RX Example:

    .. literalinclude:: ../../../examples/unit/can/dial_can_rx_example.py
        :language: python
        :linenos:


UIFLOW2 TX Example:

    |tx_example.png|


UIFLOW2 RX Example:

    |rx_example.png|


.. only:: builder_html

    |stickc_plus2_can_tx_example.m5f2|

    |dial_can_rx_example.m5f2|


class CANUnit
-------------

Constructors
------------

.. class:: CANUnit(port, mode, baudrate=125000)

    Create an CANUnit object.

    parameter is:

        - ``port`` is the pins number of the port
        - ``mode`` is one of:  NORMAL, NO_ACKNOWLEDGE, LISTEN_ONLY
        - ``baudrate`` is the baudrate of CANUnit.

    UIFLOW2:

        |init.png|

.. class:: CANUnit(tx, rx, mode, prescaler=32, sjw=3, bs1=15, bs2=4, triple_sampling=False)
    :no-index:
    
    Initialise the CAN bus with the given parameters:

        - ``tx`` is the pin to use for transmitting data
        - ``rx`` is the pin to use for receiving data
        - ``mode`` is one of:  NORMAL, NO_ACKNOWLEDGE, LISTEN_ONLY
        - ``prescaler`` is the value by which the CAN input clock is divided to generate the
          nominal bit time quanta. The prescaler can be a value between 1 and 1024 inclusive
          for classic CAN.
        - ``sjw`` is the resynchronisation jump width in units of time quanta for nominal bits;
          it can be a value between 1 and 4 inclusive for classic CAN.
        - ``bs1`` defines the location of the sample point in units of the time quanta for nominal bits;
          it can be a value between 1 and 16 inclusive for classic CAN.
        - ``bs2`` defines the location of the transmit point in units of the time quanta for nominal bits;
          it can be a value between 1 and 8 inclusive for classic CAN.
        - ``triple_sampling`` is Enables triple sampling when the TWAI controller samples a bit

    UIFLOW2:

        |init1.png|

CANUnit class inherits CAN class, See :ref:`hardware.CAN <hardware.CAN>` for more details.
