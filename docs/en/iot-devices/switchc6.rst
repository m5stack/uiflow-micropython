SwitchC6
========

.. module:: switchc6
    :synopsis: A module for controlling the SwitchC6 device

.. include:: ../refs/iot-devices.switchc6.ref

The SwitchC6 is a device that can be controlled using the M5Stack platform. This module provides functions to interact with the SwitchC6 device.

|SwitchC6|

UiFlow2 Example
---------------

SwitchC6 Control
^^^^^^^^^^^^^^^^

Open the |cores3_switchc6_example.m5f2| project in UiFlow2.

This example demonstrates how to control the SwitchC6 device using UiFlow2.

UiFlow2 Code Block:

    |cores3_switchc6_example.png|

Example output:

    None


MicroPython Example
-------------------

SwitchC6 Control
^^^^^^^^^^^^^^^^

This example demonstrates how to control the SwitchC6 device using MicroPython.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/iot-devices/switchc6/cores3_switchc6_example.py
        :language: python
        :linenos:

Example output:

    None


**API**
-------

SwitchC6Controller
^^^^^^^^^^^^^^^^^^^

.. autoclass:: iot_devices.switchc6.SwitchC6Controller
    :members:
    :member-order: bysource
