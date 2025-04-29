Buzzer Unit
===========

.. include:: ../refs/unit.buzzer.ref

Support the following products:

    |Buzzer|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/buzzer/cores3_buzzer_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_buzzer_example.m5f2|


class BuzzerUnit
-----------------

Constructors
------------

.. class:: BuzzerUnit(port)

    Create an BuzzerUnit object.

    The parameters are:
        - ``port`` Is the pin number of the port

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: BuzzerUnit.once(freq=10, duty=50, duration=50)

    Play buzzer once.

    :param int freq: The frequency of the vibration, range is 100 - 10000Hz.
    :param int duty: The duty cycle of the vibration, range is 0 - 100.
    :param int duration: The duration of the vibration, range is 0 - 10000ms.

    UIFLOW2:

        |once.png|


.. method:: BuzzerUnit.set_freq(freq: int)

    Set the frequency of the buzzer.

    :param int freq: The frequency of the vibration, range is 100 - 10000Hz.

    UIFLOW2:

        |set_freq.png|


.. method:: BuzzerUnit.set_duty(duty: int)

    Set the duty cycle of the buzzer.

    :param int duty: The duty cycle of the vibration, range is 0 - 100.

    UIFLOW2:

        |set_duty.png|


.. method:: BuzzerUnit.turn_off()

    Turn off the buzzer.

    UIFLOW2:

        |turn_off.png|


.. method:: BuzzerUnit.deint()

    Deinitialize the buzzer.

    UIFLOW2:

        |deinit.png|
