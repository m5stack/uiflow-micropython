UDP Client
==========

.. include:: ../refs/software.udp.client.ref

UiFlow2 Example
---------------

simple client
^^^^^^^^^^^^^

Open the |cores3_udp_client_example.m5f2| project in UiFlow2.

This example creates a UDP client that sends data to a server.

UiFlow2 Code Block:

    |cores3_udp_client_example.png|

Example output:

    None

MicroPython Example
-------------------

sample client
^^^^^^^^^^^^^

This example creates a UDP client that sends data to a server.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/software/udp/cores3_udp_client_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

.. method:: socket.socket()
            socket.connect(address)
    :no-index:

    Create a socket object and connect to the server.

    :param tuple address: A tuple containing the server IP address and port number.
    :return: A socket object.
    :rtype: socket.socket

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            import socket

            udpc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udpc.connect(('192.168.8.236', 8000))


.. method:: socket.close()
    :no-index:

    Close the socket connection.

    UiFlow2 Code Block:

        |close.png|

    MicroPython Code Block:

        .. code-block:: python

            udpc.close()


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

            data = udpc.recv(1024)
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

            data = udpc.read()
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

            udpc.send(b'Hello, World!')
            udpc.send('Hello, World!')


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

            udpc.write(b'Hello, World!')
            udpc.write('Hello, World!')


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

            udpc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
            udpc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
