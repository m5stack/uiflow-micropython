NCIR Hat
========

.. include:: ../refs/hat.ncir.ref

The following products are supported:

    |NCIRHAT|


Micropython Example:

    .. literalinclude:: ../../../examples/hat/ncir/stickc_plus2_ncir_example.py
        :language: python
        :linenos:


UIFLOW2 Example:

    |example.png|


.. only:: builder_html

    |stickc_plus2_ncir_example.m5f2|


class NCIRHat
-------------

Constructors
------------

.. class:: NCIRHat(i2c, address: int = 0x5A)

    Create a NCIRHat object.

    :param i2c: I2C object
    :param address: the I2C address of the device. Default is 0x5A.

    UIFLOW2:

        |init.png|


NCIRHat class inherits NCIRUnit class, See :ref:`unit.NCIRUnit.Methods <unit.NCIRUnit.Methods>` for more details.
