Vibrator HAT
============

.. include:: ../refs/hats.vibrator.ref

Support the following products:

    |Vibrator|


Micropython Example:

    .. literalinclude:: ../../../examples/hat/vibrator/vibrator_stick_plus2.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.svg|


.. .. only:: builder_html

.. ..     |adc_core_example.m5f2|


class VibratorHAT
-----------------

Constructors
------------

.. class:: VibratorHAT()

    Create an VibratorHAT object.

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: VibratorHAT.once(freq=10, duty=50, duration=50) -> None

    Play the haptic effect once on the motor.

    :param int freq: The frequency of vibration ranges from 10-55Hz.
    :param int duty: The duty cycle of vibration ranges from 0-100, representing the corresponding percentage.
    :param int duration: The duration of the vibration effect, in milliseconds.

    UIFLOW2:

        |once.svg|


.. method:: VibratorHAT.set_freq(freq)

    Set the vibration frequency.

    :param int freq: The frequency of vibration ranges from 10-55Hz.

    UIFLOW2:

        |set_freq.svg|


.. method:: VibratorHAT.set_duty(freq) -> None

    Set the vibration duty cycle.

    :param int duty: The duty cycle of vibration ranges from 0-100, representing the corresponding percentage.

    UIFLOW2:

        |set_duty.svg|


.. method:: VibratorHAT.turn_off() -> None

    Turn off the motor.

    UIFLOW2:

        |turn_off.svg|


.. method:: VibratorHAT.deint() -> None

    Deinitialize the motor.

    UIFLOW2:

        |deinit.svg|
