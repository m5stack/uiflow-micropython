LoRa868 v1.2 Module 
=====================================

.. include:: ../refs/module.lora_sx1262.ref

The LoRa868 v1.2 Module is part of the M5Stack stackable module series. It is a LoRa communication module that operates at a 900MHz frequency and utilizes the SX1262 chip solution.

Support the following products:

|Module LoRa868 v1.2|


Micropython Example 
----------------------------

.. note:: Before using the following examples, please check the DIP switches on the module to ensure that the pins used in the example match the DIP switch positions. For specific configurations, please refer to the product manual page. The SPI configuration has been implemented internally, so users do not need to worry about it.

Sender
++++++++++++++++++++++++++++
send data 

    .. literalinclude:: ../../../examples/module/lora_sx1262/cores3_lora_sx1262_tx_example.py
        :language: python
        :linenos:
        
Receiver
++++++++++++++++++++++++++++
receive data 

    .. literalinclude:: ../../../examples/module/lora_sx1262/cores3_lora_sx1262_rx_example.py
        :language: python
        :linenos:

UIFlow2.0 Example 
----------------------------

.. note:: Before using the following examples, please check the DIP switches on the module to ensure that the pins used in the example match the DIP switch positions. For specific configurations, please refer to the product manual page. The SPI configuration has been implemented internally, so users do not need to worry about it.

Sender
++++++++++++++++++++++++++++
send data 

    |cores3_lora_sx1262_tx_example.png|

.. only:: builder_html

    |cores3_lora_sx1262_tx_example.m5f2|


Receiver
++++++++++++++++++++++++++++
receive data 

    |cores3_lora_sx1262_rx_example.png|

.. only:: builder_html

    |cores3_lora_sx1262_rx_example.m5f2|


class LoRaSx1262Module  
------------------------------

Constructors
------------------------------

.. class:: LoRaSx1262Module(pin_rst: int = 5, \
                            pin_cs: int = 1, \
                            pin_irq: int = 10, \  
                            pin_busy: int = 2, \
                            freq_khz: int = 868000, \
                            bw: str = "250", \
                            sf: int = 8, \
                            coding_rate: int = 8, \
                            reamble_len: int = 12, \
                            syncword:int = 0x12, \
                            output_power: int = 10)

    :param int pin_rst: (RST) Reset pin number.
    :param int pin_cs: (NSS) Chip select pin number.
    :param int pin_irq: (IRQ) Interrupt pin number.
    :param int pin_busy: (BUSY) Busy pin number.
    :param int freq_khz: LoRa RF frequency in KHz, with a range of 850000 KHz to 930000 KHz.
    :param str bw: Bandwidth, options include:
        "7.8": 7.8 KHz
        "10.4": 10.4 KHz
        "15.6": 15.6 KHz
        "20.8": 20.8 KHz
        "31.25": 31.25 KHz
        "41.7": 41.7 KHz
        "62.5": 62.5 KHz
        "125": 125 KHz
        "250": 250 KHz
        "500": 500 KHz
    :param int sf: Spreading factor, range from 7 to 12. Higher spreading factors allow reception of weaker signals but with slower data rates.
    :param int coding_rate: Forward Error Correction (FEC) coding rate expressed as 4/N, with a range from 5 to 8.
    :param int preamble_len: Length of the preamble sequence in symbols, range from 0 to 255.
    :param syncword: Sync word to mark the start of the data frame, default is 0x12.
    :param int output_power: Output power in dBm, range from -9 to 22.

    - ``pin_rst``: (RST) Reset pin number.
    - ``pin_cs``: (NSS) Chip select pin number.
    - ``pin_irq``: (IRQ) Interrupt pin number.
    - ``pin_busy``: (BUSY) Busy pin number.
    - ``freq_khz``: LoRa RF frequency in KHz, with a range of 850000 KHz to 930000 KHz.
    - ``bw``: Bandwidth, options include:
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
    - ``sf``: Spreading factor, range from 7 to 12. Higher spreading factors allow reception of weaker signals but with slower data rates.
    - ``coding_rate``: Forward Error Correction (FEC) coding rate expressed as 4/N, with a range from 5 to 8.
    - ``preamble_len``: Length of the preamble sequence in symbols, range from 0 to 255.
    - ``syncword``: Sync word to mark the start of the data frame, default is 0x12.
    - ``int output_power``: Output power in dBm, range from -9 to 22.

    UIFLOW2:

        |init.png|

.. method:: set_irq_callback(callback)
    
    Set interrupt callback function.
    
    - ``callback``: The callback function to be executed when an interrupt occurs.
    
    **Note**: Call `start_recv()` to begin receiving data.

    UIFlow2.0

        |set_irq_callback.png|

.. method:: start_recv()
    
    Start receiving data.

    **Note**: This method initiates the process to begin receiving data. 

    UIFlow2.0

        |start_recv.png|

.. method:: recv(self, timeout_ms=None, rx_length=0xFF, rx_packet=None) -> RxPacket
    
    Receive data.

    Attempt to receive a LoRa packet. Returns `None` if timeout occurs, or returns the received packet instance.

    - ``timeout_ms``: Timeout in milliseconds (optional).
    - ``rx_length``: Length of the data to be read.
    - ``rx_packet``: An instance of `RxPacket` (optional) to reuse.

    Returns an `RxPacket` object containing the received data.

    **Example:**
    
    ::

        data = recv()
        data = recv(timeout_ms=1000)
        data = recv(timeout_ms=1000, rx_packet=data)

    - `data.decode()`: Decode the received data.
    - `data.ticks_ms`: Timestamp of when the data was received.
    - `data.rssi`: Received signal strength (units: dBm).
    - `data.snr`: Signal-to-noise ratio (units: dB * 4). 
    - `data.valid_crc`: CRC validity check.

    UIFlow2.0

        |recv.png|

.. method:: send(buf, tx_at_ms=None) -> int

    Send data.

    Send a data packet and return the timestamp after the packet is sent.

    - ``buf``: The data to be sent (supports string, list, tuple, or byte object).
    - ``tx_at_ms``: The timestamp in milliseconds when to send the data (optional).

    Returns a timestamp (result of `time.ticks_ms()`) indicating when the data packet was sent.

    **Example:**

    ::

        send("Hello World")        # Send data immediately
        send("Hello World", 5000)  # Send data at timestamp 5000 milliseconds

    UIFlow2.0

        |send.png|

.. method:: standby()

    Set module to standby mode.

    Puts the LoRa module into standby mode, consuming less power.

    UIFlow2.0

        |standby.png|

.. method:: sleep()

    Put the module to sleep mode.

    Reduces the power consumption by putting the module into deep sleep mode.

    UIFlow2.0

        |sleep.png|

.. method:: irq_triggered() -> bool

    Check IRQ trigger.

    Returns `True` if an interrupt service routine (ISR) has been triggered since the last send or receive started.

    UIFlow2.0

        |irq_triggered.png|