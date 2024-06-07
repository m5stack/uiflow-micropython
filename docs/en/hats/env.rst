ENV Hat
========

.. include:: ../refs/hat.env.ref

The following products are supported:

    ================== ==================
    |ENV II|           |ENV III|
    ================== ==================


Micropython Example::

    import M5
    from M5 import *
    from hat import *

    M5.begin()

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)

    env_0 = ENVHat(i2c=i2c0, type=1) # ENVHat
    env2_0 = ENVHat(i2c=i2c0, type=2) # ENVHat II
    env3_0 = ENVHat(i2c=i2c0, type=3) # ENVHat III

    print(env_0.read_temperature())
    print(env_0.read_humidity())
    print(env_0.read_pressure())


class ENVHat
-------------

Constructors
------------

.. class:: ENVHat(i2c: Union[I2C, PAHUBHat], type: Literal[1, 2, 3])

    Create an ENVHat object.

    parameter is:

        - ``i2c`` is an I2C object.
        - ``type`` is the type of ENVHat

            - ``1`` - ENV
            - ``2`` - ENV II
            - ``3`` - ENV III

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: ENVHat.read_temperature()

    This method allows to read the temperature value collected by ENV and returns a floating point value. The hat of measurement is °C.

    UIFLOW2:

        |read_temperature.svg|


.. method:: ENVHat.read_humidity()

    This method allows to read the relative humidity value collected by ENV and returns a floating point value. The hat of measurement is %RH.

    UIFLOW2:

        |read_humidity.svg|


.. method:: ENVHat.read_pressure()

    This method allows to read the atmospheric pressure collected by ENV and returns a floating point value. The hat of measurement is Pa.

    UIFLOW2:

        |read_pressure.svg|
