CardKB Hat
==========

.. include:: ../refs/hat.cardkb.ref

The following products are supported:

    |CardKB Hat|


class CardKBHat
---------------

Constructors
------------

.. class:: CardKBHat(i2c: I2C, address: int | list | tuple = 0x5F)

    Create a CardKBHat object.

    :param i2c: I2C object
    :param address: the I2C address of the device. Default is 0x5F.

    UIFLOW2:

        |init.png|


CardKBHat class inherits CardKBUnit class, See :ref:`unit.CardKBUnit.Methods <unit.CardKBUnit.Methods>` for more details.
