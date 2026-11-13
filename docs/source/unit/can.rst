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

    :param int id: The hardware CAN controller ID; the current binding accepts only ``0``.
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

Methods
^^^^^^^

CANUnit and MiniCANUnit inherit the following methods from ``m5can.CAN``.
``MiniCANUnit`` is an alias of ``CANUnit``.

.. method:: CANUnit.init(mode, tx, rx, quanta_resolution_hz=2500000, brp=0, tseg_1=15, tseg_2=4, sjw=3, triple_sampling=False, baudrate=0)

    Start a deinitialized controller. Call ``deinit()`` first when it is active.
    This method uses separate ``tx``/``rx`` pins and ``baudrate`` in **kbit/s**.
    The constructor uses ``port=(rx, tx)`` and baudrate in **bits per second**.
    See :meth:`hardware.CAN.init` for native timing parameters.

    :returns: ``None``.

    Raises ``ValueError``: Unsupported automatic bitrate.

    Raises ``OSError``: Controller initialization fails.

.. method:: CANUnit.deinit()

    Stop the controller and release its driver.

    :returns: ``None``.

    Raises ``OSError``: Driver removal fails.

.. method:: CANUnit.restart()

    Stop and start an enabled controller with its existing configuration.
    A deinitialized controller stays disabled.

    :returns: ``None``.

    Raises ``OSError``: The controller cannot be started.

.. method:: CANUnit.state()

    :returns: ``STOPPED`` (0), ``BUS_OFF`` (4), ``RECOVERING`` (5), or ``RUNNING`` (6).
    :rtype: int

    Raises ``OSError``: Reading controller status fails.

.. method:: CANUnit.info([list])

    :param list list: Optional list of at least eight entries, updated in place.
        Omit this argument to allocate a list.
    :returns: ``[TEC, REC, 0, 0, 0, pending_tx, pending_rx, 0]`` while enabled.
        See :meth:`hardware.CAN.info` for behavior after deinitialization.

    Raises ``TypeError``: The supplied argument is not a list.

    Raises ``ValueError``: The supplied list has fewer than eight entries.

    Raises ``OSError``: Reading controller status fails.

.. method:: CANUnit.any(fifo)

    :param int fifo: Compatibility argument; use ``0``.
    :returns: ``True`` if a frame is waiting, otherwise ``False``.

    Raises ``OSError``: Reading controller status fails.

.. method:: CANUnit.send(data, id, *, timeout=0, rtr=False, extframe=False)

    :param data: Readable buffer of at most eight bytes, such as ``bytes`` or ``bytearray``.
    :param int id: Standard 11-bit identifier, or 29-bit identifier with ``extframe=True``.
    :param int timeout: TX queue wait in FreeRTOS ticks; standard UiFlow2 builds use 1 ms ticks.
    :param bool rtr: Send a remote request, using the buffer length as DLC.
    :param bool extframe: Use an extended identifier.
    :returns: ``None`` after queueing; receipt by another node is not confirmed.

    Raises ``TypeError``: ``data`` does not support the buffer protocol.

    Raises ``ValueError``: The buffer exceeds eight bytes.

    Raises ``OSError``: The driver rejects an argument, or queueing fails or times out.

.. method:: CANUnit.recv(fifo, list=None, *, timeout=5000)

    :param int fifo: Compatibility argument; use ``0``.
    :param list list: Optional reusable list with at least five entries; its
        fifth entry must be a writable byte-oriented memoryview backed by at least eight bytes.
    :param int timeout: RX wait in FreeRTOS ticks; standard UiFlow2 builds use 1 ms ticks.
    :returns: ``(id, extframe, rtr, 255, data)`` or the updated supplied list.
        Returns ``None`` on timeout or receive failure.

    Raises ``TypeError``: On receipt of a frame, the supplied list or memoryview has the wrong type.

    Raises ``ValueError``: On receipt of a frame, the list is too short or the memoryview has an invalid format.

    .. code-block:: python

        can.send(b"\x01\x02", 0x123, timeout=0)
        frame = can.recv(0, timeout=0)
        if frame is not None:
            identifier, extended, remote, fmi, payload = frame
            print(identifier, payload)

.. method:: CANUnit.setfilter(bank, mode, fifo, params, *, rtr=None, extframe=False)

    Compatibility placeholder: arguments are parsed but filters are not applied.
    The controller accepts all identifiers.

    :returns: ``None``.

.. method:: CANUnit.clearfilter(bank, extframe=False)

    Compatibility placeholder; it does not change the receive filter.
    ``bank`` is positional.

    :returns: ``None``.
