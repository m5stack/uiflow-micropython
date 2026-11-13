I2C
===

I2C implements a two-wire serial bus using an SDA data line and an SCL clock line.
Use it to communicate with Unit, Hat, and other I2C peripherals.

MicroPython Example
-------------------

Scan PORT.A on CoreS3. GPIO assignments are board-specific; do not copy
this GPIO1/GPIO2 pair to every ESP32-S3 controller.

.. code-block:: python

    from hardware import I2C, Pin

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)
    print(i2c0.scan())

Scan PORT.A on Tough.

.. code-block:: python

    from hardware import I2C, Pin

    i2c0 = I2C(0, scl=Pin(33), sda=Pin(32), freq=100000)
    print(i2c0.scan())

StickS3 uses Grove SDA GPIO9 and SCL GPIO10. The built-in system bus is
SDA GPIO47 / SCL GPIO48 and is managed by M5Unified; do not reinitialize it
to access external Units. For the external Grove bus:

.. code-block:: python

    import M5
    from hardware import I2C, Pin

    M5.begin()
    M5.Power.setExtOutput(True)
    grove = I2C(1, scl=Pin(10), sda=Pin(9), freq=100000)
    print(grove.scan())  # An empty list is normal when no I2C Unit is attached.

See the `StopWatch pin table <../controllers/stopwatch.html>`_ for its
different Grove signals. Bus id, connector pins and supply must match the
target board and connected peripheral.

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
