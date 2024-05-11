Buzzer Unit
===========

.. include:: ../refs/unit.buzzer.ref

Support the following products:

    |Buzzer|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    import time
    from unit import BuzzerUnit

    vib_0 = BuzzerUnit((33, 32))


.. UIFLOW2 Example:

.. .. |example.svg|


.. .. only:: builder_html

.. ..     |adc_core_example.m5f2|


class BuzzerUnit
-----------------

Constructors
------------

.. class:: BuzzerUnit(port)

    Create an BuzzerUnit object.

    The parameters are:
        - ``port`` Is the pin number of the port

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: BuzzerUnit.once(freq=10, duty=50, duration=50)

    Play buzzer once.

    :param int freq: The frequency of the vibration, range is 100 - 10000Hz.
    :param int duty: The duty cycle of the vibration, range is 0 - 100.
    :param int duration: The duration of the vibration, range is 0 - 10000ms.

    UIFLOW2:

        |once.svg|


.. method:: BuzzerUnit.set_freq(freq: int)

    Set the frequency of the buzzer.

    :param int freq: The frequency of the vibration, range is 100 - 10000Hz.

    UIFLOW2:

        |set_freq.svg|


.. method:: BuzzerUnit.set_duty(duty: int)

    Set the duty cycle of the buzzer.

    :param int duty: The duty cycle of the vibration, range is 0 - 100.

    UIFLOW2:

        |set_duty.svg|


.. method:: BuzzerUnit.turn_off()

    Turn off the buzzer.

    UIFLOW2:

        |turn_off.svg|


.. method:: BuzzerUnit.deint()

    Deinitialize the buzzer.

    UIFLOW2:

        |deinit.svg|
