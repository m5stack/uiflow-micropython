
LoraModule
==========

.. include:: ../refs/module.loramodule.ref

The LoRa433_V1.1 Module is part of the M5Stack stackable module series. It is a LoRa communication module that operates at a 433MHz frequency and utilizes the Ra-02 module (SX1278 chip) solution.

Support the following products:

|LoraModule|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from module import LoraModule
    lora = LoraModule()
    lora.send("Hello, LoRa!")
    print(lora.recv())
    

UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

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

        |init.svg|


Methods
-------

.. method:: LoraModule.send(packet, tx_at_ms)

    Send a data packet.

    :param  packet: The data packet to send.
    :param  tx_at_ms: Time to transmit the packet in milliseconds. For precise timing of sent packets, there is an optional &#x60;tx_at_ms&#x60; argument which is a timestamp (as a &#x60;time.ticks_ms()&#x60; value). If set, the packet will be sent as close as possible to this timestamp and the function will block until that time arrives

    UIFLOW2:

        |send.svg|

.. method:: LoraModule.recv(timeout_ms, rx_length, rx_packet)

    Receive a data packet.

    :param  timeout_ms: Optional, sets a receive timeout in milliseconds. If None (default value), then the function will block indefinitely until a packet is received.
    :param int rx_length: Necessary to set if &#x60;implicit_header&#x60; is set to &#x60;True&#x60; (see above). This is the length of the packet to receive. Ignored in the default LoRa explicit header mode, where the received radio header includes the length.
    :param RxPacket rx_packet: Optional, this can be an &#x60;RxPacket&#x60; object previously received from the modem. If the newly received packet has the same length, this object is reused and returned to save an allocation. If the newly received packet has a different length, a new &#x60;RxPacket&#x60; object is allocated and returned instead.

    UIFLOW2:

        |recv.svg|



Constants
---------

.. data:: LoraModule.LORA_433
.. data:: LoraModule.LORA_868

    Select the LoRa frequency band.

	
.. data:: LoraModule.BANDWIDTHS

    Valid bandwidth

	
