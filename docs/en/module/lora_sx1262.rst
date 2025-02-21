LoRa868 v1.2 Module 
============================

.. sku: 

.. include:: ../refs/module.lora_sx1262.ref

The LoRa868 v1.2 Module is part of the M5Stack stackable module series. It is a LoRa communication module that operates at a 900MHz frequency and utilizes the SX1262 chip solution.

Support the following products:

    |LoRa868Module v1.2|


UiFlow2 Example 
--------------------------

.. note:: Before using the following examples, please check the DIP switches on the module to ensure that the pins used in the example match the DIP switch positions. For specific configurations, please refer to the product manual page. The SPI configuration has been implemented internally, so users do not need to worry about it.

Sender
^^^^^^^^^^^^^^^^^^^^^^^^

Open the |cores3_lora_sx1262_tx_example.m5f2| project in UiFlow2.

This example sends data every second.

UiFlow2 Code Block:

    |cores3_lora_sx1262_tx_example.png|

Example output:

    None

Receiver
^^^^^^^^^^^^^^^^^^^^^^^^

Open the |cores3_lora_sx1262_rx_example.m5f2| project in UiFlow2.

This example receives and displays data.

UiFlow2 Code Block:

    |cores3_lora_sx1262_rx_example.png|

Example output:

    None

MicroPython Example 
--------------------------

.. note:: Before using the following examples, please check the DIP switches on the module to ensure that the pins used in the example match the DIP switch positions. For specific configurations, please refer to the product manual page. The SPI configuration has been implemented internally, so users do not need to worry about it.

Sender
^^^^^^^^^^^^^^^^^^^^^^^^

This example sends data every second.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/lora_sx1262/cores3_lora_sx1262_tx_example.py
        :language: python
        :linenos:

Example output:

    None

Receiver
^^^^^^^^^^^^^^^^^^^^^^^^

This example receives and displays data.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/lora_sx1262/cores3_lora_sx1262_rx_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
--------------------------


class LoRaSx1262Module  
^^^^^^^^^^^^^^^^^^^^^^^^
 
.. class:: module.lora_sx1262.LoRaSx1262Module(pin_rst = 5, \
                            pin_cs = 1, \
                            pin_irq = 10, \  
                            pin_busy = 2, \
                            freq_khz = 868000, \
                            bw = "250", \
                            sf = 8, \
                            coding_rate = 8, \
                            reamble_len = 12, \
                            syncword = 0x12, \
                            output_power = 10)

    Create an LoRaSx1262Module object.

    :param int timer_id: The Timer ID. Range: 0~3. Default is 0.
    :param int pin_rst: (RST) Reset pin number.
    :param int pin_cs: (NSS) Chip select pin number.
    :param int pin_irq: (IRQ) Interrupt pin number.
    :param int pin_busy: (BUSY) Busy pin number.
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
    :param int sf: Spreading factor, range from 7 to 12. Higher spreading factors allow reception of weaker signals but with slower data rates.
    :param int coding_rate: Forward Error Correction (FEC) coding rate expressed as 4/N, with a range from 5 to 8.
    :param int preamble_len: Length of the preamble sequence in symbols, range from 0 to 255.
    :param int syncword: Sync word to mark the start of the data frame, default is 0x12.
    :param int output_power: Output power in dBm, range from -9 to 22. 

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import LoRaSx1262Module

            lora868v12_0 = LoRaSx1262Module(5, 1, 10, 2, 868000, '250', 8, 8, 12, 0x12, 10)

    .. method:: set_irq_callback(callback)
        
        Set the interrupt callback function to be executed on IRQ.
        
        :param callback: The callback function to be invoked when the interrupt is triggered.
                          The callback should not take any arguments and should return nothing.
        
        Call `start_recv()` to begin receiving data.

        UiFlow2 Code Block:

            |set_irq_callback.png|

        MicroPython Code Block:

            .. code-block:: python

                lora868v12_0.set_irq_callback()

    .. method:: start_recv()
        
        Start receive data.

        This method initiates the process to begin receiving data.

        UiFlow2 Code Block:

            |start_recv.png|

        MicroPython Code Block:

            .. code-block:: python

                lora868v12_0.start_recv()

    .. method:: recv(self, timeout_ms, rx_length, rx_packet) 
        
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

                data = lora868v12_0.recv()

    .. method:: send(buf, tx_at_ms=None) 

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

                lora868v12_0.send()

    .. method:: standby()

        Set module to standby mode.

        Puts the LoRa module into standby mode, consuming less power.

        UiFlow2 Code Block:

            |standby.png|

        MicroPython Code Block:

            .. code-block:: python

                lora868v12_0.standby()

    .. method:: sleep()

        Put the module to sleep mode.

        Reduces the power consumption by putting the module into deep sleep mode.

        UiFlow2 Code Block:

            |sleep.png|

        MicroPython Code Block:

            .. code-block:: python

                lora868v12_0.sleep()

    .. method:: irq_triggered()  

        Check IRQ trigger.

        :returns: Returns `True` if an interrupt service routine (ISR) has been triggered since the last send or receive started.
        :rtype: bool

        UiFlow2 Code Block:

            |irq_triggered.png|

        MicroPython Code Block:

            .. code-block:: python

                lora868v12_0.irq_triggered()

class RxPacket   
^^^^^^^^^^^^^^^^^^^^^^^^

.. class:: lora.RxPacket()

    Create an RxPacket object. 

    .. method:: decode()

        Decode the received data.

    .. method:: ticks_ms

        Timestamp of when the data was received.

    .. method:: rssi

        Received signal strength (units: dBm).

    .. method:: snr

        Signal-to-noise ratio (units: dB * 4). 

    .. method:: valid_crc

        CRC validity check.