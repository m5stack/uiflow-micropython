
Motion Base
===========

.. include:: ../refs/base.motion.ref

Atomic Motion Base is a servo and DC motor driver designed specifically for the ATOM series controllers. It integrates an STM32 control chip internally and uses I2C communication for control. Atomic Motion Base provides 4 servo channels and 2 DC motor interfaces, offering convenience for scenarios that require control of multiple servos or motor drivers, such as multi-axis servo robotic arms or small car motor control.

Support the following products:

|Motion|


Micropython Example:

    .. literalinclude:: ../../../examples/base/motion/atoms3_lite_motion_base_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |atoms3_lite_motion_base_example.m5f2|


class Motion
------------

Constructors
-------------

.. method:: Motion(i2c, address)

    Initialize the Servo8.

    - ``i2c``: I2C port to use.
    - ``address``: I2C address of the servo8.

    UIFLOW2:

        |__init__.png|


Methods
-------

.. method:: Motion.get_servo_angle(ch)

    Get the angle of the servo.

    - ``ch``: Servo channel (1 to 4).

    UIFLOW2:

        |get_servo_angle.png|

.. method:: Motion.set_servo_angle(ch, angle)

    Set the angle of the servo.

    - ``ch``: Servo channel (1 to 4).
    - ``angle``: Angle of the servo (0 to 180).

    UIFLOW2:

        |set_servo_angle.png|

.. method:: Motion.get_servo_pulse(ch)

    Get the pulse width of the servo.

    - ``ch``: Servo channel (1 to 4).

    UIFLOW2:

        |get_servo_pulse.png|

.. method:: Motion.write_servo_pulse(ch, pulse)

    Set the pulse width of the servo.

    - ``ch``: Servo channel (1 to 4).
    - ``pulse``: Pulse width of the servo (500 to 2500).

    UIFLOW2:

        |write_servo_pulse.png|

.. method:: Motion.get_motor_speed(ch)

    Get the speed of the motor.

    - ``ch``: Motor channel (1 or 2).

    UIFLOW2:

        |get_motor_speed.png|

.. method:: Motion.set_motor_speed(ch, speed)

    Set the speed of the motor.

    - ``ch``: Motor channel (1 or 2).
    - ``speed``: Speed of the motor (-127 to 127).

    UIFLOW2:

        |set_motor_speed.png|


