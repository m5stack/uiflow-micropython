
CatchUnit
=========

.. include:: ../refs/unit.catch.ref

Catch is a gripper that uses a SG92R servo as a power source. The servo uses a PWM signal to drive the gripper gear to rotate and control the gripper for clamping and releasing operations. The structure adopts a design compatible with Lego 8mm round holes. You can combine it with other Lego components to build creative control structures, such as robotic arms, gripper carts, etc.

Support the following products:

|CatchUnit|

Micropython Example::

    import os, sys, io
    import M5
    from M5 import *
    from hardware import *
    from unit import CatchUnit
    catch = CatchUnit((33, 32))
    catch.clamp()
    catch.release()
    catch.set_duty(30)
    catch.set_clamp_percent(50)


UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

class CatchUnit
---------------

Constructors
------------

.. class:: CatchUnit(port)

    Initialize the Servo.

    - ``port``: The port to which the Servo is connected. port[1]: servo pin

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: CatchUnit.clamp()

    Clamp the gripper.


    UIFLOW2:

        |clamp.svg|

.. method:: CatchUnit.release()

    Release the gripper.


    UIFLOW2:

        |release.svg|

.. method:: CatchUnit.set_duty(duty)

    Set the duty cycle.

    - ``duty``: The duty cycle. from 20 to 54.

    UIFLOW2:

        |set_duty.svg|

.. method:: CatchUnit.set_clamp_percent(percent)

    Set the clamping percentage.

    - ``percent``: The clamping percentage. from 0 to 100.

    UIFLOW2:

        |set_clamp_percent.svg|

.. method:: CatchUnit.deinit()

    Deinitialize the Servo.


    UIFLOW2:

        |deinit.svg|





