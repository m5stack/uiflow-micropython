Catch Unit
==========

.. include:: ../refs/unit.catch.ref


Catch is a gripper that uses a SG92R servo as a power source. The servo uses a
PWM signal to drive the gripper gear to rotate and control the gripper for
clamping and releasing operations. The structure adopts a design compatible with
Lego 8mm round holes. You can combine it with other Lego components to build
creative control structures, such as robotic arms, gripper carts, etc.


Support the following products:

    |CatchUnit|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/catch/cores3_catch_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |cores3_catch_example.m5f2|


class CatchUnit
---------------

Constructors
------------

.. class:: CatchUnit(port: tuple)

    Initialize the Servo.

    :param tuple port: The port to which the Servo is connected.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: CatchUnit.clamp() -> None

    Clamp the gripper.

    UIFLOW2:

        |clamp.png|


.. method:: CatchUnit.release() -> None

    Release the gripper.

    UIFLOW2:

        |release.png|


.. method:: CatchUnit.set_duty(duty: int) -> None

    Set the duty cycle.

    :param int duty: The duty cycle. from 20 to 54.

    UIFLOW2:

        |set_duty.png|


.. method:: CatchUnit.set_clamp_percent(percent: int) -> None

    Set the clamping percentage.

    :param int percent: The clamping percentage. from 0 to 100.

    UIFLOW2:

        |set_clamp_percent.png|


.. method:: CatchUnit.deinit() -> None

    Deinitialize the Servo.

    UIFLOW2:

        |deinit.png|
