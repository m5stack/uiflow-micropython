Angle Unit
==========

.. include:: ../refs/unit.angle.ref

The following products are supported:

    |Angle|

Micropython Example::

    import M5
    from M5 import *
    from unit import AngleUnit

    M5.begin()

    angle_0 = AngleUnit((8,9))

    while True:
        print(angle_0.get_voltage())
        print(angle_0.get_value())


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |angle_core_example.m5f2|


class AngleUnit
---------------

Constructors
------------

Import with ``from unit import AngleUnit``.

.. class:: AngleUnit(port)

    Create an AngleUnit object.

    parameter is:
        - ``port`` is the pins number of the port

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: AngleUnit.get_value()

    This method allows reading the Angle's rotation value and returning an integer value. The range is 0-65535.

    UIFLOW2:

        |get_value.png|


.. method:: AngleUnit.get_voltage()

    This method allows reading the voltage value of Angle, and the return value is a floating point value.

    UIFLOW2:

        |get_voltage.png|
