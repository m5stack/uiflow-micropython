MiniEncoderC Hat
================

.. include:: ../refs/hat.mini_encoder.ref

The following products are supported:

    |Encoder|

Micropython Example:

    .. literalinclude:: ../../../examples/hat/mini_encoder/mini_encoder_stickc_plus2.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.svg|


.. .. only:: builder_html

.. ..     |earth_core_example.m5f2|


class MiniEncoderCHat
---------------------

Constructors
------------

.. class:: MiniEncoderCHat(i2c, address: int | list | tuple = 0x42)

    Creates a Rotary object.

    :param i2c: I2C object.
    :param address: I2C address, Default is 0x40.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: MiniEncoderCHat.get_rotary_status() -> bool

    Gets the rotation status of the Rotary object.

    UIFLOW2:

        |get_rotary_status.svg|


.. method:: MiniEncoderCHat.get_rotary_value() -> int

    Gets the rotation value of the Rotary object.

    UIFLOW2:

        |get_rotary_value.svg|


.. method:: MiniEncoderCHat.get_rotary_increments() -> int

    Gets the rotation increment of the Rotary object. Can be used to determine
    the direction of rotation.

    UIFLOW2:

        |get_rotary_increments.svg|

.. method:: MiniEncoderCHat.reset_rotary_value() -> None

    Resets the rotation value of the Rotary object.

    UIFLOW2:

        |reset_rotary_value.svg|

.. method:: MiniEncoderCHat.get_button_status() -> bool

    Get the current status of the rotary encoder keys.

    UIFLOW2:

        |get_button_status.svg|


.. method:: MiniEncoderCHat.set_rotary_value(new_value: int) -> None

    Sets the rotation value of the Rotary object.

    :param int new_value: adjust the current value.

    UIFLOW2:

        |set_rotary_value.svg|

.. method:: MiniEncoderCHat.fill_color(rgb: int) -> None

    Set the color of the LED

    :param int rgb: the color of the LED, 0x000000 - 0xFFFFFF.

    UIFLOW2:

        |fill_color.svg|


.. method:: MiniEncoderCHat.read_fw_version() -> str

    Get the firmware version of the device.

    UIFLOW2:

        |read_fw_version.svg|


.. method:: MiniEncoderCHat.set_address(address) -> None

    Set the I2C address of the device.

    UIFLOW2:

        |set_address.svg|
