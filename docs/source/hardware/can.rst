.. py:currentmodule:: hardware

CAN
===

.. include:: ../refs/hardware.can.ref

CAN currently only supports the classic CAN controller on ESP32 series.
At the physical level CAN bus consists of 2 lines: RX and TX.  Note that to connect the M5Stack device
to a CAN bus you must use a CAN transceiver to convert the CAN logic signals from the MCU to the
correct voltage levels on the bus.

For detailed examples, please refer to: :ref:`unit.CANUnit <unit.CANUnit>`

API
---

CAN
^^^

.. class:: CAN(bus, mode, tx, rx, prescaler=32, sjw=3, bs1=15, bs2=4, triple_sampling=False)

    Construct a CAN object on the given bus.

    :param int bus: must be 0.
    :param int mode: One of NORMAL, NO_ACKNOWLEDGE, LISTEN_ONLY.
    :param int tx: The pin to use for transmitting data.
    :param int rx: The pin to use for receiving data.
    :param int prescaler: The value by which the CAN input clock is divided to generate the nominal bit time quanta. Value between 1 and 1024 inclusive for classic CAN.
    :param int sjw: The resynchronisation jump width in units of time quanta for nominal bits; value between 1 and 4 inclusive for classic CAN.
    :param int bs1: Defines the location of the sample point in units of the time quanta for nominal bits; value between 1 and 16 inclusive for classic CAN.
    :param int bs2: Defines the location of the transmit point in units of the time quanta for nominal bits; value between 1 and 8 inclusive for classic CAN.
    :param bool triple_sampling: Enables triple sampling when the TWAI controller samples a bit.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hardware import CAN
            can = CAN(0, CAN.NORMAL, 0, 0, 25000)


    .. py:method:: CAN.init(mode, tx, rx, prescaler=32, sjw=3, bs1=15, bs2=4, triple_sampling=False)

        Initialise the CAN bus with the given parameters.

        :param int mode: One of NORMAL, NO_ACKNOWLEDGE, LISTEN_ONLY.
        :param int tx: The pin to use for transmitting data.
        :param int rx: The pin to use for receiving data.
        :param int prescaler: The value by which the CAN input clock is divided to generate the nominal bit time quanta.
        :param int sjw: The resynchronisation jump width in units of time quanta for nominal bits.
        :param int bs1: Defines the location of the sample point in units of the time quanta for nominal bits.
        :param int bs2: Defines the location of the transmit point in units of the time quanta for nominal bits.
        :param bool triple_sampling: Enables triple sampling when the TWAI controller samples a bit.

        The time quanta tq is the basic unit of time for the CAN bus.  tq is the CAN
        prescaler value divided by APB_CLK clock source (typically 80 MHz);

        A single bit is made up of the synchronisation segment, which is always 1 tq.
        Then follows bit segment 1, then bit segment 2.  The sample point is after bit
        segment 1 finishes.  The transmit point is after bit segment 2 finishes.
        The baud rate will be 1/bittime, where the bittime is 1 + BS1 + BS2 multiplied
        by the time quanta tq.

        For example, with APB_CLK=80MHz, prescaler=32, sjw=3, bs1=15, bs2=4, the value of
        tq is 0.4 microseconds.  The bittime is 8 microseconds, and the baudrate
        is 125kHz.

        See esp32 technical reference manual for more details.

        MicroPython Code Block:

            .. code-block:: python

                can.init(CAN.NORMAL, 0, 0, 25000)

    .. py:method:: CAN.deinit()

        Turn off the CAN bus.

        UiFlow2 Code Block:

            |deinit.png|

        MicroPython Code Block:

            .. code-block:: python

                can.deinit()

    .. py:method:: CAN.restart()

        Force a software restart of the CAN controller without resetting its configuration.

        If the controller enters the bus-off state then it will no longer participate
        in bus activity.  If the controller is not configured to automatically restart
        (see :meth:\`~CAN.init()\`) then this method can be used to trigger a restart,
        and the controller will follow the CAN protocol to leave the bus-off state and
        go into the error active state.

        UiFlow2 Code Block:

            |restart.png|

        MicroPython Code Block:

            .. code-block:: python

                can.restart()

    .. py:method:: CAN.state()

        Return the state of the controller.

        :returns: int

        - \`\`0\`\` -- \`\`CAN.STOPPED\`\` : the controller is completely off and reset;
        - \`\`4\`\` -- \`\`CAN.BUS_OFF\`\` : the controller is on but not participating in bus activity (TEC overflowed beyond 255);
        - \`\`5\`\` -- \`\`CAN.RECOVERING\`\` -- The controller is undergoing bus recovery.
        - \`\`6\`\` -- \`\`CAN.RUNNING\`\` : The controller can transmit and receive messages;

        UiFlow2 Code Block:

            |state.png|

        MicroPython Code Block:

            .. code-block:: python

                status = can.state()

    .. py:method:: CAN.info([list])

        Get information about the controller's error states and TX and RX buffers.

        :param list list: Optional list object with at least 8 entries.
        :returns: list

        The values in the list are:

        - TEC value
        - REC value
        - number of times the controller enterted the Error Warning state(ignored for now, compatible with pyb.CAN)
        - number of times the controller enterted the Error Passive state(ignored for now, compatible with pyb.CAN)
        - number of times the controller enterted the Bus Off state(ignored for now, compatible with pyb.CAN)
        - number of pending TX messages
        - number of pending RX messages
        - number of pending RX messages on fifo 1(ignored for now, compatible with pyb.CAN)

        UiFlow2 Code Block:

            |info.png|

        MicroPython Code Block:

            .. code-block:: python

                info = can.info()

    .. py:method:: CAN.any(fifo)

        Return \`\`True\`\` if any message waiting on the FIFO, else \`\`False\`\`.

        :param int fifo: FIFO index.
        :returns: bool

        UiFlow2 Code Block:

            |any.png|

        MicroPython Code Block:

            .. code-block:: python

                if can.any(0):
                    print("Message waiting")

    .. py:method:: CAN.recv(fifo, list=None, *, timeout=5000)

        Receive data on the bus.

        :param int fifo: fifo is an integer, it can be any number and compatible with pyb.CAN
        :param list list: optional list object to be used as the return value
        :param int timeout: timeout in milliseconds to wait for the receive.
        :returns: tuple

        Return value: A tuple containing five values.

        - The id of the message.
        - A boolean that indicates if the message ID is standard or extended.
        - A boolean that indicates if the message is an RTR message.
        - The FMI (Filter Match Index) value.
        - An array containing the data.

        If *list* is \`\`None\`\` then a new tuple will be allocated, as well as a new
        bytes object to contain the data (as the fifth element in the tuple).

        If *list* is not \`\`None\`\` then it should be a list object with a least five
        elements.  The fifth element should be a memoryview object which is created
        from either a bytearray or an array of type 'B' or 'b', and this array must
        have enough room for at least 8 bytes.  The list object will then be
        populated with the first four return values above, and the memoryview object
        will be resized inplace to the size of the data and filled in with that data.
        The same list and memoryview objects can be reused in subsequent calls to
        this method, providing a way of receiving data without using the heap.
        For example::

            buf = bytearray(8)
            lst = [0, 0, 0, 0, memoryview(buf)]
            # No heap memory is allocated in the following call
            can.recv(0, lst)

        UiFlow2 Code Block:

            |recv1.png|

            |recv2.png|

        MicroPython Code Block:

            .. code-block:: python

                can.recv(0)

    .. py:method:: CAN.send(data, id, *, timeout=0, rtr=False, extframe=False)

        Send a message on the bus.

        :param data: data is the data to send (an integer to send, or a buffer object).
        :param int id: id is the id of the message to be sent.
        :param int timeout: timeout is the timeout in milliseconds to wait for the send.
        :param bool rtr: rtr is a boolean that specifies if the message shall be sent as a remote transmission request. If rtr is True then only the length of data is used to fill in the DLC slot of the frame; the actual bytes in data are unused.
        :param bool extframe: extframe if True the frame will have an extended identifier (29 bits), otherwise a standard identifier (11 bits) is used.

        If timeout is 0 the message is placed in a buffer in one of three hardware
        buffers and the method returns immediately. If all three buffers are in use
        an exception is thrown. If timeout is not 0, the method waits until the
        message is transmitted. If the message can't be transmitted within the
        specified time an exception is thrown.

        :returns: None

        UiFlow2 Code Block:

            |send.png|

        MicroPython Code Block:

            .. code-block:: python

                can.send('message!', 123)

    .. py:data:: CAN.NORMAL
            CAN.NO_ACKNOWLEDGE
            CAN.LISTEN_ONLY

        The mode of the CAN bus used in :meth:\`~CAN.init()\`.

    .. py:data:: CAN.STOPPED
            CAN.RUNNING
            CAN.BUS_OFF
            CAN.RECOVERING

        Possible states of the CAN controller returned from :meth:\`~CAN.state()\`.
