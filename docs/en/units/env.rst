ENV Unit
========

.. include:: ../refs/unit.env.ref

The following products are supported:

    ================== ================== ==================
    |ENV|              |ENV II|           |ENV III|
    ================== ================== ==================


Micropython Example::

    import M5
    from M5 import *
    from unit import *

    M5.begin()

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)

    env_0 = ENVUnit(i2c=i2c0, type=1) # ENVUnit
    env2_0 = ENVUnit(i2c=i2c0, type=2) # ENVUnit II
    env3_0 = ENVUnit(i2c=i2c0, type=3) # ENVUnit III

    print(env_0.read_temperature())
    print(env_0.read_humidity())
    print(env_0.read_pressure())


UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

    |env_cores3_example.m5f2|


class ENVUnit
-------------

Constructors
------------

.. class:: ENVUnit(i2c: Union[I2C, PAHUBUnit], type: Literal[1, 2, 3])

    Create an ENVUnit object.

    parameter is:

        - ``i2c`` is an I2C object.
        - ``type`` is the type of ENVUnit

            - ``1`` - ENV
            - ``2`` - ENV II
            - ``3`` - ENV III

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: ENVUnit.read_temperature()

    This method allows to read the temperature value collected by ENV and returns a floating point value. The unit of measurement is °C.

    UIFLOW2:

        |read_temperature.svg|


.. method:: ENVUnit.read_humidity()

    This method allows to read the relative humidity value collected by ENV and returns a floating point value. The unit of measurement is %RH.

    UIFLOW2:

        |read_humidity.svg|


.. method:: ENVUnit.read_pressure()

    This method allows to read the atmospheric pressure collected by ENV and returns a floating point value. The unit of measurement is Pa.

    UIFLOW2:

        |read_pressure.svg|
