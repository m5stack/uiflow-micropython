UART
====

.. include:: ../refs/hardware.uart.ref

UART implements the standard UART/USART duplex serial communications protocol. At the physical level it consists of 2 lines: RX and TX. The unit of communication is a character (not to be confused with a string character) which can be 8 or 9 bits wide.

UiFlow2 Example
---------------

Echo
^^^^

Open the |cores3_echo_exmaple.m5f2| project in UiFlow2.

This example demonstrates how to utilize UART interfaces by echoing back to the
sender any data received on configured UART.

UiFlow2 Code Block:

    |cores3_echo_exmaple.png|

Example output:

    None



MicroPython Example
-------------------

Echo
^^^^

This example demonstrates how to utilize UART interfaces by echoing back to the
sender any data received on configured UART.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/hardware/uart/cores3_echo_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

class UART
^^^^^^^^^^

.. _hardware.UART:

.. class:: UART(id, baudrate=9600, bits=8, parity=None, stop=1, *, ...)

    Construct a UART object of the given id.

    For more parameters, please refer to init.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hadrware import UART

            uart1 = UART(1, baudrate=115200, bits=8, parity=None, stop=1, tx=9, rx=10)


    .. method:: UART.init(baudrate=9600, bits=8, parity=None, stop=1, *, ...)

        Initialise the UART bus with the given parameters.

        :param int baudrate: the clock rate.
        :param int bits: the number of bits per character, 7, 8 or 9.
        :param parity: the parity, ``None``, 0 (even) or 1 (odd).
        :type parity: None or int
        :param int stop: the number of stop bits, 1 or 2.
        :keyword tx: the TX pin to use.
        :type tx: Pin or int
        :keyword rx: the RX pin to use.
        :type rx: Pin or int
        :keyword rts: the RTS (output) pin to use for hardware receive flow control.
        :type rts: Pin or int
        :keyword cts: the CTS (input) pin to use for hardware transmit flow control.
        :type cts: Pin or int
        :keyword int txbuf: the length in characters of the TX buffer.
        :keyword int rxbuf: the length in characters of the RX buffer.
        :keyword int timeout: the time to wait for the first character (in ms).
        :keyword int timeout_char: the time to wait between characters (in ms).
        :keyword int invert: which lines to invert.

            - ``0`` will not invert lines (idle state of both lines is logic high).

            - ``UART.INV_TX`` will invert TX line (idle state of TX line now logic low).

            - ``UART.INV_RX`` will invert RX line (idle state of RX line now logic low).

            - ``UART.INV_TX | UART.INV_RX`` will invert both lines (idle state at logic low).

        :keyword int flow: which hardware flow control signals to use. The value is a bitmask.

            - ``0`` will ignore hardware flow control signals.

            - ``UART.RTS`` will enable receive flow control by using the RTS output pin to signal if the receive FIFO has sufficient space to accept more data.

            - ``UART.CTS`` will enable transmit flow control by pausing transmission when the CTS input pin signals that the receiver is running low on buffer space.

            - ``UART.RTS | UART.CTS`` will enable both, for full hardware flow control.

        :keyword int mode: the mode of the UART. The value is a bitmask.

            - ``UART.MODE_UART`` specifies regular UART mode.

            - ``UART.MODE_RS485_HALF_DUPLEX`` specifies half duplex RS485 UART mode control by RTS pin.

            - ``UART.MODE_IRDA`` specifies IRDA UART mode.

            - ``UART.MODE_RS485_COLLISION_DETECT`` specifies RS485 collision detection UART mode (used for test purposes).

            - ``UART.MODE_RS485_APP_CTRL`` specifies application control RS485 UART mode (used for test purposes).

        .. note::
            It is possible to call ``init()`` multiple times on the same object in
            order to reconfigure  UART on the fly. That allows using single UART
            peripheral to serve different devices attached to different GPIO pins.
            Only one device can be served at a time in that case.
            Also do not call ``deinit()`` as it will prevent calling ``init()``
            again.

        UiFlow2 Code Block:

            |setup.png|

        MicroPython Code Block:

            .. code-block:: python

                uart1.init(baudrate=115200, bits=8, parity=None, stop=1, tx=9, rx=10)


    .. method:: UART.deinit()

        Turn off the UART bus.

        .. note::
            You will not be able to call ``init()`` on the object after ``deinit()``.
            A new instance needs to be created in that case.

        UiFlow2 Code Block:

            |deinit.png|

        MicroPython Code Block:

            .. code-block:: python

                uart1.deinit()


    .. method:: UART.any()

        Returns an integer counting the number of characters that can be read without
        blocking.  It will return 0 if there are no characters available and a positive
        number if there are characters.  The method may return 1 even if there is more
        than one character available for reading.

        :return: the number of characters available for reading.
        :rtype: int

        For more sophisticated querying of available characters use select.poll::

            poll = select.poll()
            poll.register(uart, select.POLLIN)
            poll.poll(timeout)

        UiFlow2 Code Block:

            |any.png|

        MicroPython Code Block:

            .. code-block:: python

                print(uart1.any())


    .. method:: UART.read([nbytes])

        Read characters.  If ``nbytes`` is specified then read at most that many bytes,
        otherwise read as much data as possible. It may return sooner if a timeout
        is reached. The timeout is configurable in the constructor.

        :return: a bytes object containing the bytes read in.  Returns ``None`` on timeout.
        :rtype: bytes or None

        UiFlow2 Code Block:

            |read_all.png|

            |read_bytes.png|

            |read_raw_data.png|

        MicroPython Code Block:

            .. code-block:: python

                print(uart1.read())


    .. method:: UART.readinto(buf[, nbytes])

        Read bytes into the ``buf``.  If ``nbytes`` is specified then read at most
        that many bytes.  Otherwise, read at most ``len(buf)`` bytes. It may return sooner if a timeout
        is reached. The timeout is configurable in the constructor.

        :return:  number of bytes read and stored into ``buf`` or ``None`` on timeout.
        :rtype: int or None

        UiFlow2 Code Block:

            |readinto.png|

        MicroPython Code Block:

            .. code-block:: python

                buf = bytearray(10)
                uart1.readinto(buf)


    .. method:: UART.readline()

        Read a line, ending in a newline character. It may return sooner if a timeout
        is reached. The timeout is configurable in the constructor.

        :return: the line read or ``None`` on timeout.
        :rtype: str or None

        UiFlow2 Code Block:

            |readline.png|

        MicroPython Code Block:

            .. code-block:: python

                print(uart1.readline())


    .. method:: UART.write(buf)

        Write the buffer of bytes to the bus.

        :param buf: the buffer of bytes to write.
        :type buf: bytes or bytearray or str

        :return: number of bytes written or ``None`` on timeout.
        :rtype: int or None

        UiFlow2 Code Block:

            |write.png|

            |write1.png|

            |write_line.png|

            |write_list.png|

            |write_raw_data.png|

            |write_raw_data_list.png|

        MicroPython Code Block:

            .. code-block:: python

                uart1.write('1234!')


    .. method:: UART.sendbreak()

        Send a break condition on the bus. This drives the bus low for a duration
        longer than required for a normal transmission of a character.

        UiFlow2 Code Block:

            |sendbreak.png|

        MicroPython Code Block:

            .. code-block:: python

                uart1.sendbreak()


    .. method:: UART.flush()

        Waits until all data has been sent. In case of a timeout, an exception is raised. The timeout
        duration depends on the tx buffer size and the baud rate. Unless flow control is enabled, a timeout
        should not occur.

        .. note::

            For the rp2, esp8266 and nrf ports the call returns while the last byte is sent.
            If required, a one character wait time has to be added in the calling script.

        UiFlow2 Code Block:

            |flush.png|

        MicroPython Code Block:

            .. code-block:: python

                uart1.flush()


    .. method:: UART.txdone()

        Tells whether all data has been sent or no data transfer is happening. In this case,
        it returns ``True``. If a data transmission is ongoing it returns ``False``.

        .. note::

            For the rp2, esp8266 and nrf ports the call may return ``True`` even if the last byte
            of a transfer is still being sent. If required, a one character wait time has to be
            added in the calling script.

        UiFlow2 Code Block:

            |txdone.png|

        MicroPython Code Block:

            .. code-block:: python

                print(uart1.txdone())


    .. method:: UART.irq(handler=None, trigger=0, hard=False)

        Configure an interrupt handler to be called when a UART event occurs.

        :param func handler: an optional function to be called when the interrupt event triggers.  The handler must take exactly one argument which is the ``UART`` instance.

        :param int trigger: configures the event(s) which can generate an interrupt. Possible values are a mask of one or more of the following:

            - ``UART.IRQ_RXIDLE`` interrupt after receiving at least one character and then the RX line goes idle.

            - ``UART.IRQ_RX`` interrupt after each received character.

            - ``UART.IRQ_TXIDLE`` interrupt after or while the last character(s) of a message are or have been sent.

            - ``UART.IRQ_BREAK`` interrupt when a break state is detected at RX

        :param bool hard: if true a hardware interrupt is used.  This reduces the delay between the pin change and the handler being called. Hard interrupt handlers may not allocate memory; see :ref:`isr_rules`.

        :return: Returns an irq object.

        Due to limitations of the hardware not all trigger events are available on all ports.

        .. table:: Availability of triggers
            :align: center

            ============== ========== ====== ========== =========
            Port / Trigger IRQ_RXIDLE IRQ_RX IRQ_TXIDLE IRQ_BREAK
            ============== ========== ====== ========== =========
            CC3200                      yes
            ESP32            yes        yes                yes
            MIMXRT           yes                yes
            NRF                         yes     yes
            RENESAS-RA       yes        yes
            RP2              yes                yes        yes
            SAMD             yes        yes     yes
            STM32            yes        yes
            ============== ========== ====== ========== =========

        .. note::
            - The ESP32 port does not support the option hard=True.

            - The rp2 port's UART.IRQ_TXIDLE is only triggered when the message
              is longer than 5 characters and the trigger happens when still 5 characters
              are to be sent.

            - The rp2 port's UART.IRQ_BREAK needs receiving valid characters for triggering
              again.

            - The SAMD port's UART.IRQ_TXIDLE is triggered while the last character is sent.

            - On STM32F4xx MCU's, using the trigger UART.IRQ_RXIDLE the handler will be called once
              after the first character and then after the end of the message, when the line is
              idle.


        Availability: cc3200, esp32, mimxrt, nrf, renesas-ra, rp2, samd, stm32.


    .. data:: UART.RTS
    .. data:: UART.CTS

        Flow control options.


    .. data:: UART.MODE_UART
    .. data:: UART.MODE_RS485_HALF_DUPLEX
    .. data:: UART.MODE_IRDA
    .. data:: UART.MODE_RS485_COLLISION_DETECT
    .. data:: UART.MODE_RS485_APP_CTRL

        UART mode options.


    .. data:: UART.IRQ_RXIDLE
    .. data:: UART.IRQ_RX
    .. data:: UART.IRQ_TXIDLE
    .. data:: UART.IRQ_BREAK

        IRQ trigger sources.
