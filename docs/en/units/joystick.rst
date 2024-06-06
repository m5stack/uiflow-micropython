Joystick Unit
=============

.. include:: ../refs/unit.joystick.ref

The following products are supported:

    |JoystickUnit|


class JoystickUnit
------------------

Constructors
------------

.. class:: JoystickUnit(i2c, address: int | list | tuple = 0x38)

    Create a new instance of the JoystickUnit class.

    :param i2c: I2C bus
    :param address: I2C address

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: JoystickUnit.get_x_raw() -> int

    Get the raw x-axis value.

    :return: x-axis value

    UIFLOW2:

        |get_x_raw.svg|


.. method:: JoystickUnit.get_y_raw() -> int

    Get the raw y-axis value.

    :return: y-axis value

    UIFLOW2:

        |get_y_raw.svg|


.. method:: JoystickUnit.get_x() -> int

    Get the x-axis value.

    :return: x-axis value

    UIFLOW2:

        |get_x.svg|


.. method:: JoystickUnit.get_y() -> int

    Get the y-axis value.

    :return: y-axis value

    UIFLOW2:

        |get_y.svg|


.. method:: JoystickUnit.swap_x(swap: bool = True) -> None

    Swap x-axis direction

    :param swap: True or False

    UIFLOW2:

        |swap_x.svg|


.. method:: JoystickUnit.swap_y(swap: bool = True) -> None

    Swap y-axis direction

    :param swap: True or False

    UIFLOW2:

        |swap_y.svg|

.. method:: JoystickUnit.get_button_status() -> bool

    Get the button status.

    :return: True or False

    UIFLOW2:

        |get_button_status.svg|
