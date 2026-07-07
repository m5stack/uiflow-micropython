I2C
===

I2C implements a two-wire serial bus using an SDA data line and an SCL clock line.
Use it to communicate with Unit, Hat, and other I2C peripherals.

MicroPython Example
-------------------

Scan PORT.A on a CoreS3 or most S3-based controllers.

.. code-block:: python

    from hardware import I2C, Pin

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    print(i2c0.scan())

Scan PORT.A on Tough.

.. code-block:: python

    from hardware import I2C, Pin

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    print(i2c0.scan())

**API**
-------

class I2C
^^^^^^^^^

.. _hardware.I2C:

.. class:: I2C(id, *, scl, sda, freq=400000)

    Construct an I2C bus object.

    :param int id: I2C peripheral id.
    :keyword scl: SCL clock pin.
    :type scl: Pin or int
    :keyword sda: SDA data pin.
    :type sda: Pin or int
    :keyword int freq: I2C bus frequency in Hz.

    MicroPython Code Block:

        .. code-block:: python

            from hardware import I2C, Pin

            i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)

    .. method:: I2C.scan()

        Scan all I2C addresses between 0x08 and 0x77 and return a list of responding addresses.

        MicroPython Code Block:

            .. code-block:: python

                print(i2c0.scan())

    .. method:: I2C.readfrom_mem(addr, memaddr, nbytes, *, addrsize=8)

        Read ``nbytes`` from a device register.

        :param int addr: I2C device address.
        :param int memaddr: register address.
        :param int nbytes: number of bytes to read.
        :keyword int addrsize: register address size in bits.

    .. method:: I2C.writeto_mem(addr, memaddr, buf, *, addrsize=8)

        Write ``buf`` to a device register.

        :param int addr: I2C device address.
        :param int memaddr: register address.
        :param bytes buf: bytes-like object to write.
        :keyword int addrsize: register address size in bits.
