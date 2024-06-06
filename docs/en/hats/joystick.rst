Joystick Hat
============

.. include:: ../refs/hat.joystick.ref

The following products are supported:

    |JoystickHat|


class JoystickHat
-----------------

Constructors
------------

.. class:: JoystickHat(i2c, address: int | list | tuple = 0x38)

    Create a new instance of the JoystickHat class.

    :param i2c: I2C bus
    :param address: I2C address

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: JoystickHat.get_x_raw() -> int

    Get the raw x-axis value.

    :return: x-axis value

    UIFLOW2:

        |get_x_raw.svg|


.. method:: JoystickHat.get_y_raw() -> int

    Get the raw y-axis value.

    :return: y-axis value

    UIFLOW2:

        |get_y_raw.svg|


.. method:: JoystickHat.get_x() -> int

    Get the x-axis value.

    :return: x-axis value

    UIFLOW2:

        |get_x.svg|


.. method:: JoystickHat.get_y() -> int

    Get the y-axis value.

    :return: y-axis value

    UIFLOW2:

        |get_y.svg|


.. method:: JoystickHat.swap_x(swap: bool = True) -> None

    Swap x-axis direction

    :param swap: True or False

    UIFLOW2:

        |swap_x.svg|


.. method:: JoystickHat.swap_y(swap: bool = True) -> None

    Swap y-axis direction

    :param swap: True or False

    UIFLOW2:

        |swap_y.svg|

.. method:: JoystickHat.get_button_status() -> bool

    Get the button status.

    :return: True or False

    UIFLOW2:

        |get_button_status.svg|
