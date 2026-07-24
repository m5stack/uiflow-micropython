LoRa
====

.. include:: ../refs/hardware.lora.ref

LoRa is used to control the built-in long-range wireless communication module inside the host device. Below is the detailed LoRa support for the host:

.. table::
    :widths: auto
    :align: center

    +-----------------+---------+
    | Controllers     | LoRa    |
    +=================+=========+
    | UnitC6L         | |S|     |
    +-----------------+---------+
    | Nesso N1        | |S|     |
    +-----------------+---------+
    | PaperMono       | |S|     |
    +-----------------+---------+

.. |S| unicode:: U+2714

On supported controllers, ``LoRa`` automatically selects the board-specific
SPI bus and the default CS, BUSY, and IRQ pins. PaperMono also enables the
built-in LoRa module automatically during initialization. The CS, BUSY, and
IRQ pins can still be overridden with constructor arguments when required.

UiFlow2 Example
---------------

Sender
^^^^^^

Open the |unit_c6l_tx_example.m5f2| project in UiFlow2.

Open the |nesso_n1_sender_example.m5f2| project in UiFlow2.

This example sends data every second.

UiFlow2 Code Block:

    |unit_c6l_tx_example.png|

Example output:

    None

Receiver
^^^^^^^^

Open the |unit_c6l_rx_example.m5f2| project in UiFlow2.

Open the |nesso_n1_receiver_example.m5f2| project in UiFlow2.

This example receives and displays data.

UiFlow2 Code Block:

    |unit_c6l_rx_example.png|

Example output:

    None

MicroPython Example
-------------------

Sender
^^^^^^

This example sends data every second.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/hardware/lora/unit_c6l_tx_example.py
        :language: python
        :linenos:

Example output:

    None

Receiver
^^^^^^^^

This example receives and displays data.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/hardware/lora/unit_c6l_rx_example.py
        :language: python
        :linenos:

Example output:

    None

Important: IRQ when using interrupt receive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

   When receiving data with the interrupt method (``set_irq_callback`` and
   ``start_recv()``), the firmware automatically clears the LoRa IRQ flag
   after interrupt handling.

   In this case, polling ``irq_triggered()`` may always return ``False``
   because the flag has already been cleared. This is not a receive failure.

   Please use synchronous receive mode (``recv()``) for testing.


**API**
-------

class LoRa
^^^^^^^^^^

.. class:: hardware.LoRa(pin_rst=-1, pin_cs=None, pin_irq=None, pin_busy=None, \
                        freq_khz=868000, bw="250", sf=8, coding_rate=8, \
                        preamble_len=12, syncword=0x12, output_power=10)

    Create an LoRa object.

    :param int pin_rst: Reserved for compatibility. The current driver does not use a reset pin.
    :param int pin_cs: Chip-select pin. ``None`` selects the board-specific default.
    :param int pin_irq: Interrupt pin. ``None`` selects the board-specific default.
    :param int pin_busy: Busy pin. ``None`` selects the board-specific default.
    :param int freq_khz: LoRa RF frequency in KHz, with a range of 850000 KHz to 930000 KHz.
    :param str bw: Bandwidth, options include:

        - ``"7.8"``: 7.8 KHz
        - ``"10.4"``: 10.4 KHz
        - ``"15.6"``: 15.6 KHz
        - ``"20.8"``: 20.8 KHz
        - ``"31.25"``: 31.25 KHz
        - ``"41.7"``: 41.7 KHz
        - ``"62.5"``: 62.5 KHz
        - ``"125"``: 125 KHz
        - ``"250"``: 250 KHz
        - ``"500"``: 500 KHz
    :param int sf: Spreading factor, range from 6 to 12. Higher spreading factors allow reception of weaker signals but with slower data rates.
    :param int coding_rate: Forward Error Correction (FEC) coding rate expressed as 4/N, with a range from 5 to 8.
    :param int preamble_len: Length of the preamble sequence in symbols, range from 5 to 255.
    :param int syncword: Sync word to mark the start of the data frame, default is 0x12.
    :param int output_power: Output power in dBm, range from -9 to 22.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hardware import LoRa

            lora_0 = LoRa(
                freq_khz=868000,
                bw="250",
                sf=8,
                coding_rate=8,
                preamble_len=12,
                syncword=0x12,
                output_power=10,
            )

    .. method:: set_freq(freq_khz)

        Set frequency in kHz.

        :param int freq_khz: Frequency in kHz (850000 ~ 930000), default is 868000.

        UiFlow2 Code Block:

            |set_freq.png|

        MicroPython Code Block:

            .. code-block:: python

                lora_0.set_freq(freq_khz)

    .. method:: set_sf(sf)

        Set spreading factor (SF).

        :param int sf: Spreading factor (6 ~ 12)

        UiFlow2 Code Block:

            |set_sf.png|

        MicroPython Code Block:

            .. code-block:: python

                lora_0.set_sf(sf)

    .. method:: set_bw(bw)

        Set bandwidth.

        :param str bw: Bandwidth in kHz as string. Must be one of:
                       '7.8', '10.4', '15.6', '20.8', '31.25', '41.7',
                       '62.5', '125', '250', '500'.

        UiFlow2 Code Block:

            |set_bw.png|

        MicroPython Code Block:

            .. code-block:: python

                lora_0.set_bw(bw)

    .. method:: set_coding_rate(coding_rate)

        Set coding rate.

        :param int coding_rate: Coding rate (5 ~ 8)

        UiFlow2 Code Block:

            |set_coding_rate.png|

        MicroPython Code Block:

            .. code-block:: python

                lora_0.set_coding_rate(coding_rate)

    .. method:: set_syncword(syncword)

        Set syncword.

        :param int syncword: Sync word (1 ~ 0xFF)

        UiFlow2 Code Block:

            |set_syncword.png|

        MicroPython Code Block:

            .. code-block:: python

                lora_0.set_syncword(syncword)

    .. method:: set_preamble_len(preamble_len)

        Set preamble length.

        :param int preamble_len: Preamble length, range: 5~255.

        UiFlow2 Code Block:

            |set_preamble_len.png|

        MicroPython Code Block:

            .. code-block:: python

                lora_0.set_preamble_len(preamble_len)

    .. method:: set_output_power(output_power)

        Set output power in dBm.

        :param int output_power: Output power in dBm (-9 ~ 22)

        UiFlow2 Code Block:

            |set_output_power.png|

        MicroPython Code Block:

            .. code-block:: python

                lora_0.set_output_power(output_power)

    .. method:: set_irq_callback(callback)

        Set the interrupt callback function to be executed on IRQ.

        :param callback: The callback function to be invoked when the interrupt is triggered.
                          The callback receives the result of polling the receive operation.
                          For a valid received packet, the result is an ``RxPacket``.

        Call ``start_recv()`` to begin receiving data.

        UiFlow2 Code Block:

            |set_irq_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                def lora_receive_event(received_data):
                    print(received_data)

                lora_0.set_irq_callback(lora_receive_event)
                lora_0.start_recv()

    .. method:: start_recv()

        Start receive data.

        This method initiates the process to begin receiving data.

        UiFlow2 Code Block:

            |start_recv.png|

        MicroPython Code Block:

            .. code-block:: python

                lora_0.start_recv()

    .. method:: recv(timeout_ms=None, rx_length=0xFF, rx_packet=None)

        Receive data.

        :param int timeout_ms: Timeout in milliseconds (optional). Default is None.
        :param int rx_length: Length of the data to be read. Default is 0xFF.
        :param RxPacket rx_packet: An instance of `RxPacket` (optional) to reuse.
        :returns: Received packet instance
        :rtype: RxPacket

        Attempt to receive a LoRa packet. Returns `None` if timeout occurs, or returns the received packet instance.

        UiFlow2 Code Block:

            |recv.png|

        MicroPython Code Block:

            .. code-block:: python

                data = lora_0.recv()

    .. method:: send(packet, tx_at_ms=None)

        Send data.

        :param str | list | tuple | int | bytearray packet: The data to be sent.
        :param int tx_at_ms: The timestamp in milliseconds when to send the data (optional). Default is None.
        :returns: Returns a timestamp (result of `time.ticks_ms()`) indicating when the data packet was sent.
        :rtype: int

        Send a data packet and return the timestamp after the packet is sent.

        UiFlow2 Code Block:

            |send.png|

        MicroPython Code Block:

            .. code-block:: python

                lora_0.send("Hello LoRa")

    .. method:: standby()

        Set module to standby mode.

        Puts the LoRa module into standby mode, consuming less power.

        UiFlow2 Code Block:

            |standby.png|

        MicroPython Code Block:

            .. code-block:: python

                lora_0.standby()

    .. method:: sleep()

        Put the module to sleep mode.

        Reduces the power consumption by putting the module into deep sleep mode.

        UiFlow2 Code Block:

            |sleep.png|

        MicroPython Code Block:

            .. code-block:: python

                lora_0.sleep()

    .. method:: irq_triggered()

        Check IRQ trigger.

        :returns: Returns ``True`` if an interrupt service routine (ISR) has been
                  triggered since the last send or receive started. In **interrupt
                  receive** mode the IRQ is usually cleared inside the driver when
                  the callback runs, so this method may stay ``False``. Use
                  synchronous ``recv()`` to test reception (see the note above).
        :rtype: bool

        UiFlow2 Code Block:

            |irq_triggered.png|

        MicroPython Code Block:

            .. code-block:: python

                lora_0.irq_triggered()

Refer to :ref:`lora_rxpacket` for more details about RxPacket.
