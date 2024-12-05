DMX512 Module
===========

.. include:: ../refs/module.dmx.ref

DMX-Base is a functional base specially designed for DMX-512 data transmission scenarios, communicating and enabling control with M5 host through serial port, equipped with XLR-5 and XLR-3 male and female interfaces, convenient for users to connect DMX devices with different interfaces, in addition, the module has HT3.96 pitch 485 interface to facilitate connection to Expansion 485 devices.

Support the following products:

|dmx|

Micropython Example Send Data:

    .. literalinclude:: ../../../examples/module/dmx/dmx512_core2_send_example.py
        :language: python
        :linenos:


Micropython Example Receive Data:

    .. literalinclude:: ../../../examples/module/dmx/dmx512_core2_receive_example.py
        :language: python
        :linenos:



UIFLOW2 Master Example:

    |tx_example.png|

UIFLOW2 Slave Example:

    |rx_example.png|

.. only:: builder_html

    |dmx512_core2_send_example.m5f2|

    |dmx512_core2_receive_example.m5f2|


class DMX512Module
----------------

Constructors
------------

.. class:: DMX512Module(id, mode = DMX_MASTER)

    Initializes the DMX512 module with a specified UART ID and port pins.

    :param Literal[0,1,2] id: UART device ID(DMX port id).
    :param int mode: Operating mode (1 for Master, 2 for Slave).

    UIFLOW2:

        |init.png|

Methods
-------

.. method:: DMX512Module.dmx_init(mode) -> None

    Initializes the DMX512 communication with UART pins and mode.

    :param  mode: Operating mode (1 for Master, 2 for Slave).

    UIFLOW2:

        |dmx_init.png|

.. method:: DMX512Module.deinit() -> None

    Deinitializes the DMX512 module and stops any ongoing operations.

    UIFLOW2:

        |deinit.png|

.. method:: DMX512Module.write_data(channel, data) -> None

    Updates the data for a specified DMX channel. Data is sent on the next update cycle.

    :param  channel: DMX channel number (1-512).
    :param  data: Data value to be sent (0-255).
        @raises ValueError if the channel number is out of range.

    UIFLOW2:

        |write_data.png|


.. method:: DMX512Module.clear_buffer() -> None

    Clears the DMX buffer and resets the data.

    UIFLOW2:

        |clear_buffer.png|

.. method:: DMX512Module.read_data(channel) -> int

    Reads data from a specified DMX channel in Slave mode.

    :param  channel: DMX channel number (1-512).

    UIFLOW2:

        |read_data.png|

.. method:: DMX512.receive_none_block() -> None

    Starts non-blocking data reception for the specified channels with associated callbacks.

    UIFLOW2:

        |receive_none_block.png|

.. method:: DMX512Module.attach_channel(channel, callback) -> None

    Attaches a callback function to a specified DMX channel.

    :param channel: DMX channel number (1-512) to attach the callback to.
    :param callback: The function to be called when data changes on the specified channel.

    UIFLOW2:

        |receive_data_event.png|

.. method:: DMX512.stop_receive() -> None

    Stops the non-blocking data reception task.

    UIFLOW2:

        |stop_receive.png|

.. method:: DMX512Module.detach_channel(channel) -> None

    Detaches the callback function from a specified DMX channel.

    :param channel: DMX channel number (1-512) to detach the callback from.
