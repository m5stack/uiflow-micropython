16340 Module
============

.. py:currentmodule:: module.module16340

.. include:: ../refs/module.module16340.ref

The following products are supported:

    |Module 16340|

``Module16340`` is a power monitor battery module. It uses the onboard INA226 sensor on the Module I2C bus to read bus voltage, shunt voltage, current, and power.

UiFlow2 Example
---------------

Read power monitor values
^^^^^^^^^^^^^^^^^^^^^^^^^

This example creates a ``Module16340`` object and reads voltage, current, and power values from the onboard INA226 sensor.

Open the |base16340_cores3_example.m5f2| project in UiFlow2.

UiFlow2 Code Block:

    |init.png|

Example output:

    None

MicroPython Example
-------------------

Read power monitor values
^^^^^^^^^^^^^^^^^^^^^^^^^

This example prints the bus voltage, shunt voltage, current, and power values.

MicroPython Code Block:

    .. literalinclude:: ../../../examples/module/ina226/base16340_cores3_example.py
        :language: python
        :linenos:

Example output:

    None

API
---

Module16340
^^^^^^^^^^^

.. autoclass:: module.module16340.Module16340
    :members:
    :inherited-members:
    :member-order: bysource
