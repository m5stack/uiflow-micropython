PwrCAN Module
===============

.. include:: ../refs/module.pwrcan.ref

PwrCAN Module 13.2 is a multifunctional module designed for the PwrCAN bus, integrating isolated CAN communication and DC 9-24V power bus. The module also includes Pwr485 (with isolation) bus functionality and can provide isolated 5V power supply to the M5 host. The CAN communication part uses the CA-IS3050G isolated transceiver, and the RS485 part uses the CA-IS3082W isolated transceiver. The GPIOs related to CAN and RS485 communication can be selected through dip switches, and the 120-ohm terminal resistance at the CAN and RS485 outputs can also be selected through dip switches. The module's power bus supports DC 9-24V wide voltage input, with the DC socket directly connected to the HT3.96 and XT30 power parts. The built-in isolated power module F0505S-2WR3 provides power to the M5 host. This module is suitable for fields such as robot control, protocol conversion, industrial automation, automotive communication systems, intelligent transportation, and building automation.

Supported Products:

|PwrCANModule|


Micropython Example:

    .. literalinclude:: ../../../examples/module/pwrcan/pwrcan_cores3_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |pwrcan_cores3_example.m5f2|

class PwrCANModule
------------------

Constructors
------------
.. class:: PwrCANModule(id, mode, tx, rx,  prescaler=32, sjw=3, bs1=15, bs2=4, triple_sampling=False)
    :no-index:
    
    Initialise the CAN bus with the given parameters:

        - ``id`` is the can bus id
        - ``tx`` is the pin to use for transmitting data
        - ``rx`` is the pin to use for receiving data
        - ``mode`` is one of:  NORMAL, NO_ACKNOWLEDGE, LISTEN_ONLY
        - ``prescaler`` is the value by which the CAN input clock is divided to generate the
          nominal bit time quanta. The prescaler can be a value between 1 and 1024 inclusive
          for classic CAN.
        - ``sjw`` is the resynchronisation jump width in units of time quanta for nominal bits;
          it can be a value between 1 and 4 inclusive for classic CAN.
        - ``bs1`` defines the location of the sample point in units of the time quanta for nominal bits;
          it can be a value between 1 and 16 inclusive for classic CAN.
        - ``bs2`` defines the location of the transmit point in units of the time quanta for nominal bits;
          it can be a value between 1 and 8 inclusive for classic CAN.
        - ``triple_sampling`` is Enables triple sampling when the TWAI controller samples a bit

    UIFLOW2:

        |init.png|

Methods
-------

PwrCANModule class inherits CAN class, See :ref:`hardware.CAN <hardware.CAN>` for more details.


class PwrCANModuleRS485
-----------------------

Constructors
------------

.. class:: PwrCANModuleRS485(id, baudrate=9600, bits=8, parity=None, stop=1, *, ...)

    Construct a UART object of the given id.

    For more parameters, please refer to init.

    UIFLOW2:

        |init_rs485.png|


Methods
-------

.. method:: PwrCANModuleRS485.init(baudrate=9600, bits=8, parity=None, stop=1, *, ...)

    Initialise the UART bus with the given parameters:

        - *baudrate* is the clock rate.
        - *bits* is the number of bits per character, 7, 8 or 9.
        - *parity* is the parity, ``None``, 0 (even) or 1 (odd).
        - *stop* is the number of stop bits, 1 or 2.

    Additional keyword-only parameters that may be supported by a port are:

        - *tx* specifies the TX pin to use.
        - *rx* specifies the RX pin to use.
        - *rts* specifies the RTS (output) pin to use for hardware receive flow control.
        - *cts* specifies the CTS (input) pin to use for hardware transmit flow control.
        - *txbuf* specifies the length in characters of the TX buffer.
        - *rxbuf* specifies the length in characters of the RX buffer.
        - *timeout* specifies the time to wait for the first character (in ms).
        - *timeout_char* specifies the time to wait between characters (in ms).
        - *invert* specifies which lines to invert.

            - ``0`` will not invert lines (idle state of both lines is logic high).
            - ``PwrCANModuleRS485.INV_TX`` will invert TX line (idle state of TX line now logic low).
            - ``PwrCANModuleRS485.INV_RX`` will invert RX line (idle state of RX line now logic low).
            - ``PwrCANModuleRS485.INV_TX | PwrCANModuleRS485.INV_RX`` will invert both lines (idle state at logic low).

        - *flow* specifies which hardware flow control signals to use. The value
          is a bitmask.

            - ``0`` will ignore hardware flow control signals.
            - ``PwrCANModuleRS485.RTS`` will enable receive flow control by using the RTS output pin to
              signal if the receive FIFO has sufficient space to accept more data.
            - ``PwrCANModuleRS485.CTS`` will enable transmit flow control by pausing transmission when the
              CTS input pin signals that the receiver is running low on buffer space.
            - ``PwrCANModuleRS485.RTS | PwrCANModuleRS485.CTS`` will enable both, for full hardware flow control.


    .. note::
        It is possible to call ``init()`` multiple times on the same object in
        order to reconfigure  UART on the fly. That allows using single UART
        peripheral to serve different devices attached to different GPIO pins.
        Only one device can be served at a time in that case.
        Also do not call ``deinit()`` as it will prevent calling ``init()``
        again.

    UIFLOW2:

        |setup.png|


.. method:: PwrCANModuleRS485.deinit()

    Turn off the UART bus.

    .. note::
        You will not be able to call ``init()`` on the object after ``deinit()``.
        A new instance needs to be created in that case.

    UIFLOW2:

        |deinit.png|


.. method:: PwrCANModuleRS485.any()

    Returns an integer counting the number of characters that can be read without
    blocking.  It will return 0 if there are no characters available and a positive
    number if there are characters.  The method may return 1 even if there is more
    than one character available for reading.

    For more sophisticated querying of available characters use select.poll::

        poll = select.poll()
        poll.register(uart, select.POLLIN)
        poll.poll(timeout)

    UIFLOW2:

        |any.png|


.. method:: PwrCANModuleRS485.read([nbytes])

    Read characters.  If ``nbytes`` is specified then read at most that many bytes,
    otherwise read as much data as possible. It may return sooner if a timeout
    is reached. The timeout is configurable in the constructor.

    Return value: a bytes object containing the bytes read in.  Returns ``None``
    on timeout.

    UIFLOW2:

        |read_all.png|

        |read_bytes.png|


.. method:: PwrCANModuleRS485.readinto(buf[, nbytes])

    Read bytes into the ``buf``.  If ``nbytes`` is specified then read at most
    that many bytes.  Otherwise, read at most ``len(buf)`` bytes. It may return sooner if a timeout
    is reached. The timeout is configurable in the constructor.

    Return value: number of bytes read and stored into ``buf`` or ``None`` on
    timeout.

    UIFLOW2:

        |readinto.png|


.. method:: PwrCANModuleRS485.readline()

    Read a line, ending in a newline character. It may return sooner if a timeout
    is reached. The timeout is configurable in the constructor.

    Return value: the line read or ``None`` on timeout.

    UIFLOW2:

        |readline.png|


.. method:: PwrCANModuleRS485.write(buf)

    Write the buffer of bytes to the bus.

    Return value: number of bytes written or ``None`` on timeout.

    UIFLOW2:

        |write.png|

        |write_line.png|

        |write_list.png|


.. method:: PwrCANModuleRS485.sendbreak()

    Send a break condition on the bus. This drives the bus low for a duration
    longer than required for a normal transmission of a character.

    UIFLOW2:

        |sendbreak.png|


.. method:: PwrCANModuleRS485.flush()

    Waits until all data has been sent. In case of a timeout, an exception is raised. The timeout
    duration depends on the tx buffer size and the baud rate. Unless flow control is enabled, a timeout
    should not occur.

    .. note::

        For the rp2, esp8266 and nrf ports the call returns while the last byte is sent.
        If required, a one character wait time has to be added in the calling script.

    UIFLOW2:

        |flush.png|


.. method:: PwrCANModuleRS485.txdone()

    Tells whether all data has been sent or no data transfer is happening. In this case,
    it returns ``True``. If a data transmission is ongoing it returns ``False``.

    .. note::

        For the rp2, esp8266 and nrf ports the call may return ``True`` even if the last byte
        of a transfer is still being sent. If required, a one character wait time has to be
        added in the calling script.

    UIFLOW2:

        |txdone.png|
