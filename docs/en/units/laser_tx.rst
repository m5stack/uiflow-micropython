
LaserTX Unit
============
.. sku:U066
.. include:: ../refs/unit.laser_tx.ref

LASER.TX is one of the communication devices among the M5Units family - a Laser emitter with adjustable focal length.It is mainly built with a laser diode Laser communications devices are wireless connections through the atmosphere. They work similarly to fiber-optic links, except the beam is transmitted through free space. While the transmitter and receiver must require line-of-sight conditions, they have the benefit of eliminating the need for broadcast rights and buried cables.

Support the following products:

|LaserTXUnit|

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

class LaserTXUnit
-----------------

Constructors
------------

.. class:: LaserTXUnit(port, mode, id)

    Initialize the LaserTXUnit with the specified port, communication mode, and UART ID.

    :param tuple port: A tuple containing pin numbers for TX and RX.
    :param int mode: Communication mode; use PIN_MODE or UART_MODE.
    :param int id: UART ID, either 1 or 2.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: LaserTXUnit.init_uart(baudrate, bits, parity, stop)

    Initialize UART communication with specified parameters.

    :param int baudrate: The baud rate for UART communication. Default is 115200.
    :param int bits: The number of data bits; 7, 8, or 9. Default is 8.
    :param int parity: Parity setting; None, 0, or 1. Default is 8.
    :param int stop: The number of stop bits; 1 or 2. Default is 1.

    UIFLOW2:

        |init_uart.png|

.. method:: LaserTXUnit.write(payload)

    Transmit data through UART.

    :param  payload: The data to be transmitted via UART.

    UIFLOW2:

        |write.png|

.. method:: LaserTXUnit.on()

    Turn on the laser when using PIN_MODE.


    UIFLOW2:

        |on.png|

.. method:: LaserTXUnit.off()

    Turn off the laser when using PIN_MODE.


    UIFLOW2:

        |off.png|

.. method:: LaserTXUnit.value(x)

    Set the laser state to either on or off using PIN_MODE.

    :param bool x: A boolean value; True turns the laser on, False turns it off.
