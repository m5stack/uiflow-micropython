JoyC Hat
========

.. include:: ../refs/hat.joyc.ref

The following products are supported:

    |JoyCHat|


Micropython Example:

    .. literalinclude:: ../../../examples/hat/joyc/stickc_plus2_joyc_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |stickc_plus2_joyc_example.m5f2|


class JoyCHat
-------------

Constructors
------------

.. class:: JoyCHat(i2c, address: int | list | tuple = 0x38)

    Create a new instance of the JoyCHat class.

    :param i2c: I2C bus
    :param address: I2C address

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: JoyCHat.get_x_raw(channel: int = 0) -> int

    Get the raw x-axis value.

    :param channel: 0 or 1

    :return: x-axis value

    UIFLOW2:

        |get_x_raw.png|


.. method:: JoyCHat.get_y_raw(channel: int = 0) -> int

    Get the raw y-axis value.

    :param channel: 0 or 1

    :return: y-axis value

    UIFLOW2:

        |get_y_raw.png|


.. method:: JoyCHat.get_x(channel: int = 0) -> int

    Get the x-axis value.

    :param channel: 0 or 1

    :return: x-axis value

    UIFLOW2:

        |get_x.png|


.. method:: JoyCHat.get_y(channel: int = 0) -> int

    Get the y-axis value.

    :param channel: 0 or 1

    :return: y-axis value

    UIFLOW2:

        |get_y.png|


.. method:: JoyCHat.swap_x(swap: bool = True) -> None

    Swap x-axis direction

    :param swap: True or False

    UIFLOW2:

        |swap_x.png|


.. method:: JoyCHat.swap_y(swap: bool = True) -> None

    Swap y-axis direction

    :param swap: True or False

    UIFLOW2:

        |swap_y.png|

.. method:: JoyCHat.get_button_status(channel: int = 0) -> bool

    Get the button status.

    :param channel: 0 or 1
    :return: True or False

    UIFLOW2:

        |get_button_status.png|


.. method:: JoyCHat.fill_color() -> None

    Fill the screen with a color.

    UIFLOW2:

        |fill_color.png|
