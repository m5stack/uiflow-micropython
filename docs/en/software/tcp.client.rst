TCP Client
==========

.. include:: ../refs/software.tcp.client.ref

UiFlow2 Example
---------------

simple client
^^^^^^^^^^^^^

Open the |cores3_tcp_client_example.m5f2| project in UiFlow2.

This example creates a TCP client that sends data to a server.

UiFlow2 Code Block:

    |cores3_tcp_client_example.png|

Example output:

    None

MicroPython Example
-------------------

simple client
^^^^^^^^^^^^^

This example creates a TCP client that sends data to a server.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/softwave/tcp/cores3_tcp_client_example.py
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

            tcpc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcpc.connect(('192.168.8.236', 8001))


.. method:: socket.close()
    :no-index:

    Close the socket connection.

    UiFlow2 Code Block:

        |close.png|

    MicroPython Code Block:

        .. code-block:: python

            tcpc.close()

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

            data = tcpc.recv(1024)
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

            data = tcpc.read()
            print(data)

.. method:: socket.readline()
    :no-index:

    Read a line, ending in a newline character.

    :return: the line read.
    :rtype: str

    UiFlow2 Code Block:

        |readline.png|

    MicroPython Code Block:

        .. code-block:: python

            data = tcpc.readline()
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

            tcpc.send(b'Hello, World!')
            tcpc.send('Hello, World!')


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

            tcpc.write(b'Hello, World!')
            tcpc.write('Hello, World!')


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

            tcpc.setblocking(True)
            tcpc.setblocking(False)


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

            tcpc.settimeout(5)
            tcpc.settimeout(None)
