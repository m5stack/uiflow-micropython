4EncoderMotor Module
======================

.. sku: M138/M138-V11

.. include:: ../refs/module.encoder4_motor.ref

4EncoderMotor Module is a 4-channel encoder motor driver module that utilizes the STM32+BL5617 solution. It is suitable for various applications such as robot motion control, automation equipment, smart vehicles, laboratory equipment, and industrial automation systems.

This is the driver library for the 4EncoderMotor Module, use to control motor and read encoder value.

Support the following products:

    ================== ===================
    |4EncoderMotor|    |4EncoderMotor-V11|
    ================== ===================


UiFlow2 Example
---------------

Motor control
^^^^^^^^^^^^^

Open the |encoder4motor_core2_example.m5f2| project in UiFlow2.

This example shows how to control the motor and read the encoder value.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

Motor control
^^^^^^^^^^^^^^

This example shows how to control the motor and read the encoder value.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/encoder4_motor/encoder4motor_core2_example.py
        :language: python
        :linenos:

Example output:

    None

**API**
-------

Encoder4MotorModule
^^^^^^^^^^^^^^^^^^^^

.. autoclass:: module.encoder4_motor.Encoder4MotorModule
    :members:
    :member-order: bysource