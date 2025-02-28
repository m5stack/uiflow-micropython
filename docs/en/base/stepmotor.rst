Atomic Stepmotor Base
============================

.. sku: A132

.. include:: ../refs/base.stepmotor.ref

 
Support the following products:

    |Atomic Stepmotor Base|


UiFlow2 Example:
--------------------------

Direction control 
^^^^^^^^^^^^^^^^^^^^^^^^

Open the |atoms3r_stepmotor_direction_control_example.m5f2| project in UiFlow2.

The example demonstrates motor direction control. Pressing the screen button toggles the rotation direction.

UiFlow2 Code Block:

    |atoms3r_stepmotor_direction_control_example.png|

Example output:

    None

Rotate control 
^^^^^^^^^^^^^^^^^^^^^^^^

Open the |atoms3r_stepmotor_rotate_control_example.m5f2| project in UiFlow2.

The example demonstrates the motor continuously rotating for multiple turns, then reversing for multiple turns, and repeating the cycle after a 2-second pause.

UiFlow2 Code Block:

    |atoms3r_stepmotor_rotate_control_example.png|

Example output:

    None

MicroPython Example:
--------------------------

Direction control 
^^^^^^^^^^^^^^^^^^^^^^^^

The example demonstrates motor direction control. Pressing the screen button toggles the rotation direction.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/stepmotor/atoms3r_stepmotor_direction_control_example.py
        :language: python
        :linenos:

Example output:

    None

Rotate control 
^^^^^^^^^^^^^^^^^^^^^^^^

The example demonstrates the motor continuously rotating for multiple turns, then reversing for multiple turns, and repeating the cycle after a 2-second pause.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/base/stepmotor/atoms3r_stepmotor_rotate_control_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
--------------------------

AtomicStepmotorBase 
^^^^^^^^^^^^^^^^^^^^^^^^

.. autoclass:: base.stepmotor.AtomicStepmotorBase
    :members:
