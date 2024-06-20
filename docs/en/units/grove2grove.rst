Grove2GroveUnit
===============

.. include:: ../refs/unit.grove2grove.ref


UNIT-GROVE2GROVE is a Grove expansion Unit with On/Off Control + Current Meter
functions. On/Off control adopts switch value, Current meter is 0 - 3.3V analog
signal.


Support the following products:

    |Grove2GroveUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    import time
    from unit import Grove2GroveUnit
    grove2grove = Grove2GroveUnit((33,32)) # for core2
    grove2grove.on()


class Grove2GroveUnit
---------------------

Constructors
------------

.. class:: Grove2GroveUnit(port: tuple)

    Initialize the Grove2GroveUnit.

    :param tuple port: The port to which the Grove2GroveUnit is connected. port[0]: adc pin, port[1]: grove pin.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: Grove2GroveUnit.get_current() -> float

    Get the current of the sensor.

    :return: The current of the sensor.

    UIFLOW2:

        |get_current.svg|


.. method:: Grove2GroveUnit.on() -> None

    Turn on the grove.

    UIFLOW2:

        |on.svg|


.. method:: Grove2GroveUnit.off() -> None

    Turn off the grove.

    UIFLOW2:

        |off.svg|


.. method:: Grove2GroveUnit.set_en(state: int) -> None

    Set the state of the grove.

    :param int state: The state of the grove.

    UIFLOW2:

        |set_en.svg|
