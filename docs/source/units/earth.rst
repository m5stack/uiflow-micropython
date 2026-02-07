EARTH Unit
==========

.. include:: ../refs/unit.earth.ref

Support the following products:

    |EARTH|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/earth/earth_core_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |earth_core_example.m5f2|


class Earth
-----------

Constructors
------------

.. class:: Earth(port)

    Create an Earth object.

    The parameters is:
        - ``port`` Is the pin number of the port

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: EARTH.get_analog_value()

    This method allows you to read the analog captured by EARTH and return an integer value. The value ranges from 0 to 65535.

    UIFLOW2:

        |get_analog_value.png|


.. method:: EARTH.get_digital_value()

    This method allows you to read the amount of numbers collected by EARTH and return an integer value. The value ranges from 0 to 1.

    UIFLOW2:

        |get_digital_value.png|


.. method:: EARTH.get_voltage_mv()

    This method allows you to read the voltage value collected by EARTH and return an integer value. It ranges from 0 to 3300.

    UIFLOW2:

        |get_voltage_mv.png|


.. method:: EARTH.humidity()

    This method allows you to read the voltage value collected by EARTH and return a floating-point value. Range 0.0 to 1.0.

    UIFLOW2:

        |humidity.png|


.. method:: EARTH.set_calibrate()

    This method allows setting the maximum (0-3300) and minimum (0-3300) values for calibrating the EARTH sensor.

    UIFLOW2:

        |set_calibrate.png|
