Encoder Unit
============

.. include:: ../refs/unit.encoder.ref

The following products are supported:

    |Encoder|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/encoder/encoder_stickc_plus2.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.svg|


.. .. only:: builder_html

.. ..     |earth_core_example.m5f2|


class EncoderUnit
-----------------

Constructors
------------

.. class:: EncoderUnit(i2c, address: int | list | tuple = 0x40)

    Creates a Rotary object.

    :param i2c: I2C object.
    :param address: I2C address, Default is 0x40.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: EncoderUnit.get_rotary_status() -> bool

    Gets the rotation status of the Rotary object.

    UIFLOW2:

        |get_rotary_status.svg|


.. method:: EncoderUnit.get_rotary_value() -> int

    Gets the rotation value of the Rotary object.

    UIFLOW2:

        |get_rotary_value.svg|


.. method:: EncoderUnit.get_rotary_increments() -> int

    Gets the rotation increment of the Rotary object. Can be used to determine
    the direction of rotation.

    UIFLOW2:

        |get_rotary_increments.svg|


.. method:: EncoderUnit.reset_rotary_value() -> None

    Resets the rotation value of the Rotary object.

    UIFLOW2:

        |reset_rotary_value.svg|


.. method:: EncoderUnit.set_rotary_value(new_value: int) -> None

    Sets the rotation value of the Rotary object.

    :param int new_value: adjust the current value.

    UIFLOW2:

        |set_rotary_value.svg|


.. method:: EncoderUnit.get_button_status() -> bool

    Get the current status of the rotary encoder keys.

    UIFLOW2:

        |get_button_status.svg|


.. method:: EncoderUnit.set_color(index, rgb: int) -> None

    Set the color of the LED

    :param int index: the index of the LED, 1 or 2.
    :param int rgb: the color of the LED, 0x000000 - 0xFFFFFF.

    UIFLOW2:

        |set_color.svg|


.. method:: EncoderUnit.fill_color(rgb: int) -> None

    Set the color of the LED

    :param int rgb: the color of the LED, 0x000000 - 0xFFFFFF.

    UIFLOW2:

        |fill_color.svg|

