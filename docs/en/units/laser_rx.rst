
LaserRX Unit
============
.. sku:U065
.. include:: ../refs/unit.laser_rx.ref

LASER.RX is one of the communication devices among M5Units, a Laser receiver. It is mainly built with a laser transistor. Laser communications devices are wireless connections through the atmosphere. They work similarly to fiber-optic links, except the beam is transmitted through free space. While the transmitter and receiver must require line-of-sight conditions, they have the benefit of eliminating the need for broadcast rights and buried cables. Laser communications systems can be easily deployed since they are inexpensive, small, low power and do not require any radio interference studies. Two parallel beams are needed, one for transmission and one for reception. Therefore we have a LASER.TX in parallel.

Support the following products:

|LaserRXUnit|

LaserTX Example:

    .. literalinclude:: ../../../examples/unit/laser/lasertx_cores3_example.py
        :language: python
        :linenos:

LaserRX Example:

    .. literalinclude:: ../../../examples/unit/laser/laserrx_core2_example.py
        :language: python
        :linenos:

LaserTX UIFLOW2 Example:

    |example_tx.png|

LaserRX UIFLOW2 Example:

    |example_rx.png|

.. only:: builder_html

    |laserrx_core2_example.m5f2|

    |lasertx_cores3_example.m5f2|


class LaserRXUnit
-----------------

Constructors
------------

.. class:: LaserRXUnit(port, mode, id)

    Initialize the LaserRXUnit with the specified port, communication mode, and UART ID.

    :param tuple port: A tuple containing pin numbers for TX and RX.
    :param int mode: Communication mode; use PIN_MODE or UART_MODE.
    :param int id: UART ID, either 1 or 2.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: LaserRXUnit.init_uart(baudrate, bits, parity, stop)

    Initialize UART communication with specified parameters.

    :param int baudrate: The baud rate for UART communication. Default is 115200.
    :param int bits: The number of data bits; 7, 8, or 9. Default is 8.
    :param int parity: Parity setting; None, 0, or 1. Default is 8.
    :param int stop: The number of stop bits; 1 or 2. Default is 1.

    UIFLOW2:

        |init_uart.png|

.. method:: LaserRXUnit.read(byte)

    Read data from UART. Optionally specify the number of bytes to read.

    :param  byte: The number of bytes to read. If None, reads all available data.

    :returns: The data read from UART or None if no data is available.
            
    UIFLOW2:

        |read.png|

.. method:: LaserRXUnit.readline()

    Read a single line of data from UART.

    :returns: The line read from UART or None if no data is available.


.. method:: LaserRXUnit.any()

    Check if there is any data available in UART buffer.

    :returns: True if data is available; otherwise, False.

    UIFLOW2:

        |any.png|

.. method:: LaserRXUnit.value()

    Get the current value of the input pin when using PIN_MODE.

    :returns: The value of the pin (0 or 1).
