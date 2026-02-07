Servo Hat
==========

.. include:: ../refs/hat.servo.ref


SERVO HAT as the name suggests, is a servo motor module with the new and
upgraded "ES9251II" digital servo,This comes with 145°±10° range of motion and
can be controlled by PWM signals. The signal pin of the hat is connected to G26
on M5StickC.


Support the following products:

    |ServoHat|


Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from hat import ServoHat
    servo = ServoHat((26, 0))
    servo.set_duty(100)
    servo.set_percent(50)


UIFLOW2 Example:

    |example.png|


.. only:: builder_html


class ServoHat
--------------

Constructors
------------

.. class:: ServoHat(port: tuple)

    Initialize the Servo.

    :param tuple port: The port to which the Servo is connected. port[0]: servo pin

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ServoHat.set_duty(duty: int) -> None

    Set the duty cycle.

    :param int duty: The duty cycle. from 26 to 127.

    UIFLOW2:

        |set_duty.png|


.. method:: ServoHat.set_percent(percent: int) -> None

    Set the clamping percentage.

    :param int percent: The clamping percentage. from 0 to 100.

    UIFLOW2:

        |set_percent.png|


.. method:: ServoHat.deinit()

    Deinitialize the Servo.

    UIFLOW2:

        |deinit.png|
