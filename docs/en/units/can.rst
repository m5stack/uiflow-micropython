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


CANUnit class inherits CAN class, See :ref:`hardware.CAN <hardware.CAN>` for more details.
