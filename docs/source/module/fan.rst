Fan v1.1 Module
================

.. sku: M013-V11

.. include:: ../refs/module.fan.ref

This is the driver library of Fan Module, which is used to control the fan.

Support the following products:

    |FAN|


UiFlow2 Example
---------------

control module fan v1.1
^^^^^^^^^^^^^^^^^^^^^^^

Open the |fan_cores3_example.m5f2| project in UiFlow2.

Initializes the fan module, sets the fan status, PWM frequency and duty cycle, and displays the fan status, speed, PWM frequency and duty cycle on the screen in real time. When the user touches the screen, the fan status toggles on/off.

UiFlow2 Code Block:

    |example.png|

Example output:

    None

MicroPython Example
-------------------

control module fan v1.1
^^^^^^^^^^^^^^^^^^^^^^^

Initializes the fan module, sets the fan status, PWM frequency and duty cycle, and displays the fan status, speed, PWM frequency and duty cycle on the screen in real time. When the user touches the screen, the fan status toggles on/off.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/fan/fan_cores3_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

FanModule
^^^^^^^^^

.. autoclass:: module.fan.FanModule
    :members:
    :member-order: bysource