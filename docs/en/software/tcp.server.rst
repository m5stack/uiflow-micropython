TCP Server
==========

.. include:: ../refs/software.tcp.server.ref

UiFlow2 Example
---------------

echo server
^^^^^^^^^^^

Open the |cores3_tcp_server_example.m5f2| project in UiFlow2.

This example creates a TCP server that echoes the received data.

UiFlow2 Code Block:

    |cores3_tcp_server_example.png|

Example output:

    None

MicroPython Example
-------------------

echo server
^^^^^^^^^^^

This example creates a TCP server that echoes the received data.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/softwave/tcp/cores3_tcp_server_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

.. method:: socket.socket()
            socket.bind(address)
            socket.listen([backlog])
    :no-index:

    Create a socket object and bind it to an address.

    :param tuple address: A tuple containing the server IP address and port number.
    :param int backlog: The maximum number of queued connections. Default is 5.
    :return: A socket object.
    :rtype: socket.socket

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            import socket

            tcps = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcps.bind(('0.0.0.0', 8001))
            tcps.listen(5)


.. method:: socket.close()
    :no-index:

    Close the socket connection.

    UiFlow2 Code Block:

        |close.png|

        |close_client.png|

    MicroPython Code Block:

        .. code-block:: python

            tcps.close()


.. method:: socket.accept()
    :no-index:

    Accept a connection. The socket must be bound to an address and listening
    for connections. The return value is a pair (conn, address) where conn is a
    new socket object usable to send and receive data on the connection,
    and address is the address bound to the socket on the other end of the
    connection.

    :return: A tuple containing the client socket and the address of the client.
    :rtype: tuple

    UiFlow2 Code Block:

        |accept.png|

    MicroPython Code Block:

        .. code-block:: python

            client_socket, addr = tcps.accept()
            print('Connected by', addr)


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

            data = tcps.recv(1024)
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

            data = tcps.read()
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

            tcps.send(b'Hello, World!')
            tcps.send('Hello, World!')


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

            tcps.write(b'Hello, World!')
            tcps.write('Hello, World!')


.. method:: socket.setblocking(flag)
   :no-index:

    Set blocking or non-blocking mode of the socket: if flag is false, the
    socket is set to non-blocking, else to blocking mode.

   This method is a shorthand for certain `settimeout()` calls:

   * ``sock.setblocking(True)`` is equivalent to ``sock.settimeout(None)``
   * ``sock.setblocking(False)`` is equivalent to ``sock.settimeout(0)``

    :param bool flag: If True, the socket will be in blocking mode. If False, the socket will be in non-blocking mode.
    :return: None
    :rtype: None

    UiFlow2 Code Block:

        |setblocking.png|

    MicroPython Code Block:

        .. code-block:: python

            tcps.setblocking(True)
            tcps.setblocking(False)


.. method:: socket.settimeout(timeout)
    :no-index:

    Set a timeout on blocking socket operations. The value argument can be a
    nonnegative floating point number expressing seconds, or None. If a
    non-zero value is given, subsequent socket operations will raise an OSError
    exception if the timeout period value has elapsed before the operation has
    completed. If zero is given, the socket is put in non-blocking mode. If None
    is given, the socket is put in blocking mode.

    :param float timeout: The timeout value in seconds. If None, the socket is put in blocking mode.
    :return: None
    :rtype: None

    UiFlow2 Code Block:

        |settimeout.png|

    MicroPython Code Block:

        .. code-block:: python

            tcps.settimeout(5)
            tcps.settimeout(None)


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

            tcps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 0)
            tcps.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
