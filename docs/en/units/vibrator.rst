Vibrator Unit
=============

.. include:: ../refs/unit.vibrator.ref

Support the following products:

    |Vibrator|


class VibratorUnit
------------------

Constructors
------------

.. class:: VibratorUnit(port: tuple = (26, 0))

    Create an VibratorUnit object.

    :param port: The port where the VibratorUnit is connected to.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: VibratorUnit.once(freq=10, duty=50, duration=50) -> None

    Play the haptic effect once on the motor.

    :param int freq: The frequency of vibration ranges from 10-55Hz.
    :param int duty: The duty cycle of vibration ranges from 0-100, representing the corresponding percentage.
    :param int duration: The duration of the vibration effect, in milliseconds.

    UIFLOW2:

        |once.png|


.. method:: VibratorUnit.set_freq(freq)

    Set the vibration frequency.

    :param int freq: The frequency of vibration ranges from 10-55Hz.

    UIFLOW2:

        |set_freq.png|


.. method:: VibratorUnit.set_duty(freq) -> None

    Set the vibration duty cycle.

    :param int duty: The duty cycle of vibration ranges from 0-100, representing the corresponding percentage.

    UIFLOW2:

        |set_duty.png|


.. method:: VibratorUnit.turn_off() -> None

    Turn off the motor.

    UIFLOW2:

        |turn_off.png|


.. method:: VibratorUnit.deint() -> None

    Deinitialize the motor.

    UIFLOW2:

        |deinit.png|
