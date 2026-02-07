Servo Kit 180°
===============

.. sku: A076-B

.. include:: ../refs/unit.servo180.ref

This is the driver library of Servo 180 Unit, which is used to control the rotation angle of the servo.

Support the following products:

    |Servo Kit 180°|


UiFlow2 Example
---------------

Set servo angle
^^^^^^^^^^^^^^^

Open the |cores3_servo180_example.m5f2| project in UiFlow2.

This example controls the servo to rotate to different angles.

UiFlow2 Code Block:

    |cores3_servo180_example.png|

MicroPython Example
-------------------

Set servo angle
^^^^^^^^^^^^^^^

This example controls the servo to rotate to different angles.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/servo180/cores3_servo180_example.py
        :language: python
        :linenos:


**API**
-------

Servo180Unit
^^^^^^^^^^^^

.. autoclass:: unit.servo180.Servo180Unit
    :members:
