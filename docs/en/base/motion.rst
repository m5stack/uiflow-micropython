Motion Base
===========

.. include:: ../refs/base.motion.ref

Atomic Motion Base is a servo and DC motor driver designed specifically for the ATOM series controllers. It integrates an STM32 control chip internally and uses I2C communication for control. Atomic Motion Base provides 4 servo channels and 2 DC motor interfaces, offering convenience for scenarios that require control of multiple servos or motor drivers, such as multi-axis servo robotic arms or small car motor control.

Atomic Motion Base v1.1 adds INA226 to implement current and voltage detection.

Support the following products:

|Motion|

|Motion Base v1.1|


Micropython Example:
----------------------------

Motion Base
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../examples/base/motion/atoms3_lite_motion_base_example.py
        :language: python
        :linenos:

Motion Base v1.1  
++++++++++++++++++++++++++++

    .. literalinclude:: ../../../examples/base/motion/atoms3_motion_base_v1.1_example.py
        :language: python
        :linenos:

UIFlow2.0 Example:
----------------------------

Motion Base  
++++++++++++++++++++++++++++

    |example.png|

.. only:: builder_html

    |atoms3_lite_motion_base_example.m5f2|

Motion Base v1.1
++++++++++++++++++++++++++++

    |motion_base_v1.1_example.png|

.. only:: builder_html

    |atoms3_motion_base_v1.1_example.m5f2|


class Motion
------------

Constructors
-------------

.. method:: Motion(i2c, address)

    Initialize the Servo8.

    - ``i2c``: I2C port to use.
    - ``address``: I2C address of the servo8.

    UIFlow2.0:

        |__init__.png|

Methods
-------

.. method:: Motion.get_servo_angle(ch)

    Get the angle of the servo.

    - ``ch``: Servo channel (1 to 4).

    UIFlow2.0:

        |get_servo_angle.png|

.. method:: Motion.set_servo_angle(ch, angle)

    Set the angle of the servo.

    - ``ch``: Servo channel (1 to 4).
    - ``angle``: Angle of the servo (0 to 180).

    UIFlow2.0:

        |set_servo_angle.png|

.. method:: Motion.get_servo_pulse(ch)

    Get the pulse width of the servo.

    - ``ch``: Servo channel (1 to 4).

    UIFlow2.0:

        |get_servo_pulse.png|

.. method:: Motion.write_servo_pulse(ch, pulse)

    Set the pulse width of the servo.

    - ``ch``: Servo channel (1 to 4).
    - ``pulse``: Pulse width of the servo (500 to 2500).

    UIFlow2.0:

        |write_servo_pulse.png|

.. method:: Motion.get_motor_speed(ch)

    Get the speed of the motor.

    - ``ch``: Motor channel (1 or 2).

    UIFlow2.0:

        |get_motor_speed.png|

.. method:: Motion.set_motor_speed(ch, speed)

    Set the speed of the motor.

    - ``ch``: Motor channel (1 or 2).
    - ``speed``: Speed of the motor (-127 to 127).

    UIFLOW2:

        |set_motor_speed.png|

.. method:: Motion.read_voltage() -> float

    Read voltage (unit: V)

    .. note::
        This method is supported only on Motion Base v1.1 and later versions.

    UIFlow2.0

        |read_voltage.png|

.. method:: Motion.read_current() -> float

    Read voltage (unit: A)

    .. note::
        This method is supported only on Motion Base v1.1 and later versions.

    UIFlow2.0

        |read_current.png|

.. method:: Motion.read_power() -> float

    Read power (unit: W)

    .. note::
        This method is supported only on Motion Base v1.1 and later versions.

    UIFlow2.0

        |read_power.png|