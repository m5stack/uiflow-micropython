
LoraModule
==========

.. include:: ../refs/module.lora.ref

The LoRa433_V1.1 Module is part of the M5Stack stackable module series. It is a LoRa communication module that operates at a 433MHz frequency and utilizes the Ra-02 module (SX1278 chip) solution.

Support the following products:

|LoraModule|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from module import LoraModule
    lora = LoraModule(pin_irq=35, pin_rst=13) # basic
    lora = LoraModule(pin_irq=35, pin_rst=25) # core2
    lora = LoraModule(pin_irq=10, pin_rst=5) # cores3
    lora.send("Hello, LoRa!")

    print(lora.recv())

    def callback(received_data):
        global lora
        print(received_data)
        lora.start_recv()
    lora.set_irq_callback(callback)
    lora.start_recv()


UIFLOW2 Example:

    |example_tx.svg|

    |example_rx.svg|


.. only:: builder_html

    |cores3_lora433_rx_example.m5f2|

    |cores3_lora433_tx_example.m5f2|

    |cores3_lora868_rx_example.m5f2|

    |cores3_lora868_tx_example.m5f2|


class LoraModule
----------------

Constructors
------------

.. class:: LoraModule(pin_cs, pin_irq, pin_rst, freq_band, sf, bw, coding_rate, preamble_len, output_power)

    Initialize the LoRa module.

    :param int pin_cs: Chip select pin
    :param int pin_irq: Interrupt pin
    :param int pin_rst: Reset pin
    :param  freq_band: LoRa RF frequency in kHz.
    :param int sf: Spreading factor, Higher spreading factors allow reception of weaker signals but have slower data rate.
    :param str bw: Bandwidth value in kHz. Must be exactly one of BANDWIDTHS
    :param int coding_rate: Forward Error Correction (FEC) coding rate is expressed as a ratio, &#x60;4/N&#x60;.
    :param int preamble_len: Length of the preamble sequence, in units of symbols.
    :param int output_power: Output power in dBm.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: LoraModule.send(packet, tx_at_ms)

    Send a data packet.

    :return (int): The return value is the timestamp when transmission completed, as a&#x60;time.ticks_ms()&#x60; result. It will be more accurate if the modem was initialized to use interrupts.

    :param  packet: The data packet to send.
    :param  tx_at_ms: Time to transmit the packet in milliseconds. For precise timing of sent packets, there is an optional &#x60;tx_at_ms&#x60; argument which is a timestamp (as a &#x60;time.ticks_ms()&#x60; value). If set, the packet will be sent as close as possible to this timestamp and the function will block until that time arrives

    UIFLOW2:

        |send.png|

.. method:: LoraModule.recv(timeout_ms, rx_length, rx_packet)

    Receive a data packet.

    :return (RxPacket): Returns None on timeout, or an &#x60;RxPacket&#x60; instance with the packet on success.

    :param  timeout_ms: Optional, sets a receive timeout in milliseconds. If None (default value), then the function will block indefinitely until a packet is received.
    :param int rx_length: Necessary to set if &#x60;implicit_header&#x60; is set to &#x60;True&#x60; (see above). This is the length of the packet to receive. Ignored in the default LoRa explicit header mode, where the received radio header includes the length.
    :param RxPacket rx_packet: Optional, this can be an &#x60;RxPacket&#x60; object previously received from the modem. If the newly received packet has the same length, this object is reused and returned to save an allocation. If the newly received packet has a different length, a new &#x60;RxPacket&#x60; object is allocated and returned instead.

    UIFLOW2:

        |recv.png|

.. method:: LoraModule.start_recv()

    Start receiving data once, trigger an interrupt when data is received.



    UIFLOW2:

        |start_recv.png|

.. method:: LoraModule.set_irq_callback(callback)

    Set the IRQ callback function.


    :param  callback: The callback function. The function should accept one argument, which is the received data.

    UIFLOW2:

        |set_irq_callback.png|

.. method:: LoraModule.standby()

    Set the modem to standby mode.



    UIFLOW2:

        |standby.png|

.. method:: LoraModule.sleep()

    Set the modem to sleep mode.



    UIFLOW2:

        |sleep.png|

.. method:: LoraModule.irq_triggered()

    Check if the IRQ has been triggered.



    UIFLOW2:

        |irq_triggered.png|



Constants
---------

.. data:: LoraModule.LORA_433
.. data:: LoraModule.LORA_868

    Select the LoRa frequency band.


.. data:: LoraModule.BANDWIDTHS

    Valid bandwidth


