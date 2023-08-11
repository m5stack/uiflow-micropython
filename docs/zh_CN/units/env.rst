ENV Unit
========

支持以下产品：

================== ================== ==================
|ENV|_             |ENV II|_          |ENV III|_
================== ================== ==================

.. |ENV| image:: https://static-cdn.m5stack.com/resource/docs/products/unit/env/env_01.webp
    :target: https://docs.m5stack.com/en/unit/env
.. _ENV: replace:: |ENV|_

.. |ENV II| image:: https://static-cdn.m5stack.com/resource/docs/products/unit/envII/envII_01.webp
    :target: https://docs.m5stack.com/en/unit/envII
.. _ENV II: replace:: |ENV II|_

.. |ENV III| image:: https://static-cdn.m5stack.com/resource/docs/products/unit/envIII/envIII_01.webp
    :target: https://docs.m5stack.com/en/unit/envIII
.. _ENV III: replace:: |ENV III|_


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

.. image:: ../../_static/units/env/example.svg

.. only:: builder_html

    :download:`example <../../_static/units/env/example.m5f2>`.


Constructors
------------

.. class:: ENV(i2c: Union[I2C, PAHUB], type: Literal[1, 2, 3])

    创建一个ENV对象。

    参数是：

        - ``i2c`` 是一个 I2C 对象。
        - ``type`` 是ENV的类型

            - ``1`` - ENV
            - ``2`` - ENV II
            - ``3`` - ENV III

    UIFLOW2:

        .. image:: ../../_static/units/env/init.svg


Methods
-------

.. method:: ENV.read_temperature()

    此方法允许读取ENV采集的温度值并返回一个浮点型数值。计量单位为°C。

    UIFLOW2:

        .. image:: ../../_static/units/env/read_temperature.svg

.. method:: ENV.read_humidity()

    此方法允许读取ENV采集的相对湿度值并返回一个浮点型数值。计量单位为%RH。

    UIFLOW2:

        .. image:: ../../_static/units/env/read_humidity.svg

.. method:: ENV.read_pressure()

    此方法允许读取ENV采集的大气压并返回一个浮点型数值。计量单位为Pa。

    UIFLOW2:

        .. image:: ../../_static/units/env/read_pressure.svg
