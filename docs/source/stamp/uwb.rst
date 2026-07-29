Stamp UWB
=========

.. include:: ../refs/stamp.uwb.ref

Stamp UWB is a QM33120 ultra-wideband transceiver. The ``StampUWB`` class
selects the pin mapping for the current Stamp host and provides the PHY, frame,
status, and timestamp operations. The PHY channel is fixed to channel 9, and
only one active
``StampUWB`` instance is supported.

Support the following products:

    |Stamp UWB|

Supported hosts:

- StampS3Mini
- StampC6
- StampC5

DS-TWR Ranging Principle
------------------------

The simple examples use a three-message double-sided two-way ranging exchange:

1. The Tag transmits a Poll frame and records the Poll TX timestamp ``T1``.
   The Anchor receives it and records the Poll RX timestamp ``T2``.
2. The Anchor transmits a Response frame and records the Response TX timestamp
   ``T3``. The Tag receives it and records the Response RX timestamp ``T4``.
3. The Tag schedules a delayed Final frame, records its TX timestamp ``T5``,
   and includes ``T1``, ``T4``, and ``T5`` in the frame. The Anchor receives
   the Final frame and records timestamp ``T6``.

The examples use the following compact frame format. Multi-byte values are
little-endian, and the sequence number associates the three frames:

- Poll: ``[0x01, sequence]``
- Response: ``[0x02, sequence]``
- Final: ``[0x03, sequence, T1, T4, T5]``, where each timestamp occupies the
  low 32 bits of a device timestamp

The Anchor calculates the time of flight while handling 32-bit timestamp
wraparound:

.. code-block:: text

    round_a = T4 - T1
    round_b = T6 - T3
    delay_a = T5 - T4
    delay_b = T3 - T2
    tof = (round_a * round_b - delay_a * delay_b) \
          / (round_a + round_b + delay_a + delay_b)
    distance = abs(tof * DWT_TIME_UNITS * 299702547)

``DWT_TIME_UNITS`` is ``1 / (499200000 * 128)`` seconds. The Anchor prints the
calculated distance locally. This simplified protocol does not send the
distance back to the Tag.

UiFlow2 Example
---------------

Simple DS-TWR Anchor
^^^^^^^^^^^^^^^^^^^^

Open the |stampc5_uwb_simple_anchor.m5f2| project in UiFlow2.

The anchor receives Poll and Final frames, calculates the distance locally,
and prints the non-negative ranging result.

UiFlow2 Code Block:

    |simple_anchor_example.png|

Simple DS-TWR Tag
^^^^^^^^^^^^^^^^^

Open the |stampc5_uwb_simple_tag.m5f2| project in UiFlow2.

The tag sends Poll, waits for Response, and sends a delayed Final frame. This
minimal protocol does not return the calculated distance to the tag.

UiFlow2 Code Block:

    |simple_tag_example.png|

MicroPython Example
-------------------

Simple DS-TWR Anchor
^^^^^^^^^^^^^^^^^^^^

The anchor receives Poll and Final frames, calculates the distance locally,
and prints the non-negative ranging result.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/stamp/uwb/stampc5_uwb_simple_anchor.py
        :language: python
        :linenos:

Simple DS-TWR Tag
^^^^^^^^^^^^^^^^^

The tag sends Poll, waits for Response, and sends a delayed Final frame. This
minimal protocol does not return the calculated distance to the tag.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/stamp/uwb/stampc5_uwb_simple_tag.py
        :language: python
        :linenos:

**API**
-------

class StampUWB
--------------

Constructors
------------

.. class:: StampUWB()

    Create a Stamp UWB object using the pin mapping of the current Stamp host.
    Only one active instance is supported.

    :raises OSError: If another instance is active, SPI initialization fails,
        or the UWB device cannot be probed or initialized.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from stamp import StampUWB

            stamp_uwb_0 = StampUWB()

Constants
---------

The option block supplies the PHY, TX/RX mode, and status-mask constants used
by the methods below.

UiFlow2 Code Block:

    |constant_option.png|

.. data:: uwb.SFD_DW_8

    Decawave 8-symbol SFD used by :meth:`StampUWB.configure`.

.. data:: uwb.BR_6M8

    6.8 Mbit/s PHY data rate used by :meth:`StampUWB.configure`.

.. data:: uwb.PHR_STD

    Standard PHY header mode used by :meth:`StampUWB.configure`.

.. data:: uwb.PHR_RATE_STD

    Standard PHY header rate used by :meth:`StampUWB.configure`.

.. data:: uwb.TX_IMMEDIATE

    Start transmission immediately.

.. data:: uwb.TX_DELAYED

    Start transmission at the time set by
    :meth:`StampUWB.set_delayed_trx_time`.

.. data:: uwb.RESPONSE_EXPECTED

    Automatically enable the receiver after transmission. Combine this flag
    with a TX start mode.

.. data:: uwb.RX_IMMEDIATE

    Enable the receiver immediately.

.. data:: uwb.RX_DELAYED

    Enable the receiver at the configured delayed RX time.

.. data:: uwb.IDLE_ON_DELAY_ERROR

    Return to idle if a delayed RX operation is already too late.

.. data:: uwb.STATUS_TX_DONE

    Transmission-complete status bit.

.. data:: uwb.STATUS_RX_GOOD

    Good-frame-received status bit.

.. data:: uwb.STATUS_RX_TIMEOUT

    Combined receive-timeout status mask.

.. data:: uwb.STATUS_RX_ERROR

    Combined receive-error status mask.

.. data:: uwb.STATUS_RX_ALL

    Combined mask containing good-frame, receive-timeout, and receive-error
    status bits.

Methods
-------

.. method:: StampUWB.configure(preamble_length=128, pac=8, tx_code=9, rx_code=9, sfd_type=uwb.SFD_DW_8, data_rate=uwb.BR_6M8, phr_mode=uwb.PHR_STD, phr_rate=uwb.PHR_RATE_STD, sfd_timeout=129)

    Configure the channel 9 UWB PHY.

    :param int preamble_length: Preamble length in symbols. Allowed values are ``32``, ``64``, ``72``, ``128``, ``256``, ``512``, ``1024``, ``1536``, ``2048``, and ``4096``. Default is ``128``.
    :param int pac: Preamble acquisition chunk size. Allowed values are ``4``, ``8``, ``16``, and ``32``. Default is ``8``.
    :param int tx_code: TX preamble code, range ``9`` to ``12``. Default is ``9``.
    :param int rx_code: RX preamble code, range ``9`` to ``12``. Default is ``9``.
    :param int sfd_type: SFD type. Use ``uwb.SFD_DW_8``.
    :param int data_rate: PHY data rate. Use ``uwb.BR_6M8``.
    :param int phr_mode: PHR mode. Use ``uwb.PHR_STD``.
    :param int phr_rate: PHR rate. Use ``uwb.PHR_RATE_STD``.
    :param int sfd_timeout: SFD timeout in symbols, range ``0`` to ``65535``. Default is ``129``.

    UiFlow2 Code Block:

        |configure.png|

    MicroPython Code Block:

        .. code-block:: python

            import uwb

            stamp_uwb_0.configure(
                preamble_length=128,
                pac=8,
                tx_code=9,
                rx_code=9,
                sfd_type=uwb.SFD_DW_8,
                data_rate=uwb.BR_6M8,
                phr_mode=uwb.PHR_STD,
                phr_rate=uwb.PHR_RATE_STD,
                sfd_timeout=129,
            )

.. method:: StampUWB.configure_tx_rf(pg_delay=0x34, tx_power=0xFEFEFEFE, pg_count=0)

    Configure the channel 9 transmitter RF settings.

    :param int pg_delay: Pulse generator delay, range ``0x00`` to ``0xFF``. Default is ``0x34``.
    :param int tx_power: 32-bit TX power value, range ``0x00000000`` to ``0xFFFFFFFF``. Default is ``0xFEFEFEFE``.
    :param int pg_count: Pulse generator count, range ``0x00`` to ``0xFF``. Default is ``0``.

    UiFlow2 Code Block:

        |configure_tx_rf.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.configure_tx_rf(0x34, 0xFEFEFEFE, 0)

.. method:: StampUWB.set_antenna_delay(tx=16385, rx=16385)

    Set the TX and RX antenna delays.

    :param int tx: TX antenna delay in device time units, range ``0`` to ``65535``. Default is ``16385``.
    :param int rx: RX antenna delay in device time units, range ``0`` to ``65535``. Default is ``16385``.

    UiFlow2 Code Block:

        |set_antenna_delay.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.set_antenna_delay(tx=16385, rx=16385)

.. method:: StampUWB.set_lna_pa(lna=True, pa=True)

    Enable or disable the low-noise amplifier and power amplifier controls.

    :param bool lna: Enable the LNA. Default is ``True``.
    :param bool pa: Enable the PA. Default is ``True``.

    UiFlow2 Code Block:

        |set_lna_pa.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.set_lna_pa(lna=True, pa=True)

.. method:: StampUWB.set_rx_after_tx_delay(delay_uus=0)

    Set the delay from TX completion to automatic RX enable.

    :param int delay_uus: Delay in UWB microseconds, range ``0`` to ``4294967295``. Default is ``0``.

    UiFlow2 Code Block:

        |set_rx_after_tx_delay.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.set_rx_after_tx_delay(0)

.. method:: StampUWB.set_rx_timeout(timeout_uus=30000)

    Set the RX frame timeout. A value of ``0`` disables the timeout.

    :param int timeout_uus: Timeout in UWB microseconds, range ``0`` to ``4294967295``. Default is ``30000``.

    UiFlow2 Code Block:

        |set_rx_timeout.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.set_rx_timeout(30000)

.. method:: StampUWB.set_preamble_timeout(timeout=0)

    Set the preamble detection timeout. A value of ``0`` disables the timeout.

    :param int timeout: Timeout in PAC units, range ``0`` to ``65535``. Default is ``0``.

    UiFlow2 Code Block:

        |set_preamble_timeout.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.set_preamble_timeout(0)

.. method:: StampUWB.write_tx_frame(data, ranging=True)

    Write a payload to the TX buffer. Do not include the two-byte FCS.

    :param data: Bytes-like payload, range ``0`` to ``125`` bytes.
    :param bool ranging: Set the ranging bit in TX frame control. Default is ``True``.
    :raises ValueError: If the payload exceeds 125 bytes.
    :raises OSError: If the payload cannot be written to the TX buffer.

    UiFlow2 Code Block:

        |write_tx_frame.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.write_tx_frame(b"hello", ranging=True)

.. method:: StampUWB.set_delayed_trx_time(device_time)

    Set the delayed TX/RX device time.

    :param int device_time: Low 32 bits of the 40-bit device timestamp shifted right by 8, range ``0`` to ``4294967295``.

    UiFlow2 Code Block:

        |set_delayed_trx_time.png|

    MicroPython Code Block:

        .. code-block:: python

            delayed_time = (stamp_uwb_0.rx_timestamp() + 4500 * 63898) >> 8
            stamp_uwb_0.set_delayed_trx_time(delayed_time)

.. method:: StampUWB.start_tx(mode)

    Start an immediate or delayed transmission.

    :param int mode: TX mode composed from ``uwb.TX_IMMEDIATE`` or ``uwb.TX_DELAYED`` and optional ``uwb.RESPONSE_EXPECTED``.
    :raises OSError: If a delayed transmission time has already passed.

    UiFlow2 Code Block:

        |start_tx.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.start_tx(uwb.TX_IMMEDIATE | uwb.RESPONSE_EXPECTED)

.. method:: StampUWB.rx_enable(mode=uwb.RX_IMMEDIATE)

    Enable the receiver.

    :param int mode: Use ``uwb.RX_IMMEDIATE`` or ``uwb.RX_DELAYED``. Delayed RX can be combined with ``uwb.IDLE_ON_DELAY_ERROR``. Default is ``uwb.RX_IMMEDIATE``.
    :raises OSError: If the receiver cannot be enabled.

    UiFlow2 Code Block:

        |rx_enable.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.rx_enable(uwb.RX_IMMEDIATE)

.. method:: StampUWB.wait_status(mask, timeout_ms=-1)

    Wait until any requested system status bit is set.

    :param int mask: Status mask composed from ``uwb.STATUS_*`` constants, range ``0x00000000`` to ``0xFFFFFFFF``.
    :param int timeout_ms: Software timeout in milliseconds, range ``-1`` to ``1073741823``. ``-1`` waits indefinitely. Default is ``-1``.
    :returns: Raw 32-bit system status value.
    :rtype: int
    :raises OSError: ``ETIMEDOUT`` if no requested status bit is set before the
        software timeout.

    UiFlow2 Code Block:

        |wait_status.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.wait_status(uwb.STATUS_RX_ALL, 50)

.. method:: StampUWB.read_status()

    Read the low 32 bits of the system status register.

    :returns: Raw 32-bit system status value.
    :rtype: int

    UiFlow2 Code Block:

        |read_status.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.read_status()

.. method:: StampUWB.clear_status(mask)

    Clear selected system status bits.

    :param int mask: Status mask, range ``0x00000000`` to ``0xFFFFFFFF``.

    UiFlow2 Code Block:

        |clear_status.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.clear_status(uwb.STATUS_TX_DONE)

.. method:: StampUWB.force_trx_off()

    Force the transmitter and receiver to the idle state.

    UiFlow2 Code Block:

        |force_trx_off.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.force_trx_off()

.. method:: StampUWB.frame_length()

    Get the last received frame length including the two-byte FCS.

    :returns: Received frame length in bytes, range ``2`` to ``127``.
    :rtype: int

    UiFlow2 Code Block:

        |frame_length.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.frame_length()

.. method:: StampUWB.read_rx_frame()

    Read the last received payload without the two-byte FCS.

    :returns: Received payload, range ``0`` to ``125`` bytes.
    :rtype: bytes
    :raises OSError: If the received frame length is outside the valid range.

    UiFlow2 Code Block:

        |read_rx_frame.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.read_rx_frame()

.. method:: StampUWB.tx_timestamp()

    Read the last TX timestamp.

    :returns: Full 40-bit TX timestamp in device time units.
    :rtype: int

    UiFlow2 Code Block:

        |tx_timestamp.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.tx_timestamp()

.. method:: StampUWB.rx_timestamp()

    Read the last RX timestamp.

    :returns: Full 40-bit RX timestamp in device time units.
    :rtype: int

    UiFlow2 Code Block:

        |rx_timestamp.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.rx_timestamp()

.. method:: StampUWB.system_timestamp()

    Read the current UWB system timestamp.

    :returns: Full 40-bit system timestamp in device time units.
    :rtype: int

    UiFlow2 Code Block:

        |system_timestamp.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.system_timestamp()

.. method:: StampUWB.reset()

    Reset, probe, and reinitialise the UWB device. Configure the PHY and RF
    settings again after reset.

    :raises OSError: If the device cannot be probed or initialized after reset.

    UiFlow2 Code Block:

        |reset.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.reset()
            stamp_uwb_0.configure(
                preamble_length=128,
                pac=8,
                tx_code=9,
                rx_code=9,
                sfd_type=uwb.SFD_DW_8,
                data_rate=uwb.BR_6M8,
                phr_mode=uwb.PHR_STD,
                phr_rate=uwb.PHR_RATE_STD,
                sfd_timeout=129,
            )
            stamp_uwb_0.configure_tx_rf(
                pg_delay=0x34, tx_power=0xFEFEFEFE, pg_count=0
            )

.. method:: StampUWB.wakeup()

    Pulse the WAKEUP pin to wake the UWB device.

    UiFlow2 Code Block:

        |wakeup.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.wakeup()

.. method:: StampUWB.deinit()

    Stop TX/RX and release the SPI and GPIO resources. This method is
    idempotent. After deinitialization, other methods raise ``OSError(ENODEV)``.

    UiFlow2 Code Block:

        |deinit.png|

    MicroPython Code Block:

        .. code-block:: python

            stamp_uwb_0.deinit()
