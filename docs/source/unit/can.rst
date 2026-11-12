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

.. class:: CANUnit(id=0, port=None, mode=CANUnit.NORMAL, prescaler=0, sjw=0, bs1=0, bs2=0, triple_sampling=False, quantum_resolution_hz=0, baudrate=0, verbose=False)

    Create a CANUnit object. Supply ``port=(rx_pin, tx_pin)`` for the connected
    controller; the default ``None`` does not select pins automatically.

    :param int id: The hardware CAN controller ID.
    :param tuple port: The port pins in **(rx, tx)** order.
    :param int mode: CANUnit.NORMAL, CANUnit.NO_ACKNOWLEDGE, or CANUnit.LISTEN_ONLY.
    :param int prescaler: Nominal bit-time prescaler for manual timing.
    :param int sjw: Resynchronisation jump width in time quanta.
    :param int bs1: Time segment before the sample point, in time quanta.
    :param int bs2: Time segment after the sample point, in time quanta.
    :param bool triple_sampling: Enable triple sampling.
    :param int quantum_resolution_hz: Time-quanta clock frequency in Hz.
    :param int baudrate: Bus bitrate in bits per second. Use a nonzero value for automatic timing.
    :param bool verbose: Print the selected configuration.

    UiFlow2 Code Block:

        |init.png|
        |init1.png|

    MicroPython Code Block:

        .. code-block:: python

            from unit import CANUnit

            # Automatic timing, 125 kbit/s. Choose pins for your controller.
            can = CANUnit(id=0, port=(13, 14), mode=CANUnit.NORMAL, baudrate=125000)

    Alternatively, configure manual timing instead of setting ``baudrate``:

        .. code-block:: python

            can = CANUnit(
                id=0, port=(13, 14), mode=CANUnit.NORMAL,
                prescaler=128, sjw=3, bs1=16, bs2=8,
                triple_sampling=False,
            )

    .. note::

        CANUnit inherits CAN. See :class:`hardware.CAN <hardware.CAN>`
        for timing constraints and supported controller IDs on each target.
