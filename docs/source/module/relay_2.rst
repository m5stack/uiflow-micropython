
Relay2 Module
=============

.. include:: ../refs/module.relay_2.ref

Support the following products:

|Relay2Module|

Micropython Example:

    .. literalinclude:: ../../../examples/module/relay2/relay2_fire_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

class Relay2Module
------------------

Constructors
------------

.. class:: Relay2Module(address)

    Initialize the 2Relay Module with the specified I2C address.

    :param int|list|tuple address: I2C address of the Relay2Module.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: Relay2Module.set_relay_state(num, state) -> None

    Set the state of a specific relay.

    :param int num: The relay number (1 or 2).
    :param bool state: True to turn on, False to turn off.

    UIFLOW2:

        |set_relay_state.png|

.. method:: Relay2Module.get_relay_status(num) -> bool

    Get the status of a specific relay.

    :param int num: The relay number (1 or 2).

    UIFLOW2:

        |get_relay_status.png|

.. method:: Relay2Module.set_all_relay_state(state) -> None

    Set the state of both relays simultaneously.

    :param bool state: True to turn on both relays, False to turn off both relays.

    UIFLOW2:

        |set_all_relay_state.png|

.. method:: Relay2Module.get_firmware_version() -> int

    Get the firmware version of the Relay2 Module.


    UIFLOW2:

        |get_firmware_version.png|

.. method:: Relay2Module.set_i2c_address(addr) -> None

    Set a new I2C address(0x08~0x77) for the Relay2 Module.

    :param int addr: The new I2C address to set.

    UIFLOW2:

        |set_i2c_address.png|

.. method:: Relay2Module.get_i2c_address() -> int

    Get the current I2C address of the Relay2 Module.


    UIFLOW2:

        |get_i2c_address.png|





