Angle Unit
==========

.. include:: ../refs/unit.angle.ref

The following products are supported:

    |Angle|

Micropython Example::

    import M5
    from M5 import *
    from unit import *

    M5.begin()

    angle_0 = Angle((8,9))

    while True:
        print(angle_0.get_voltage())
        print(angle_0.get_value())


UIFLOW2 Example:

    |example.svg|


.. only:: builder_html

    |angle_core_example.m5f2|


class Angle
-----------

Constructors
------------

.. class:: Angle(port)

    Create an Angle object.

    parameter is:
        - ``port`` is the pins number of the port

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: Angle.get_value()

    This method allows reading the Angle's rotation value and returning an integer value. The range is 0-65535.

    UIFLOW2:

        |get_value.svg|


.. method:: Angle.get_voltage()

    This method allows reading the voltage value of Angle, and the return value is a floating point value.

    UIFLOW2:

        |get_voltage.svg|
