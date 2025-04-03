UDP Server
==========

.. include:: ../refs/software.udp.server.ref

UiFlow2 Example
---------------

echo server
^^^^^^^^^^^

Open the |cores3_udp_server_example.m5f2| project in UiFlow2.

This example creates a UDP server that echoes the received data.

UiFlow2 Code Block:

    |cores3_udp_server_example.png|

Example output:

    None

MicroPython Example
-------------------

echo server
^^^^^^^^^^^

This example creates a UDP server that echoes the received data.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/softwave/udp/cores3_udp_server_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

.. method:: socket.socket()
            socket.bind(address)
    :no-index:

    Create a socket object and bind it to an address.

    :param tuple address: A tuple containing the server IP address and port number.
    :return: A socket object.
    :rtype: socket.socket

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            import socket

            udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udps.bind(('0.0.0.0', 8000))


.. method:: socket.close()
    :no-index:

    Close the socket connection.

    UiFlow2 Code Block:

        |close.png|

    MicroPython Code Block:

        .. code-block:: python

            udps.close()


.. method:: socket.recv(bufsize)
    :no-index:

    Receive data from the socket.

    :param int bufsize: The maximum amount of data to be received at once.
    :return: The received data.
    :rtype: bytes

    UiFlow2 Code Block:

        |recv.png|

    MicroPython Code Block:

        .. code-block:: python

            data = udps.recv(1024)
            print(data)


.. method:: socket.recvfrom(bufsize)
    :no-index:

    Receive data from the socket. The return value is a pair (bytes, address)
    where bytes is a bytes object representing the data received and address is
    the address of the socket sending the data.

    :param int bufsize: The maximum amount of data to be received at once.
    :return: The received data.
    :rtype: tuple

    UiFlow2 Code Block:

        |recvfrom.png|

    MicroPython Code Block:

        .. code-block:: python

            data, address = udps.recvfrom(1024)
            print(data)


.. method:: socket.read()
    :no-index:

    Read data from the socket.

    :return: The received data.
    :rtype: bytes

    UiFlow2 Code Block:

        |read.png|

    MicroPython Code Block:

        .. code-block:: python

            data = udps.read()
            print(data)


.. method:: socket.send(data)
    :no-index:

    Send data to the socket. The socket must be connected to a remote socket.

    :param data: The data to be sent.
    :type data: bytes | str
    :return: The number of bytes sent.
    :rtype: int

    UiFlow2 Code Block:

        |send.png|

    MicroPython Code Block:

        .. code-block:: python

            udps.send(b'Hello, World!')
            udps.send('Hello, World!')


.. method:: socket.sendto(data, address)
    :no-index:

    Send data to the socket. The socket should not be connected to a remote socket, since the destination socket is specified by address.

    :param data: The data to be sent.
    :type data: bytes | str
    :param tuple address: A tuple containing the destination IP address and port number.
    :return: The number of bytes sent.
    :rtype: int

    UiFlow2 Code Block:

        |sendto.png|

    MicroPython Code Block:

        .. code-block:: python

            udps.sendto("hello", ("192.168.8.8", 8000))


.. method:: socket.write(data)
    :no-index:

    Write the buffer of bytes to the socket. This function will try to write all
    data to a socket (no “short writes”). This may be not possible with a
    non-blocking socket though, and returned value will be less than the length
    of buf.

    :param data: The data to be sent.
    :type data: bytes | str
    :return: The number of bytes sent.
    :rtype: int

    UiFlow2 Code Block:

        |write.png|

    MicroPython Code Block:

        .. code-block:: python

            udps.write(b'Hello, World!')
            udps.write('Hello, World!')


.. method:: socket.setsockopt(level, optname, value)
    :no-index:

    Set the value of the given socket option. The needed symbolic constants are
    defined in the socket module (SO_* etc.). The value can be an integer or a
    bytes-like object representing a buffer.

    :param int level: The level at which the option is defined.
    :param int optname: The name of the option to set.
    :param value: The value to set for the option.

    UiFlow2 Code Block:

        |setsockopt.png|

    MicroPython Code Block:

        .. code-block:: python

            udps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
            udps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

