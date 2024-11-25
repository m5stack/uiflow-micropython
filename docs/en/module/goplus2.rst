
GoPlus2Module
=============

.. include:: ../refs/module.goplus2.ref

Support the following products:

|GoPlus2Module|

Micropython Example:

    .. literalinclude:: ../../../examples/module/goplus2/goplus2_core2_example.py
        :language: python
        :linenos:

UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |goplus2_core2_example.m5f2|

class GoPlus2Module
-------------------

Constructors
------------

.. class:: GoPlus2Module(address)

    Initialize the GoPlus2Module.

    :param int|list|tuple address: The I2C address of the GoPlus2 module (default is 0x38).

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: GoPlus2Module.set_servo_angle(servo_num, angle) -> None

    Set the angle of the specified servo.

    :param int servo_num: The number of the servo (1 to 4).
    :param int angle: The angle to set the servo to (0 to 180 degrees).

    UIFLOW2:

        |set_servo_angle.png|

.. method:: GoPlus2Module.set_servo_pulse_width(servo_num, pulse_width) -> None

    Set the pulse width for the specified servo.

    :param int servo_num: The number of the servo (1 to 4).
    :param int pulse_width: The pulse width to set (in microseconds).

    UIFLOW2:

        |set_servo_pulse_width.png|

.. method:: GoPlus2Module.set_motor_speed(motor_num, speed) -> None

    Set the speed of the specified motor.

    :param int motor_num: The number of the motor (1 or 2).
    :param int speed: The speed to set (negative for reverse).

    UIFLOW2:

        |set_motor_speed.png|

.. method:: GoPlus2Module.set_digital_output(pin_num, value) -> None

    Set the digital output for the specified pin.

    :param int pin_num: The number of the pin (1 to 3).
    :param int value: The value to set (0 or 1).

    UIFLOW2:

        |set_digital_output.png|

.. method:: GoPlus2Module.get_digital_input(pin_num) -> int

    Get the digital input value of the specified pin.

    :param int pin_num: The number of the pin (1 to 3).

    UIFLOW2:

        |get_digital_input.png|

.. method:: GoPlus2Module.get_analog_input(pin_num) -> int

    Get the analog input value of the specified pin.

    :param int pin_num: The number of the pin (1 to 3).

    UIFLOW2:

        |get_analog_input.png|





