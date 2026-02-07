Light Unit
==========

.. include:: ../refs/unit.light.ref

Support the following products:

    |Light|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/light/light_core_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


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

        |init.png|


Methods
-------

.. method:: Light.get_digital_value()

    Define digital and analog output pins.

    UIFLOW2:

        |get_digital_value.png|


.. method:: Light.get_analog_value()

    Gets the analog (returns 0-65535).

    UIFLOW2:

        |get_analog_value.png|


.. method:: Light.get_ohm()

    Gets the resistance value (returns an integer).

    UIFLOW2:

        |get_ohm.png|
