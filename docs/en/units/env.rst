ENV Unit
========

.. include:: ../refs/unit.env.ref

The following products are supported：

================== ================== ==================
|ENV|              |ENV II|           |ENV III|
================== ================== ==================


Micropython Example::

    import M5
    from M5 import *
    from unit import *

    M5.begin()

    i2c0 = I2C(0, scl=Pin(1), sda=Pin(2), freq=100000)

    env_0 = ENV(i2c=i2c0, type=1) # ENV
    env2_0 = ENV(i2c=i2c0, type=2) # ENV II
    env3_0 = ENV(i2c=i2c0, type=3) # ENV III

    print(env_0.read_temperature())
    print(env_0.read_humidity())
    print(env_0.read_pressure())


UIFLOW2 Example:

    |example.svg|

.. only:: builder_html

|env_cores3_example.m5f2|


class ENV
---------

Constructors
------------

.. class:: ENV(i2c: Union[I2C, PAHUB], type: Literal[1, 2, 3])

    Create an ENV object.

    parameter is:

        - ``i2c`` is an I2C object.
        - ``type`` is the type of ENV

            - ``1`` - ENV
            - ``2`` - ENV II
            - ``3`` - ENV III

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: ENV.read_temperature()

    This method allows to read the temperature value collected by ENV and returns a floating point value. The unit of measurement is °C.

    UIFLOW2:

        |read_temperature.svg|

.. method:: ENV.read_humidity()

    This method allows to read the relative humidity value collected by ENV and returns a floating point value. The unit of measurement is %RH.

    UIFLOW2:

        |read_humidity.svg|

.. method:: ENV.read_pressure()

    This method allows to read the atmospheric pressure collected by ENV and returns a floating point value. The unit of measurement is Pa.

    UIFLOW2:

        |read_pressure.svg|
