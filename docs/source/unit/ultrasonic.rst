Ultrasonic Unit
===============

.. include:: ../refs/unit.ultrasonic.ref

Support the following products:

    |Ultrasonic|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/ultrasonic/ultrasonic_core_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |ultrasonic_core_example.m5f2|


class UltrasoundI2CUnit
-----------------------

Constructors
--------------

Import with ``from unit import UltrasoundI2CUnit``.

.. class:: UltrasoundI2CUnit(i2c, address=0x57)

    Create a ULTRASONIC I2C object.

    The parameters is:
        - ``i2c`` is an initialized I2C bus or PAHUB port.
        - ``address`` is the I2C address (default 0x57).

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: UltrasoundI2CUnit.get_target_distance()

    Acquire transmitting distance

    UIFLOW2:

        |get_target_distance.png|
