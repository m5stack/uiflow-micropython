Light Unit
==========

.. include:: ../refs/unit.light.ref

Support the following products:

    |Light|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from unit import *


    light_0 = None


    def setup():
    global light_0

    light_0 = Light((8,9))
    M5.begin()
    Widgets.fillScreen(0x222222)

    print(light_0.get_analog_value())


UIFLOW2 Example:

    |example.svg|


.. only:: builder_html

    |light_core_example.m5f2|


class Light
-----------

Constructors
------------

.. class:: Light(IO1,IO2)

    Create a Light object.

    The parameters are:
        - ``IO1,IO2`` Define digital and analog output pins.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: Light.get_digital_value()

    Define digital and analog output pins.

    UIFLOW2:

        |get_digital_value.svg|


.. method:: Light.get_analog_value()

    Gets the analog (returns 0-65535).

    UIFLOW2:

        |get_analog_value.svg|


.. method:: Light.get_ohm()

    Gets the resistance value (returns an integer).

    UIFLOW2:

        |get_ohm.svg|
