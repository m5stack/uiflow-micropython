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


class ULTRASONIC_I2C
--------------------

Constructors
--------------

.. class:: ULTRASONIC_I2C(PORT)

    Create a ULTRASONIC I2C object.

    The parameters is:
        - ``PORT`` Define an i2c port.

    UIFLOW2:

        |init.png|


Methods
-------

.. method:: ULTRASONIC_I2C.get_target_distance()

    Acquire transmitting distance

    UIFLOW2:

        |get_target_distance.png|
