Grove2Grove Unit
================

.. include:: ../refs/unit.grove2grove.ref


UNIT-GROVE2GROVE is a Grove expansion Unit with On/Off Control + Current Meter
functions. On/Off control adopts switch value, Current meter is 0 - 3.3V analog
signal.


Support the following products:

    |Grove2GroveUnit|

Micropython Example:

    .. literalinclude:: ../../../examples/unit/grove2grove/cores3_grove2_grove_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |cores3_grove2_grove_example.m5f2|


class Grove2GroveUnit
---------------------

Constructors
------------

.. class:: Grove2GroveUnit(port: tuple)

    Initialize the Grove2GroveUnit.

    :param tuple port: The port to which the Grove2GroveUnit is connected. port[0]: adc pin, port[1]: grove pin.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: Grove2GroveUnit.get_current() -> float

    Get the current of the sensor.

    :return: The current of the sensor.

    UIFLOW2:

        |get_current.png|


.. method:: Grove2GroveUnit.on() -> None

    Turn on the grove.

    UIFLOW2:

        |on.png|


.. method:: Grove2GroveUnit.off() -> None

    Turn off the grove.

    UIFLOW2:

        |off.png|


.. method:: Grove2GroveUnit.set_en(state: int) -> None

    Set the state of the grove.

    :param int state: The state of the grove.

    UIFLOW2:

        |set_en.png|
