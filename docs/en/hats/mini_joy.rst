MiniJoyC Hat
============

.. include:: ../refs/hat.mini_joy.ref

The following products are supported:

    |MiniJoyCHat|


class MiniJoyHat
-----------------

Constructors
------------

.. class:: MiniJoyHat(i2c, address: int | list | tuple = 0x38)

    Create a new instance of the MiniJoyHat class.

    :param i2c: I2C bus
    :param address: I2C address

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: MiniJoyHat.get_x_raw() -> int

    Get the raw x-axis value.

    :return: x-axis value

    UIFLOW2:

        |get_x_raw.svg|


.. method:: MiniJoyHat.get_y_raw() -> int

    Get the raw y-axis value.

    :return: y-axis value

    UIFLOW2:

        |get_y_raw.svg|


.. method:: MiniJoyHat.get_x() -> int

    Get the x-axis value.

    :return: x-axis value

    UIFLOW2:

        |get_x.svg|


.. method:: MiniJoyHat.get_y() -> int

    Get the y-axis value.

    :return: y-axis value

    UIFLOW2:

        |get_y.svg|


.. method:: MiniJoyHat.swap_x(swap: bool = True) -> None

    Swap x-axis direction

    :param swap: True or False

    UIFLOW2:

        |swap_x.svg|


.. method:: MiniJoyHat.swap_y(swap: bool = True) -> None

    Swap y-axis direction

    :param swap: True or False

    UIFLOW2:

        |swap_y.svg|

.. method:: MiniJoyHat.get_button_status() -> bool

    Get the button status.

    :return: True or False

    UIFLOW2:

        |get_button_status.svg|


.. method:: MiniJoyHat.get_firmware_version() -> str

    Get the firmware version.

    :return: firmware version

    UIFLOW2:

        |get_firmware_version.svg|


.. method:: MiniJoyHat.set_i2c_address(address: int) -> None

    Set the I2C address.

    :param address: 0x01 ~ 0x7F

    UIFLOW2:

        |set_i2c_address.svg|
