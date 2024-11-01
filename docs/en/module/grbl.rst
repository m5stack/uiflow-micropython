
GRBLModule
==========

.. include:: ../refs/module.grblmodule.ref

GRBL 13.2 is a three-axis stepper motor driver module in the M5Stack stacking module series. It uses an ATmega328P-AU controller with three sets of DRV8825PWPR stepper motor driver chip control ways, which can drive three bipolar steppers at the same time.

Support the following products:

|GRBLModule|

Micropython Example:

    .. literalinclude:: ../../../examples/module/grbl_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|

.. only:: builder_html

    |grbl_example.m5f2|

class GRBLModule
----------------

Constructors
------------

.. class:: GRBLModule(address)

    Initialize the GRBLModule.

    :param hex address: The I2C address of the device.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: GRBLModule.g_code(command)

    Send the G-code command.

    :param  command: The G-code command.

    UIFLOW2:

        |g_code.png|

.. method:: GRBLModule.get_code_time(code)

    Get the time of the code.

    :return (int): The estimated time of the command.
    :param  code: The G-code command

    UIFLOW2:

        |get_code_time.png|

.. method:: GRBLModule.turn(x, y, z, speed)

    Turn the motor to a specific position.

    :param  x: The position of the X motor, 1.6&#x3D;360°.
    :param  y: The position of the Y motor, 1.6&#x3D;360°.
    :param  z: The position of the Z motor, 1.6&#x3D;360°.
    :param  speed: The speed of the motor.

    UIFLOW2:

        |turn.png|

.. method:: GRBLModule.set_mode(mode)

    Set the mode of the motor.

    :param  mode: The mode of the motor.
        Options:
        - ``Absolute``: GRBLModule.MODE_ABSOLUTE
        - ``Relative``: GRBLModule.MODE_RELATIVE

    UIFLOW2:

        |set_mode.png|

.. method:: GRBLModule.init(x_step, y_step, z_step, acc)

    Initialize the motor.

    :param  x_step: The step of the X motor.
    :param  y_step: The step of the Y motor.
    :param  z_step: The step of the Z motor.
    :param  acc: The acceleration of the motor.

    UIFLOW2:

        |init.png|

.. method:: GRBLModule.flush()

    Flush the buffer.


    UIFLOW2:

        |flush.png|

.. method:: GRBLModule.get_message()

    Get the message.

    :return (str): The message string.

    UIFLOW2:

        |get_message.png|

.. method:: GRBLModule.get_status()

    Get the status.

    :return (str): The status string.

    UIFLOW2:

        |get_status.png|

.. method:: GRBLModule.get_idle_state()

    Get the idle state.

    :return (bool): The idle state.

    UIFLOW2:

        |get_idle_state.png|

.. method:: GRBLModule.get_lock_state()

    Get the lock state.

    :return (bool): The lock state.

    UIFLOW2:

        |get_lock_state.png|

.. method:: GRBLModule.wait_idle()

    Wait until the motor is idle.


    UIFLOW2:

        |wait_idle.png|

.. method:: GRBLModule.unlock_alarm_state()

    Unlock the alarm state.


    UIFLOW2:

        |unlock_alarm_state.png|

.. method:: GRBLModule.lock()

    Lock the motor.


    UIFLOW2:

        |lock.png|

.. method:: GRBLModule.unlock()

    Unlock the motor.


    UIFLOW2:

        |unlock.png|



Constants
---------

    .. data:: GRBLModule.MODE_ABSOLUTE
    .. data:: GRBLModule.MODE_RELATIVE

    Motor mode

