NCIR Unit
=========

.. include:: ../refs/unit.ncir.ref

Support the following products:

    |NCIR|


Micropython Example:

    .. literalinclude:: ../../../examples/unit/ncir/ncir_core_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |ncir_core_example.m5f2|


class NCIRUnit
--------------

Constructors
------------

.. class:: NCIRUnit(i2c)

    Create an NCIRUnit object.

    The parameters is:
        - ``i2c`` Define the i2c pin.

    UIFLOW2:

        |init.png|


.. _unit.NCIRUnit.Methods:

Methods
-------

.. method:: ncir.get_ambient_temperature()

    Obtain the ambient temperature.

    UIFLOW2:

        |get_ambient_temperature.png|


.. method:: ncir.get_object_temperature()

   Get the temperature of the measured object.

    UIFLOW2:

        |get_object_temperature.png|
