CAN Unit
========

.. include:: ../refs/unit.can.ref

The following products are supported:

    ================== ==================
    |CAN Unit|         |MiniCAN Unit|
    ================== ==================


Micropython Example::

    import M5
    from M5 import *
    from unit import CANUnit

    can = CANUnit((15, 13), CANUnit.NORMAL, 125000)


UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

    |env_cores3_example.m5f2|


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

        |init.svg|


CANUnit class inherits CAN class, See :ref:`hardware.CAN <hardware.CAN>` for more details.
