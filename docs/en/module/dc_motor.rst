DCMotor Module 
==============

.. sku: M021

.. include:: ../refs/module.dc_motor.ref

This library is the driver for Module DCMotor, and the module communicates via I2C.

Support the following products:

    |Module DCMotor|

UiFlow2 Example
---------------

Speed Control
^^^^^^^^^^^^^

Open the |cores3_dc_motor_module_speed_control.m5f2| project in UiFlow2.

This example demonstrates the use of the DCMotor Module to control the speed of a DC motor and display the motor's encoder value in real-time. 
The program automatically adjusts the motor speed, gradually increasing or decreasing the speed until it reaches the maximum or minimum value, then reverses the direction.

UiFlow2 Code Block:

    |cores3_dc_motor_module_speed_control.png|

Example output:

    None
   
MicroPython Example
-------------------

Speed Control
^^^^^^^^^^^^^

This example demonstrates the use of the DCMotor Module to control the speed of a DC motor and display the motor's encoder value in real-time. 
The program automatically adjusts the motor speed, gradually increasing or decreasing the speed until it reaches the maximum or minimum value, then reverses the direction.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/dc_motor/cores3_dc_motor_module_speed_control.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

DCMotorModule
^^^^^^^^^^^^^

.. autoclass:: module.dc_motor.DCMotorModule
    :members:
