ToF Hat
=======

.. include:: ../refs/hat.tof.ref

The following products are supported:

    |ToFHat|


class ToFHat
-------------

Constructors
------------

.. class:: ToFHat(i2c: I2C, address: int = 0x29, io_timeout_ms: int = 0)

    Creates an instance of the ToFHat class.

    :param i2c: the I2C object.
    :param address: the I2C address of the device. Default is 0x23.
    :param io_timeout_ms: the timeout of I2C communication. Default is 0ms.

    UIFLOW2:

        |init.svg|


ToFHat class inherits ToFUnit class, See :ref:`unit.ToFUnit.Methods <unit.ToFUnit.Methods>` for more details.
