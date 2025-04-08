Thermal Unit
============

.. include:: ../refs/unit.thermal.ref

Support the following products:

    |ThermalUnit|


class ThermalUnit
-----------------

Constructors
------------

.. class:: ThermalUnit(i2c, address: int = 0x33)

    Create a ThermalUnit object.

    :param i2c: the I2C object.
    :param address: the I2C address of the device. Default is 0x33.

    UIFLOW2:

        |init.png|


.. _unit.ThermaltUnit.Methods:

Methods
-------

.. property:: ThermalUnit.get_max_temperature

    :type: float

    get the max temperature.

    UIFLOW2:

        |get_max_temperature.png|


.. property:: ThermalUnit.get_min_temperature

    :type: float

    get the min temperature.

    UIFLOW2:

        |get_min_temperature.png|


.. property:: ThermalUnit.get_midpoint_temperature

    :type: float

    get the midpoint temperature.

    UIFLOW2:

        |get_midpoint_temperature.png|


.. method:: ThermalUnit.get_pixel_temperature(x: int, y: int) -> float

    get the temperature of the pixel at the specified coordinates.

    :param int x: The x coordinate of the pixel.
    :param int y: The y coordinate of the pixel.

    :return: The temperature of the pixel.

    UIFLOW2:

        |get_pixel_temperature.png|


.. property:: ThermalUnit.get_refresh_rate

    :type: float

    get the refresh rate.

    UIFLOW2:

        |get_refresh_rate.png|


.. method:: ThermalUnit.get_temperature_buffer() -> list

    get the temperature buffer.

    :return: The temperature buffer.

    UIFLOW2:

        |get_temperature_buffer.png|


.. method:: ThermalUnit.set_refresh_rate(rate: int) -> None

    Set the refresh rate.

    :param int rate: The refresh rate in Hz.

    UIFLOW2:

        |set_refresh_rate.png|


.. method:: ThermalUnit.update_temperature_buffer() -> bytes

    Update the temperature buffer.

    :return: The temperature buffer.

    UIFLOW2:

        |update_temperature_buffer.png|
