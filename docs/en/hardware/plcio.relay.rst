Relay
=====

.. include:: ../refs/hardware.plcio.relay.ref

Relay is used to control the relay of host devices.


UiFlow2 Example
---------------

Relay control
^^^^^^^^^^^^^

Open the |stamplc_relay_example.m5f2| project in UiFlow2.

This example demonstrates how to use a button to control the state of a relay and display the relay's state value on the screen.

UiFlow2 Code Block:

    |stamplc_relay_example.png|

Example output:

    None


MicroPython Example
-------------------

Relay control
^^^^^^^^^^^^^

This example demonstrates how to use a button to control the state of a relay and display the relay's state value on the screen.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/hardware/plcio/relay/stamplc_relay_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

Relay
^^^^^

.. class:: Relay(id: int)

    Initialize a relay object.

    :param int id: The ID of the relay. The range of ID is 1-4.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from hadrware import Relay

            relay = Relay(1)


    .. method:: Relay.on() -> None

        Turn on the relay.

        UiFlow2 Code Block:

            |on.png|

        MicroPython Code Block:

            .. code-block:: python

                relay.on()


    .. method:: Relay.off() -> None

        Turn off the relay.

        UiFlow2 Code Block:

            |off.png|

        MicroPython Code Block:

            .. code-block:: python

                relay.off()


    .. method:: Relay.value() -> int

        Get the value of the relay.

        :return: The value of the relay.
        :rtype: int

        UiFlow2 Code Block:

            |set_value.png|

            |get_value.png|

        MicroPython Code Block:

            .. code-block:: python

                relay.value(1)
                relay.value()


    .. method:: Relay.get_status() -> bool

        Get the status of the relay.

        :return: The status of the relay.
        :rtype: bool

        UiFlow2 Code Block:

            |get_status.png|

        MicroPython Code Block:

            .. code-block:: python

                relay.get_status()

    .. method:: Relay.set_status(status: bool) -> None

        Set the status of the relay.

        :param bool status: The status of the relay.

        UiFlow2 Code Block:

            |set_status.png|

        MicroPython Code Block:

            .. code-block:: python

                relay.set_status(True)
