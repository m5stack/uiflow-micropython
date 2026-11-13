CardKB Unit
===========

.. include:: ../refs/unit.cardkb.ref

Support the following products:

    ================== ==================
    |CardKB Unit|      |CardKB Unit v1.1|
    ================== ==================


Micropython Example:

    .. literalinclude:: ../../../examples/unit/cardkb/cores3_cardkb_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_cardkb_example.m5f2|


Key codes
---------

Import the CardKB character constants with ``from unit import KeyCode``.
For example, ``KeyCode.KEYCODE_ENTER`` is 10 (0x0A). These names exist in
UiFlow2 and differ from ``usb.device.hid.KeyCode``. See
`Keyboard key codes <../hardware/keycode.html>`_ for the complete list and the I2C versus
UART/ESP-NOW return-value distinction.


class CardKBUnit
----------------

Constructors
------------

.. class:: CardKBUnit(*args, mode=CardKBUnit.CardKB_I2C_MODE, **kwargs)

    Factory returning the driver for the selected communication mode.
    The keyboard firmware and connection must already support that mode;
    selecting ``mode`` does not reconfigure the keyboard firmware.

    :param int mode: ``CardKB_I2C_MODE`` (0, default), ``CardKB_UART_MODE`` (1), or ``CardKB_ESP_NOW_MODE`` (2).
    :return: ``unit.cardkb.CardKBI2C`` for I2C mode,
        ``unit.cardkb.CardKBUART`` for UART mode, or
        ``unit.cardkb.CardKBESPNOW`` for ESP-NOW mode.
    :raises ValueError: If ``mode`` is not one of the three supported values.

    These are the concrete returned classes, not subclasses of ``CardKBUnit``.
    The methods below belong to the returned instance; for example, call
    ``cardkb.get_key()`` rather than looking up ``CardKBUnit.get_key``.

    **I2C:** pass the I2C object as the first positional argument. The optional
    ``address`` keyword defaults to ``0x5F`` and applies only to I2C.

    .. code-block:: python

        from unit import CardKBUnit
        from hardware import I2C, Pin

        # Choose GPIO pins for your controller.
        i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
        cardkb = CardKBUnit(i2c0, address=0x5F, mode=CardKBUnit.CardKB_I2C_MODE)

    **UART:** pass the UART ID as the first positional argument and
    ``port=(rx_pin, tx_pin)``. The driver uses 115200 baud, 8N1.

    .. code-block:: python

        cardkb = CardKBUnit(2, port=(33, 32), mode=CardKBUnit.CardKB_UART_MODE)

    **ESP-NOW:** no bus argument is needed.

    .. code-block:: python

        cardkb = CardKBUnit(mode=CardKBUnit.CardKB_ESP_NOW_MODE)


    UIFLOW2:

        |init.png|


.. _unit.CardKBUnit.Methods:

Methods
-------

.. method:: CardKBUnit.get_key()

    Read the key value.

    :return: An integer key code in I2C mode, or a ``(key_id, key_state)``
        tuple in UART and ESP-NOW modes. Returns ``None`` when no key is available.
        The state is ``CardKBUnit.KEY_STATE_PRESS`` or ``CardKBUnit.KEY_STATE_RELEASE``.

    In I2C mode the integer is a character/special-key value compatible
    with the CardKB ``KeyCode.KEYCODE_*`` constants. V2 UART/ESP-NOW key IDs
    are raw HID usage IDs; see `Keyboard key codes <../hardware/keycode.html>`_ before converting
    or comparing them.

    UIFLOW2:

        |get_key.png|


.. method:: CardKBUnit.get_string() -> str

    Read the key string.

    :return: key string, str

    UIFLOW2:

        |get_string.png|


.. method:: CardKBUnit.is_pressed() -> bool

    Check if the key is pressed.

    :return: True if the key is pressed, False otherwise

    UIFLOW2:

        |is_pressed.png|


.. method:: CardKBUnit.set_callback(handler)

    Set the key press event callback.

    :param handler: Callback function. I2C callbacks receive the CardKB instance;
        UART and ESP-NOW callbacks receive a key tuple.

    UIFLOW2:

        |pressed_event.png|

    Example:

    .. code-block:: python

        from unit import CardKBUnit

        def cb(keyboard):
            print(keyboard.get_key())

        cardkb = CardKBUnit(i2c)
        cardkb.set_callback(cb)
        while True:
            cardkb.tick()


.. method:: CardKBUnit.tick()

    Update the key status.

    UIFLOW2:

        |tick.png|

