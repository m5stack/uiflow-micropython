Scroll Unit
===========

.. include:: ../refs/unit.scroll.ref

The following products are supported:

    |Scroll|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/scroll/cores3_scroll_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_scroll_example.m5f2|


class ScrollUnit
-----------------

Constructors
------------

.. class:: ScrollUnit(i2c, address: int | list | tuple = 0x40)

    Creates a Rotary object.

    :param i2c: I2C object.
    :param address: I2C address, Default is 0x40.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ScrollUnit.get_rotary_status() -> bool

    Gets the rotation status of the Rotary object.

    UIFLOW2:

        |get_rotary_status.png|


.. method:: ScrollUnit.get_rotary_value() -> int

    Gets the rotation value of the Rotary object.

    UIFLOW2:

        |get_rotary_value.png|


.. method:: ScrollUnit.get_rotary_increments() -> int

    Gets the rotation increment of the Rotary object. Can be used to determine
    the direction of rotation.

    UIFLOW2:

        |get_rotary_increments.png|


.. method:: ScrollUnit.reset_rotary_value() -> None

    Resets the rotation value of the Rotary object.

    UIFLOW2:

        |reset_rotary_value.png|


.. method:: ScrollUnit.set_rotary_value(new_value: int) -> None

    Sets the rotation value of the Rotary object.

    :param int new_value: adjust the current value.

    UIFLOW2:

        |set_rotary_value.png|


.. method:: ScrollUnit.get_button_status() -> bool

    Get the current status of the rotary encoder keys.

    UIFLOW2:

        |get_button_status.png|


.. method:: ScrollUnit.fill_color(rgb: int) -> None

    Set the color of the LED

    :param int rgb: the color of the LED, 0x000000 - 0xFFFFFF.

    UIFLOW2:

        |fill_color.png|


.. method:: ScrollUnit.get_bootloader_version() -> str

    Get the bootloader version.

    :return: bootloader version

    UIFLOW2:

        |get_bootloader_version.png|


.. method:: ScrollUnit.get_firmware_version() -> str

    Get the firmware version.

    :return: firmware version

    UIFLOW2:

        |get_firmware_version.png|
