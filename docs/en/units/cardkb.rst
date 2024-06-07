CardKB Unit
===========

.. include:: ../refs/unit.cardkb.ref

Support the following products:

    ================== ==================
    |CardKB Unit|      |CardKB Unit v1.1|
    ================== ==================


class CardKBUnit
----------------

Constructors
------------

.. class:: CardKBUnit(i2c: I2C, address: int | list | tuple = 0x5F)

    Create a CardKBUnit object.

    :param i2c: I2C object
    :param address: I2C address, 0x5F by default

    UIFLOW2:

        |init.svg|


.. _unit.CardKBUnit.Methods:

Methods
-------

.. method:: CardKBUnit.get_key() -> int

    Read the key value.

    :return: key value, int

    UIFLOW2:

        |get_key.svg|


.. method:: CardKBUnit.get_string() -> str

    Read the key string.

    :return: key string, str

    UIFLOW2:

        |get_string.svg|


.. method:: CardKBUnit.is_pressed() -> bool

    Check if the key is pressed.

    :return: True if the key is pressed, False otherwise

    UIFLOW2:

        |is_pressed.svg|


.. method:: CardKBUnit.set_callback(handler)

    Set the key press event callback.

    :param handler: callback function

    UIFLOW2:

        |pressed_event.svg|

    Example:

    .. code-block:: python

        from cardkb_unit import CardKBUnit

        def cb(key):
            print(key)

        cardkb = CardKBUnit(i2c)
        cardkb.set_callback(cb)
        while True:
            cardkb.tick()


.. method:: CardKBUnit.tick()

    Update the key status.

    UIFLOW2:

        |tick.svg|

