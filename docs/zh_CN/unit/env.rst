ENV Unit
========

.. include:: ../refs/unit.env.ref

支持以下产品：

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

.. class:: ENVUnit(i2c: Union[I2C, PAHUB], type: Literal[1, 2, 3])

    创建一个ENV对象。

    参数是：

        - ``i2c`` 是一个 I2C 对象。
        - ``type`` 是ENV的类型

            - ``1`` - ENV
            - ``2`` - ENV II
            - ``3`` - ENV III

    UIFLOW2:

        |init.svg|


Methods
-------

.. method:: ENVUnit.read_temperature()

    此方法允许读取ENV采集的温度值并返回一个浮点型数值。计量单位为°C。

    UIFLOW2:

        |read_temperature.svg|

.. method:: ENVUnit.read_humidity()

    此方法允许读取ENV采集的相对湿度值并返回一个浮点型数值。计量单位为%RH。

    UIFLOW2:

        |read_humidity.svg|

.. method:: ENVUnit.read_pressure()

    此方法允许读取ENV采集的大气压并返回一个浮点型数值。计量单位为Pa。

    UIFLOW2:

        |read_pressure.svg|
