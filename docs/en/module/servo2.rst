
Servo2Module
============

.. include:: ../refs/module.servo2module.ref

SERVO 2 is an updated servo driver module in the M5Stack stackable module series. It uses a PCA9685 16 channel PWM controller to control 16 channel servos at the same time. The power input is 6-12V DC and two SY8368AQQC chips are used for voltage reduction.

Support the following products:

|Servo2Module|

Micropython Example:

    import os, sys, io
    import M5
    from M5 import *
    from module import Servo2Module
    servo = Servo2Module()
    servo.position(0, degrees=90)
    servo.release()


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

class Servo2Module
------------------

Constructors
------------

.. class:: Servo2Module(address, freq, min_us, max_us, degrees)

    Create a Servo instance.

    :param int address: The I2C address.
    :param int freq: The PWM frequency in Hz.
    :param int min_us: The minimum pulse width in microseconds.
    :param int max_us: The maximum pulse width in microseconds.
    :param int degrees: The maximum angle in degrees.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: Servo2Module.position(index, degrees, radians, us, duty)

    Set the servo position.

    :param  index: The channel index.
    :param  degrees: The angle in degrees.
    :param  radians: The angle in radians.
    :param  us: The pulse width in microseconds.
    :param  duty: The duty cycle in percent.

    UIFLOW2:

        |position.png|

.. method:: Servo2Module.release(index)

    Release the servo.

    :param  index: The channel index.

    UIFLOW2:

        |release.png|



