Bala2 Module
============================

.. sku: K014-E

.. include:: ../refs/module.bala2.ref

The Bala2 Module is part of the M5Stack stackable module series. The module communicates with the host via the I2C interface, and its built-in microcontroller manages PWM control for the motor, reads the encoder count, and outputs control signals for the servo.

Support the following products:

    |Bala2-Fire|


UiFlow2 Example
--------------------------

Servo control 
^^^^^^^^^^^^^^^^^^^^^^^^

Open the |servo_control_example.m5f2| project in UiFlow2.

Control the servo to swing back and forth between 0° and 180°.

UiFlow2 Code Block:

    |servo_control_example.png|

Example output:

    None

Motor control 
^^^^^^^^^^^^^^^^^^^^^^^^

Open the |motor_control_example.m5f2| project in UiFlow2.

Run the program, and the car's motors will first rotate forward, gradually accelerating to the maximum speed, then gradually decelerating to a stop. Next, the motors will reverse, similarly accelerating to the maximum speed before gradually slowing down to a stop. Finally, the car will come to a complete stop, with the motor speed returning to zero.

UiFlow2 Code Block:

    |motor_control_example.png|

Example output:

    None

Read encoder 
^^^^^^^^^^^^^^^^^^^^^^^^

Open the |read_encoder_example.m5f2| project in UiFlow2.

Run the program and manually rotate the wheels to observe the screen display.

UiFlow2 Code Block:

    |read_encoder_example.png|

Example output:

    None

Car control 
^^^^^^^^^^^^^^^^^^^^^^^^

Open the |car_control_example.m5f2| project in UiFlow2.

Save the program to the controller, place the car on its side, and turn it on. After the gyroscope calibration is complete, the car will automatically stand upright and maintain balance. It will then perform a series of actions, including turning left, turning right, moving forward, and moving backward. Finally, it will stop and return to the balanced state.

UiFlow2 Code Block:

    |car_control_example.png|

Example output:

    None

MicroPython Example 
--------------------------

Servo control 
^^^^^^^^^^^^^^^^^^^^^^^^

Control the servo to swing back and forth between 0° and 180°.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/bala2/servo_control_example.py
        :language: python
        :linenos:

Example output:

    None

Motor control 
^^^^^^^^^^^^^^^^^^^^^^^^

Run the program, and the car's motors will first rotate forward, gradually accelerating to the maximum speed, then gradually decelerating to a stop. Next, the motors will reverse, similarly accelerating to the maximum speed before gradually slowing down to a stop. Finally, the car will come to a complete stop, with the motor speed returning to zero.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/bala2/motor_control_example.py
        :language: python
        :linenos:

Example output:

    None

Read encoder 
^^^^^^^^^^^^^^^^^^^^^^^^

Run the program and manually rotate the wheels to observe the screen display.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/bala2/read_encoder_example.py
        :language: python
        :linenos:

Example output:

    None

Car control 
^^^^^^^^^^^^^^^^^^^^^^^^

Save the program to the controller, place the car on its side, and turn it on. After the gyroscope calibration is complete, the car will automatically stand upright and maintain balance. It will then perform a series of actions, including turning left, turning right, moving forward, and moving backward. Finally, it will stop and return to the balanced state.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/bala2/car_control_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
--------------------------

Bala2Module 
^^^^^^^^^^^^^^^^^^^^^^^^
      
.. class:: module.bala2.Bala2Module(timer_id = 0)

    Create an Bala2Module object.

    :param int timer_id: Timer ID from 0 to 3 (Use a timer to periodically call the balance control program.)

    UiFlow2 Code Block:

        |init.png|

    MicroPython Code Block:

        .. code-block:: python

            from module import Bala2Module

            module_bala2_0 = Bala2Module(timer_id = 0)

    .. method:: calibrate()

        Calibrate sensor 

        UiFlow2 Code Block:

            |calibrate.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.calibrate()

    .. method:: set_motor_speed(left, right)
        
        Set motor speed 

        :param int left: The speed of the left motor. Range: -1023 ~ 1023.
        :param int right: The speed of the right motor. Range: -1023 ~ 1023.

        UiFlow2 Code Block:

            |set_motor_speed.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_motor_speed(left, right)

    .. method:: set_encoder_value(left, right)

        Set encoder value

        :param int left: The value of the left encoder. Range: -2^31 ~ 2^31.
        :param int right: The value of the right encoder. Range: -2^31 ~ 2^31.

        UiFlow2 Code Block:

            |set_encoder_value.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_encoder_value(left, right)

    .. method:: get_encoder_value()

        The left, right encoder value returned in a 2-tuple  

        :returns: left, right encoder value
        :rtype: tuple[int, int]

        UiFlow2 Code Block:

            |get_encoder_value.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.get_encoder_value()

    .. method:: set_servo_angle(pos, angle)

        Set servo angle   

        :param int pos: The position of the output cahnnel. Range: 1 ~ 4.
        :param int angle: The value of the right encoder. Range: 0 ~ 180.

        UiFlow2 Code Block:

            |set_servo_angle.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_servo_angle(pos, angle)

    .. method:: start()

        Start the balance car (car upright balance) 

        UiFlow2 Code Block:

            |start.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.start()

    .. method:: stop()

        Stop the balance car (stop the balance control of the car) 

        UiFlow2 Code Block:

            |stop.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.stop()

    .. method:: get_angle()

        Get the tilt angle of the balance car

        :returns: The angle of the car
        :rtype: int

        Data is valid only when the car is running (start() is called).

        UiFlow2 Code Block:

            |get_angle.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.get_angle()

    .. method:: set_angle_pid(kp, ki, kd)

        Set angle PID parameters

        :param float kp: Proportional gain
        :param float ki: Integral gain
        :param float kd: Derivative gain

        UiFlow2 Code Block:

            |set_angle_pid.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_angle_pid(kp, ki, kd)

    .. method:: get_angle_pid()

        The angle loop PID parameters returned in a 3-tuple 

        :returns: kp, ki, kd parameters  
        :rtype: tuple[float, float, float]

        UiFlow2 Code Block:

            |get_angle_pid.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.get_angle_pid()

    .. method:: set_angle_pid_target(angle = 0)

        Set angle loop PID control target.

        :param float angle: The angle of the angle loop PID control target. Default is 0.

        UiFlow2 Code Block:

            |set_angle_pid_target.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_angle_pid_target(angle)

    .. method:: get_angle_pid_target() 

        Get angle loop PID control target  

        :returns: The angle loop PID control target 
        :rtype: float 

        UiFlow2 Code Block:

            |get_angle_pid_target.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.get_angle_pid_target()

    .. method:: set_speed_pid(kp, ki, kd)

        Set speed loop PID parameters.

        :param float kp: Proportional gain
        :param float ki: Integral gain
        :param float kd: Derivative gain

        UiFlow2 Code Block:

            |set_speed_pid.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_speed_pid(kp, ki, kd)

    .. method:: get_speed_pid()

        The speed loop PID parameters returned in a 3-tuple 

        :returns: kp, ki, kd parameters  
        :rtype: tuple[float, float, float]

        UiFlow2 Code Block:

            |get_speed_pid.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.get_speed_pid()

    .. method:: set_speed_pid_target(speed = 0)

        Set speed loop PID control target.

        :param float speed: The speed of the speed loop PID control target. Default is 0.

        UiFlow2 Code Block:

            |set_speed_pid_target.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_speed_pid_target(speed)

    .. method:: get_speed_pid_target() 

        Get speed loop PID control target  

        :returns: The speed loop PID control target 
        :rtype: float 

        UiFlow2 Code Block:

            |get_speed_pid_target.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.get_speed_pid_target()

    .. method:: set_turn_speed(speed)

        Set turning speed 

        :param float speed: The speed of the left and right motor offset

        UiFlow2 Code Block:

            |set_turn_speed.png|

        MicroPython Code Block:

            .. code-block:: python

                module_bala2_0.set_turn_speed(speed)
