.. currentmodule:: bleuart

class BLEUARTServer
===================

.. include:: ../refs/system.bleuart.server.ref

BLEUARTServer class is a BLE UART server, which can be connected to by a BLE UART client and communicate with it.


Micropython Example:

    .. literalinclude:: ../../../examples/system/bleuart/cores3_bleuart_server_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_bleuart_server_example.m5f2|


Constructors
------------

.. class:: bleuart.BLEUARTServer(name="", rxbuf=100, verbose=False)

    Create a BLE UART server.

    :param str name: The name of the ble device.
    :param int rxbuf: The size of the receive buffer.
    :param bool verbose: Enable verbose output.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: BLEUARTServer.irq()

    The irq of the ble uart server.


.. method:: BLEUARTServer.any() -> int

    Check if there is any data in the receive buffer.

    :return: The number of bytes in the receive buffer.

    UIFLOW2:

        |any.png|


.. method:: BLEUARTServer.read(sz=None) -> bytes

    Read data from the receive buffer.

    :param int sz: The number of bytes to read. If not specified, read all data.

    :return: The data read from the receive buffer.

    UIFLOW2:

        |read_all.png|

        |read_bytes.png|

        |read_raw_data.png|

        |readline.png|


.. method:: BLEUARTServer.write(data: bytes)

    Write data to the ble uart server.

    :param bytes data: The data to write.

    UIFLOW2:

        |write.png|

        |write1.png|

        |write_line.png|

        |write_list.png|

        |write_raw_data.png|

        |write_raw_data1.png|


.. method:: BLEUARTServer.close()

    Close the ble uart server.

    UIFLOW2:

        |close.png|

.. method:: BLEUARTServer.deinit()

    Deinitialize the ble uart server.

    UIFLOW2:

        |deinit.png|
