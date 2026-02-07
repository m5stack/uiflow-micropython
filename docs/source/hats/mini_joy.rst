MiniJoyC Hat
============

.. include:: ../refs/hat.mini_joy.ref

The following products are supported:

    |MiniJoyCHat|


Micropython Example:

    .. literalinclude:: ../../../examples/hat/mini_joy/stickc_plus2_mini_joy_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |stickc_plus2_mini_joy_example.m5f2|


class MiniJoyHat
-----------------

Constructors
------------

.. class:: MiniJoyHat(i2c, address: int | list | tuple = 0x38)

    Create a new instance of the MiniJoyHat class.

    :param i2c: I2C bus
    :param address: I2C address

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: MiniJoyHat.get_x_raw() -> int

    Get the raw x-axis value.

    :return: x-axis value

    UIFLOW2:

        |get_x_raw.png|


.. method:: MiniJoyHat.get_y_raw() -> int

    Get the raw y-axis value.

    :return: y-axis value

    UIFLOW2:

        |get_y_raw.png|


.. method:: MiniJoyHat.get_x() -> int

    Get the x-axis value.

    :return: x-axis value

    UIFLOW2:

        |get_x.png|


.. method:: MiniJoyHat.get_y() -> int

    Get the y-axis value.

    :return: y-axis value

    UIFLOW2:

        |get_y.png|


.. method:: MiniJoyHat.swap_x(swap: bool = True) -> None

    Swap x-axis direction

    :param swap: True or False

    UIFLOW2:

        |swap_x.png|


.. method:: MiniJoyHat.swap_y(swap: bool = True) -> None

    Swap y-axis direction

    :param swap: True or False

    UIFLOW2:

        |swap_y.png|

.. method:: MiniJoyHat.get_button_status() -> bool

    Get the button status.

    :return: True or False

    UIFLOW2:

        |get_button_status.png|


.. method:: MiniJoyHat.get_firmware_version() -> str

    Get the firmware version.

    :return: firmware version

    UIFLOW2:

        |get_firmware_version.png|


.. method:: MiniJoyHat.set_i2c_address(address: int) -> None

    Set the I2C address.

    :param address: 0x01 ~ 0x7F

    UIFLOW2:

        |set_i2c_address.png|
