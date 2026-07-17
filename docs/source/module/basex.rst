BaseX Module
============

.. py:currentmodule:: module

.. sku: M123

.. include:: ../refs/module.basex.ref

BaseX is an M5Stack stackable module with 4 DC motor channels and 2 servo
channels. It communicates with the host via I2C address ``0x22``. The onboard
controller handles motor PWM output, motor encoder count, position/speed mode
configuration, and servo output.

Support the following products:

    |BaseXModule|

UiFlow2 Example
---------------

Servo control
^^^^^^^^^^^^^

Open the |m5core_basex_servo_control_example.m5f2| project in UiFlow2.

Control two servos by button. Button A changes Servo1 angle, Button B changes
Servo2 angle, and Button C resets both servos to 0 degrees.

UiFlow2 Code Block:

    |servo_control_example.png|

Example output:

    None

Motor normal control
^^^^^^^^^^^^^^^^^^^^

Open the |m5core_basex_motor_normal_control_example.m5f2| project in UiFlow2.

Set all motors to Normal mode and control PWM duty by button.

UiFlow2 Code Block:

    |motor_normal_control_example.png|

Example output:

    None

Motor position control
^^^^^^^^^^^^^^^^^^^^^^

Open the |m5basic_basex_motor_position_control_example.m5f2| project in
UiFlow2.

Button A sets position target to 720, Button B sets target to -720, and Button C
sets target to 0.

UiFlow2 Code Block:

    |motor_position_control_example.png|

Example output:

    None

Motor speed control
^^^^^^^^^^^^^^^^^^^

Open the |m5basic_basex_motor_speed_control_example.m5f2| project in UiFlow2.

Button A increases speed target, Button B decreases speed target, and Button C
sets speed target to 0.

UiFlow2 Code Block:

    |motor_speed_control_example.png|

Example output:

    None

Read encoder
^^^^^^^^^^^^

Open the |m5basic_basex_encoder_display_example.m5f2| project in UiFlow2.

Display encoder values for four motor channels. Button B clears all encoder
values.

UiFlow2 Code Block:

    |encoder_display_example.png|

Example output:

    None

MicroPython Example
-------------------

Servo control
^^^^^^^^^^^^^

Control two servos by button.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/basex/m5core_basex_servo_control_example.py
        :language: python
        :linenos:

Example output:

    None

Motor normal control
^^^^^^^^^^^^^^^^^^^^

Set all motors to Normal mode and control PWM duty by button.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/basex/m5core_basex_motor_normal_control_example.py
        :language: python
        :linenos:

Example output:

    None

Motor position control
^^^^^^^^^^^^^^^^^^^^^^

Use position mode to move Motor1 between fixed target positions.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/basex/m5basic_basex_motor_position_control_example.py
        :language: python
        :linenos:

Example output:

    None

Motor speed control
^^^^^^^^^^^^^^^^^^^

Use speed mode to set Motor1 speed target.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/basex/m5basic_basex_motor_speed_control_example.py
        :language: python
        :linenos:

Example output:

    None

Read encoder
^^^^^^^^^^^^

Display encoder values for four motor channels. Button B clears all encoder
values.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/basex/m5basic_basex_encoder_display_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

ModuleBaseX
^^^^^^^^^^^

.. py:class:: ModuleBaseX()

    Create a BaseX module object.

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import ModuleBaseX

            basex_0 = ModuleBaseX()

    .. py:attribute:: MOTOR_MODE_NORMAL

        Normal PWM mode.

    .. py:attribute:: MOTOR_MODE_POSITION

        Position control mode.

    .. py:attribute:: MOTOR_MODE_SPEED

        Speed target control mode.

    .. py:method:: set_servo_angle(channel, angle)

        Set servo angle.

        :param int channel: Servo channel. Range: 1 ~ 2.
        :param int angle: Servo angle. Range: 0 ~ 180.

        UiFlow2 Code Block:

            |set_servo_angle.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_servo_angle(1, 90)

    .. py:method:: set_servo_pulse(channel, pulse_us)

        Set servo pulse width.

        :param int channel: Servo channel. Range: 1 ~ 2.
        :param int pulse_us: Pulse width in microseconds. Range: 500 ~ 2500.

        The servo PWM frequency is 50Hz, with a period of 20ms. The pulse range
        500 ~ 2500us corresponds to about 2.5% ~ 12.5% duty.

        UiFlow2 Code Block:

            |set_servo_pulse.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_servo_pulse(1, 1500)

    .. py:method:: set_motor_pwm(channel, duty)

        Set motor PWM duty.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int duty: PWM duty. Range: -127 ~ 127.

        The sign indicates direction. ``abs(duty)`` 0 ~ 127 maps to 0% ~ 100%
        duty.

        UiFlow2 Code Block:

            |set_motor_pwm.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_pwm(1, 80)

    .. py:method:: get_motor_speed_20ms(channel)

        Get motor speed feedback over 20ms.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :returns: Encoder delta over 20ms.
        :rtype: int

        UiFlow2 Code Block:

            |get_motor_speed_20ms.png|

        MicroPython Code Block:

            .. code-block:: python

                speed = basex_0.get_motor_speed_20ms(1)

    .. py:method:: get_motor_encoder(channel)

        Get motor encoder value.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :returns: Encoder count as signed 32-bit integer.
        :rtype: int

        UiFlow2 Code Block:

            |get_motor_encoder.png|

        MicroPython Code Block:

            .. code-block:: python

                encoder = basex_0.get_motor_encoder(1)

    .. py:method:: set_motor_encoder(channel, value)

        Set motor encoder value.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int value: Encoder count as signed 32-bit integer.

        UiFlow2 Code Block:

            |set_motor_encoder.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_encoder(1, 0)

    .. py:method:: set_motor_mode(channel, mode)

        Set motor control mode.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int mode: Motor mode. ``MOTOR_MODE_NORMAL``,
            ``MOTOR_MODE_POSITION`` or ``MOTOR_MODE_SPEED``.

        UiFlow2 Code Block:

            |set_motor_mode.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_mode(1, ModuleBaseX.MOTOR_MODE_NORMAL)

    .. py:method:: set_motor_position_pid(channel, p=3, i=1, d=15)

        Set motor position mode PID parameters.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int p: Position P parameter. Default is 3.
        :param int i: Position I parameter. Default is 1.
        :param int d: Position D parameter. Default is 15.

        UiFlow2 Code Block:

            |set_motor_position_pid.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_position_pid(1)

    .. py:method:: set_motor_position_target(channel, position)

        Set motor position mode target.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int position: Position target as signed 32-bit integer.

        UiFlow2 Code Block:

            |set_motor_position_target.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_position_target(1, 720)

    .. py:method:: set_motor_position_max_speed(channel, speed)

        Set motor position mode max speed.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int speed: Max speed. Range: -127 ~ 127.

        The sign indicates direction.

        UiFlow2 Code Block:

            |set_motor_position_max_speed.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_position_max_speed(1, 80)

    .. py:method:: set_motor_speed_pid(channel, p=3, i=1, d=15)

        Set motor speed mode PID parameters.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int p: Speed P parameter. Default is 3.
        :param int i: Speed I parameter. Default is 1.
        :param int d: Speed D parameter. Default is 15.

        UiFlow2 Code Block:

            |set_motor_speed_pid.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_speed_pid(1)

    .. py:method:: set_motor_speed_target(channel, speed)

        Set motor speed mode target.

        :param int channel: Motor channel. Range: 1 ~ 4.
        :param int speed: Speed target. Range: -20 ~ 20.

        The sign indicates direction. The target controls the feedback value
        returned by :meth:`get_motor_speed_20ms`.

        UiFlow2 Code Block:

            |set_motor_speed_target.png|

        MicroPython Code Block:

            .. code-block:: python

                basex_0.set_motor_speed_target(1, 20)
