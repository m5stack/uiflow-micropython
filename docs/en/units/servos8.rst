8Servos Unit
============

.. sku: U165

.. include:: ../refs/unit.servos8.ref

This is the driver library for the 8Servos Unit. It is a 8-channel servo
controller that can control up to 8 servos. It can be used to control the
angles of the servos, set the pulse width, and set the mode of the servos.

Support the following products:

    |8Servos Unit|


UiFlow2 Example
---------------

servo control
^^^^^^^^^^^^^

Open the |cores3_servo_example.m5f2| project in UiFlow2.

This example controls the servo angle of the 8Servos Unit.

UiFlow2 Code Block:

    |example_servo.png|

Example output:

    None


rgb control
^^^^^^^^^^^

Open the |cores3_rgb_example.m5f2| project in UiFlow2.

This example controls the RGB LED of the 8Servos Unit.

UiFlow2 Code Block:

    |example_rgb.png|

Example output:

    None


MicroPython Example
-------------------

servo control
^^^^^^^^^^^^^

This example controls the servo angle of the 8Servos Unit.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/8servos/cores3_servo_example.py
        :language: python
        :linenos:

Example output:

    None


rgb control
^^^^^^^^^^^

This example controls the RGB LED of the 8Servos Unit.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/8servos/cores3_rgb_example.py
        :language: python
        :linenos:

Example output:

    None



**API**
-------

Servos8Unit
^^^^^^^^^^^

.. autoclass:: unit.servos8.Servos8Unit
    :members:
