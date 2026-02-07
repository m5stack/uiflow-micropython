Servo Kit 360°
==============

.. sku: A076-A

.. include:: ../refs/unit.servo360.ref

This is the driver library of Servo 360 Unit, which is used to control the rotation speed and direction of the servo.

Support the following products:

    |Servo Kit 360°|


UiFlow2 Example
---------------

Control servo rotation
^^^^^^^^^^^^^^^^^^^^^^

Open the |cores3_servo360_example.m5f2| project in UiFlow2.

This example controls the servo rotation direction and speed.

UiFlow2 Code Block:

    |cores3_servo360_example.png|

MicroPython Example
-------------------

Control servo rotation
^^^^^^^^^^^^^^^^^^^^^^

This example controls the servo rotation direction and speed.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/unit/servo360/cores3_servo360_example.py
        :language: python
        :linenos:


**API**
-------

Servo360Unit
^^^^^^^^^^^^

.. autoclass:: unit.servo360.Servo360Unit
    :members:
