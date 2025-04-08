.. _hardware.CAN:

CAN
===

.. include:: ../refs/hardware.can.ref

CAN implements support for classic CAN (available on F4, F7 MCUs) and CAN FD (H7 series) controllers.
At the physical level CAN bus consists of 2 lines: RX and TX.  Note that to connect the pyboard to a
CAN bus you must use a CAN transceiver to convert the CAN logic signals from the pyboard to the correct
voltage levels on the bus.

Example usage for classic CAN controller in Loopback (transceiver-less) mode::

    from m5can import CAN
    can = CAN(1, CAN.LOOPBACK, 1, 2)
    can.send('message!', 123)   # send a message with id 123
    can.recv(0)                 # receive message


For detailed examples, please refer to: :ref:`unit.CANUnit <unit.CANUnit>`


Constructors
------------

.. class:: CAN(bus, mode, tx, rx, prescaler=32, sjw=3, bs1=15, bs2=4, triple_sampling=False)

    Construct a CAN object on the given bus.  *bus* must be 0.
    With no additional parameters, the CAN object is created but not
    initialised (it has the settings from the last initialisation of
    the bus, if any).  If extra arguments are given, the bus is initialised.
    See :meth:`CAN.init` for parameters of initialisation.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: CAN.init(mode, tx, rx, prescaler=32, sjw=3, bs1=15, bs2=4, triple_sampling=False)

    Initialise the CAN bus with the given parameters:

        - *mode* is one of:  NORMAL, NO_ACKNOWLEDGE, LISTEN_ONLY
        - *tx* is the pin to use for transmitting data
        - *rx* is the pin to use for receiving data
        - *prescaler* is the value by which the CAN input clock is divided to generate the
          nominal bit time quanta. The prescaler can be a value between 1 and 1024 inclusive
          for classic CAN.
        - *sjw* is the resynchronisation jump width in units of time quanta for nominal bits;
          it can be a value between 1 and 4 inclusive for classic CAN.
        - *bs1* defines the location of the sample point in units of the time quanta for nominal bits;
          it can be a value between 1 and 16 inclusive for classic CAN.
        - *bs2* defines the location of the transmit point in units of the time quanta for nominal bits;
          it can be a value between 1 and 8 inclusive for classic CAN.
        - *triple_sampling* is Enables triple sampling when the TWAI controller samples a bit


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

.. method:: CAN.deinit()

    Turn off the CAN bus.

    UIFLOW2:

        |deinit.png|


.. method:: CAN.restart()

    Force a software restart of the CAN controller without resetting its
    configuration.

    If the controller enters the bus-off state then it will no longer participate
    in bus activity.  If the controller is not configured to automatically restart
    (see :meth:`~CAN.init()`) then this method can be used to trigger a restart,
    and the controller will follow the CAN protocol to leave the bus-off state and
    go into the error active state.

    UIFLOW2:

        |restart.png|

.. method:: CAN.state()

    Return the state of the controller.  The return value can be one of:

    - ``CAN.STOPPED`` -- the controller is completely off and reset;
    - ``CAN.RUNNING`` -- The controller can transmit and receive messages;
    - ``CAN.BUS_OFF`` -- the controller is on but not participating in bus activity
      (TEC overflowed beyond 255);
    - ``RECOVERING`` -- The controller is undergoing bus recovery.

    UIFLOW2:

        |state.png|


.. method:: CAN.info([list])

    Get information about the controller's error states and TX and RX buffers.
    If *list* is provided then it should be a list object with at least 8 entries,
    which will be filled in with the information.  Otherwise a new list will be
    created and filled in.  In both cases the return value of the method is the
    populated list.

    The values in the list are:

    - TEC value
    - REC value
    - number of times the controller enterted the Error Warning state(ignored for now, compatible with pyb.CAN)
    - number of times the controller enterted the Error Passive state(ignored for now, compatible with pyb.CAN)
    - number of times the controller enterted the Bus Off state(ignored for now, compatible with pyb.CAN)
    - number of pending TX messages
    - number of pending RX messages
    - number of pending RX messages on fifo 1(ignored for now, compatible with pyb.CAN)

    UIFLOW2:

        |info.png|


.. method:: CAN.any(fifo)

    Return ``True`` if any message waiting on the FIFO, else ``False``.

    UIFLOW2:

        |any.png|


.. method:: CAN.recv(fifo, list=None, *, timeout=5000)

    Receive data on the bus:

        - *fifo* is an integer, it can be any number and compatible with pyb.CAN
        - *list* is an optional list object to be used as the return value
        - *timeout* is the timeout in milliseconds to wait for the receive.

    Return value: A tuple containing five values.

        - The id of the message.
        - A boolean that indicates if the message ID is standard or extended.
        - A boolean that indicates if the message is an RTR message.
        - The FMI (Filter Match Index) value.
        - An array containing the data.

    If *list* is ``None`` then a new tuple will be allocated, as well as a new
    bytes object to contain the data (as the fifth element in the tuple).

    If *list* is not ``None`` then it should be a list object with a least five
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

    UIFLOW2:

        |recv1.png|

        |recv2.png|


.. method:: CAN.send(data, id, *, timeout=0, rtr=False, extframe=False)

    Send a message on the bus:

        - *data* is the data to send (an integer to send, or a buffer object).
        - *id* is the id of the message to be sent.
        - *timeout* is the timeout in milliseconds to wait for the send.
        - *rtr* is a boolean that specifies if the message shall be sent as
          a remote transmission request.  If *rtr* is True then only the length
          of *data* is used to fill in the DLC slot of the frame; the actual
          bytes in *data* are unused.
        - *extframe* if True the frame will have an extended identifier (29 bits),
          otherwise a standard identifier (11 bits) is used.

        If timeout is 0 the message is placed in a buffer in one of three hardware
        buffers and the method returns immediately. If all three buffers are in use
        an exception is thrown. If timeout is not 0, the method waits until the
        message is transmitted. If the message can't be transmitted within the
        specified time an exception is thrown.

    Return value: ``None``.

    UIFLOW2:

        |send.png|


Constants
---------

.. data:: CAN.NORMAL
          CAN.NO_ACKNOWLEDGE
          CAN.LISTEN_ONLY

    The mode of the CAN bus used in :meth:`~CAN.init()`.


.. data:: CAN.STOPPED
          CAN.RUNNING
          CAN.BUS_OFF
          CAN.RECOVERING

    Possible states of the CAN controller returned from :meth:`~CAN.state()`.
