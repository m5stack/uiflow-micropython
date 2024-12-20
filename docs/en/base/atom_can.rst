ATOM CAN Base
==============

.. include:: ../refs/base.can.ref

The following products are supported:

    ================== ==================
    |Atom CAN|         |Atomic CAN Base|
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

class ATOMCANBase
-----------------

Constructors
------------

.. class:: ATOMCANBase(id, tx, rx, mode, baudrate)

    Create an ATOMCANBase object.

    parameter is:

        - ``id`` is the ID of the CAN bus
        - ``tx`` is the pin to use for transmitting data
        - ``rx`` is the pin to use for receiving data
        - ``mode`` is one of:  NORMAL, NO_ACKNOWLEDGE, LISTEN_ONLY
        - ``baudrate`` is the baudrate of ATOMCANBase

    UIFLOW2:

        |init.png|

.. class:: ATOMCANBase(id, tx, rx, mode, prescaler, sjw, bs1, bs2, triple_sampling=False)
    :no-index:
    
    Initialise the CAN bus with the given parameters:

        - ``id`` is the ID of the CAN bus
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

        |init_advanced.png|

ATOMCANBase class inherits CAN class, See :ref:`hardware.CAN <hardware.CAN>` for more details.
