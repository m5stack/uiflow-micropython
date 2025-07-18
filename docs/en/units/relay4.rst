Relay4 Unit
===========

.. include:: ../refs/unit.relay4.ref

4-Relay unit is an integrated 4-way relay module which can be controlled by I2C
protocol. The maximum control voltage of each relay is AC-250V/DC-28V, the rated
current is 10A and the instantaneous current can hold up to 16A. Each relay can
be controlled independently, each on it's own. Each relay has status (LED)
indictor as well to show the state of the relay at any given time.


Support the following products:

    |Relay4Unit|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/relay4/cores3_relay4_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |cores3_relay4_example.m5f2|


class Relay4Unit
----------------

Constructors
------------

.. class:: Relay4Unit(i2c: I2C, address: int | list | tuple = 0x26)

    Initialize the Relay4Unit object.

    :param I2C i2c: I2C port to use.
    :param int address: I2C address of the Relay4Unit.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: Relay4Unit.set_mode(mode: int)

    Set the mode of the relay.

    :param int mode: The mode of the relay

        Options:
        - ``Relay4Unit.ASYNC_MODE``: async
        - ``Relay4Unit.SYNC_MODE``: sync

    UIFLOW2:

        |set_mode.png|


.. method:: Relay4Unit.get_mode() -> int

    Get the mode of the relay.

    :return: The mode of the relay

        Options:
        - ``Relay4Unit.ASYNC_MODE``: async
        - ``Relay4Unit.SYNC_MODE``: sync

    UIFLOW2:

        |get_mode.png|


.. method:: Relay4Unit.get_led_state(n: int) -> int

    Get the state of the LED.

    :param int n: The number of the LED.

    UIFLOW2:

        |get_led_state.png|


.. method:: Relay4Unit.set_led_state(n: int, state: int) -> None

    Set the state of the LED.

    :param int n: The number of the LED.
    :param int state: The state of the LED.

    UIFLOW2:

        |set_led_state.png|


.. method:: Relay4Unit.get_relay_state(n: int) -> int

    Get the state of the relay.

    :param int n: The number of the relay.

    :return: The state of the relay.

    UIFLOW2:

        |get_relay_state.png|


.. method:: Relay4Unit.set_relay_state(n: int, state: int) -> None

    Set the state of the relay.

    :param int n: The number of the relay.
    :param int state: The state of the relay.

    UIFLOW2:

        |set_relay_state.png|


.. method:: Relay4Unit.set_relay_all(state: int) -> None

    Set the state of all the relay.

    :param int state: The state of the relay.

    UIFLOW2:

        |set_relay_all.png|
