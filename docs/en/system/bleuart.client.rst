.. currentmodule:: bleuart

class BLEUARTClient
===================

.. include:: ../refs/system.bleuart.client.ref

BLEUARTClient class is a BLE UART client, which can connect to a BLE UART server and communicate with it.


Micropython Example:

    .. literalinclude:: ../../../examples/system/bleuart/atoms3_bleuart_client_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |atoms3_bleuart_client_example.m5f2|


Constructors
------------

.. class:: bleuart.BLEUARTClient(name="", rxbuf=100, verbose=False)

    Create a BLE UART client.

    :param str name: The name of the ble device.
    :param int rxbuf: The size of the receive buffer.
    :param bool verbose: Enable verbose output.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: BLEUARTClient.irq()

    The irq of the ble uart client.


.. method:: BLEUARTClient.is_connected()

    Check if the ble uart server is connected.

    UIFLOW2:

        |is_connected.png|


.. method:: BLEUARTClient.connect(name, timeout=2000)

    Connect to the ble uart server.

    :param str name: The name of the ble device.
    :param int timeout: The timeout of the connection.

    UIFLOW2:

        |connect.png|


.. method:: BLEUARTClient.any() -> int

    Check if there is any data in the receive buffer.

    :return: The number of bytes in the receive buffer.

    UIFLOW2:

        |any.png|


.. method:: BLEUARTClient.read(sz=None) -> bytes

    Read data from the receive buffer.

    :param int sz: The number of bytes to read. If not specified, read all data.

    :return: The data read from the receive buffer.

    UIFLOW2:

        |read_all.png|

        |read_bytes.png|

        |read_raw_data.png|

        |readline.png|


.. method:: BLEUARTClient.write(data: bytes)

    Write data to the ble uart server.

    :param bytes data: The data to write.

    UIFLOW2:

        |write.png|

        |write1.png|

        |write_line.png|

        |write_list.png|

        |write_raw_data.png|

        |write_raw_data1.png|


.. method:: BLEUARTClient.close()

    Close the ble uart server.

    UIFLOW2:

        |close.png|

.. method:: BLEUARTClient.deinit()

    Deinitialize the ble uart server.

    UIFLOW2:

        |deinit.png|
